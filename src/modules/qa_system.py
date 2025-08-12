"""
Q&A System Module
=================

This module provides a question-answering system using GPT-4
to answer questions about business reports and documents.

Author: Report GPT Team
Date: 2024
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging
from datetime import datetime
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QASystem:
    """
    Q&A System Class
    
    Provides question-answering capabilities using GPT-4
    and existing document knowledge.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize Q&A System
        
        Args:
            api_key: OpenAI API key (optional, will use env var if not provided)
            model: GPT model to use (default: gpt-4)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY in .env file")
        
        self.model = model
        
        # Initialize OpenAI client
        openai.api_key = self.api_key
        
        # Output directory
        self.output_dir = Path("data/output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load training data for context
        self.training_data = self._load_training_data()
        
        logger.info(f"Q&A System initialized with model: {model}")
    
    def _load_training_data(self) -> Dict:
        """
        Load training data for context
        
        Returns:
            Training data dictionary
        """
        try:
            training_file = self.output_dir / "training_dataset.json"
            if training_file.exists():
                with open(training_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.info(f"Loaded training data with {len(data.get('qa_pairs', []))} Q&A pairs")
                return data
            else:
                logger.warning("Training dataset not found")
                return {"qa_pairs": []}
        except Exception as e:
            logger.error(f"Error loading training data: {e}")
            return {"qa_pairs": []}
    
    def _get_relevant_context(self, question: str, max_context: int = 5) -> str:
        """
        Get relevant context from training data
        
        Args:
            question: User question
            max_context: Maximum number of relevant Q&A pairs to include
            
        Returns:
            Relevant context string
        """
        if not self.training_data.get('qa_pairs'):
            return ""
        
        # Simple keyword matching for relevance
        question_lower = question.lower()
        relevant_pairs = []
        
        for qa_pair in self.training_data['qa_pairs']:
            qa_question = qa_pair.get('question', '').lower()
            qa_answer = qa_pair.get('answer', '').lower()
            
            # Check if question keywords match
            relevance_score = 0
            for word in question_lower.split():
                if word in qa_question or word in qa_answer:
                    relevance_score += 1
            
            if relevance_score > 0:
                relevant_pairs.append({
                    'score': relevance_score,
                    'question': qa_pair.get('question', ''),
                    'answer': qa_pair.get('answer', '')
                })
        
        # Sort by relevance and take top matches
        relevant_pairs.sort(key=lambda x: x['score'], reverse=True)
        context_pairs = relevant_pairs[:max_context]
        
        # Build context string
        context = "Relevant information from documents:\n\n"
        for i, pair in enumerate(context_pairs, 1):
            context += f"{i}. Q: {pair['question']}\n   A: {pair['answer']}\n\n"
        
        return context
    
    def ask_question(self, question: str, include_context: bool = True) -> Dict:
        """
        Ask a question and get answer from GPT-4
        
        Args:
            question: User question
            include_context: Whether to include relevant context
            
        Returns:
            Response dictionary with answer and metadata
        """
        logger.info(f"Processing question: {question[:50]}...")
        
        try:
            # Prepare system message
            system_message = "You are a helpful assistant that answers questions about business reports and documents. Provide accurate, detailed answers based on the available information."
            
            # Prepare user message
            if include_context:
                context = self._get_relevant_context(question)
                user_message = f"{context}\n\nQuestion: {question}\n\nPlease answer based on the information provided above."
            else:
                user_message = question
            
            # Call GPT-4
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            # Prepare response
            result = {
                "question": question,
                "answer": answer,
                "model": self.model,
                "tokens_used": tokens_used,
                "timestamp": datetime.now().isoformat(),
                "context_included": include_context
            }
            
            logger.info(f"Generated answer using {tokens_used} tokens")
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return {
                "question": question,
                "answer": f"Sorry, I encountered an error while processing your question: {str(e)}",
                "model": self.model,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def batch_questions(self, questions: List[str]) -> List[Dict]:
        """
        Process multiple questions in batch
        
        Args:
            questions: List of questions
            
        Returns:
            List of response dictionaries
        """
        logger.info(f"Processing {len(questions)} questions in batch")
        
        results = []
        for i, question in enumerate(questions, 1):
            logger.info(f"Processing question {i}/{len(questions)}")
            result = self.ask_question(question)
            results.append(result)
        
        return results
    
    def save_conversation(self, conversation: List[Dict], filename: Optional[str] = None) -> str:
        """
        Save conversation to file
        
        Args:
            conversation: List of Q&A pairs
            filename: Optional filename
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qa_conversation_{timestamp}.json"
        
        file_path = self.output_dir / filename
        
        conversation_data = {
            "conversation": conversation,
            "model": self.model,
            "total_questions": len(conversation),
            "total_tokens": sum(qa.get('tokens_used', 0) for qa in conversation),
            "created_at": datetime.now().isoformat()
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, indent=2)
        
        logger.info(f"Conversation saved to: {file_path}")
        return str(file_path)
    
    def get_system_stats(self) -> Dict:
        """
        Get system statistics
        
        Returns:
            System statistics dictionary
        """
        stats = {
            "model": self.model,
            "training_data_qa_pairs": len(self.training_data.get('qa_pairs', [])),
            "training_data_documents": self.training_data.get('total_documents', 0),
            "training_data_pages": self.training_data.get('total_pages', 0),
            "training_data_tables": self.training_data.get('total_tables', 0),
            "api_key_set": bool(self.api_key),
            "output_directory": str(self.output_dir)
        }
        
        return stats
    
    def interactive_mode(self):
        """
        Start interactive Q&A mode
        """
        print(f"\n🤖 Q&A System Interactive Mode")
        print(f"Model: {self.model}")
        print(f"Training Data: {len(self.training_data.get('qa_pairs', []))} Q&A pairs")
        print("=" * 60)
        print("Type 'quit' to exit, 'stats' for system info")
        print("=" * 60)
        
        conversation = []
        
        while True:
            try:
                question = input("\n❓ Your question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    break
                elif question.lower() == 'stats':
                    stats = self.get_system_stats()
                    print(f"\n📊 System Stats:")
                    for key, value in stats.items():
                        print(f"   {key}: {value}")
                    continue
                elif not question:
                    continue
                
                # Get answer
                print("🤔 Thinking...")
                result = self.ask_question(question)
                conversation.append(result)
                
                # Display answer
                print(f"\n💡 Answer:")
                print(f"{result['answer']}")
                print(f"\n📊 Tokens used: {result.get('tokens_used', 'N/A')}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
        
        # Save conversation
        if conversation:
            save = input(f"\n💾 Save conversation? (y/n): ").lower()
            if save in ['y', 'yes']:
                filename = input("📁 Filename (optional): ").strip()
                if not filename:
                    filename = None
                file_path = self.save_conversation(conversation, filename)
                print(f"✅ Conversation saved to: {file_path}")
        
        print("👋 Interactive mode ended")
