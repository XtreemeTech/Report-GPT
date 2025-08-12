"""
Report Generator Module
======================

This module generates structured reports from document data
and Q&A responses using GPT-4.

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


class ReportGenerator:
    """
    Report Generator Class
    
    Generates structured reports from document data and Q&A responses.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize Report Generator
        
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
        
        logger.info(f"Report Generator initialized with model: {model}")
    
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
    
    def _load_extracted_data(self) -> Dict:
        """
        Load extracted document data
        
        Returns:
            Extracted data dictionary
        """
        try:
            extracted_file = self.output_dir / "extracted_data.json"
            if extracted_file.exists():
                with open(extracted_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.info(f"Loaded extracted data with {len(data.get('documents', []))} documents")
                return data
            else:
                logger.warning("Extracted data not found")
                return {"documents": []}
        except Exception as e:
            logger.error(f"Error loading extracted data: {e}")
            return {"documents": []}
    
    def generate_executive_summary(self, max_length: int = 1000) -> Dict:
        """
        Generate executive summary report
        
        Args:
            max_length: Maximum length of summary
            
        Returns:
            Executive summary report
        """
        logger.info("Generating executive summary report")
        
        try:
            # Prepare context from training data
            context = self._prepare_summary_context()
            
            # Generate executive summary using GPT-4
            system_message = """You are a professional report writer. Create a concise executive summary based on the provided document information. Focus on key findings, main topics, and important insights."""
            
            user_message = f"""Based on the following document information, create a professional executive summary (maximum {max_length} words):

{context}

Please structure the summary with:
1. Main Topic/Subject
2. Key Findings
3. Important Insights
4. Document Overview

Make it professional and business-ready."""

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            # Create report structure
            report = {
                "type": "executive_summary",
                "title": "Executive Summary Report",
                "content": summary,
                "generated_at": datetime.now().isoformat(),
                "model": self.model,
                "tokens_used": tokens_used,
                "max_length": max_length,
                "document_count": len(self.training_data.get('qa_pairs', [])),
                "word_count": len(summary.split())
            }
            
            logger.info(f"Generated executive summary with {tokens_used} tokens")
            return report
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            return {
                "type": "executive_summary",
                "error": str(e),
                "generated_at": datetime.now().isoformat()
            }
    
    def generate_key_findings_report(self) -> Dict:
        """
        Generate key findings report
        
        Returns:
            Key findings report
        """
        logger.info("Generating key findings report")
        
        try:
            # Prepare context from training data
            context = self._prepare_findings_context()
            
            # Generate key findings using GPT-4
            system_message = """You are a professional analyst. Extract and organize key findings from the provided document information. Focus on important discoveries, data points, and significant insights."""
            
            user_message = f"""Based on the following document information, create a comprehensive key findings report:

{context}

Please structure the findings with:
1. Primary Findings
2. Data Insights
3. Important Metrics
4. Significant Discoveries
5. Key Takeaways

Make it detailed and analytical."""

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            findings = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            # Create report structure
            report = {
                "type": "key_findings",
                "title": "Key Findings Report",
                "content": findings,
                "generated_at": datetime.now().isoformat(),
                "model": self.model,
                "tokens_used": tokens_used,
                "document_count": len(self.training_data.get('qa_pairs', [])),
                "word_count": len(findings.split())
            }
            
            logger.info(f"Generated key findings report with {tokens_used} tokens")
            return report
            
        except Exception as e:
            logger.error(f"Error generating key findings report: {e}")
            return {
                "type": "key_findings",
                "error": str(e),
                "generated_at": datetime.now().isoformat()
            }
    
    def generate_recommendations_report(self) -> Dict:
        """
        Generate recommendations report
        
        Returns:
            Recommendations report
        """
        logger.info("Generating recommendations report")
        
        try:
            # Prepare context from training data
            context = self._prepare_recommendations_context()
            
            # Generate recommendations using GPT-4
            system_message = """You are a strategic consultant. Based on the provided document information, generate actionable recommendations and strategic insights."""
            
            user_message = f"""Based on the following document information, create a strategic recommendations report:

{context}

Please structure the recommendations with:
1. Strategic Recommendations
2. Action Items
3. Implementation Steps
4. Priority Levels
5. Expected Outcomes

Make it actionable and strategic."""

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            recommendations = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            # Create report structure
            report = {
                "type": "recommendations",
                "title": "Strategic Recommendations Report",
                "content": recommendations,
                "generated_at": datetime.now().isoformat(),
                "model": self.model,
                "tokens_used": tokens_used,
                "document_count": len(self.training_data.get('qa_pairs', [])),
                "word_count": len(recommendations.split())
            }
            
            logger.info(f"Generated recommendations report with {tokens_used} tokens")
            return report
            
        except Exception as e:
            logger.error(f"Error generating recommendations report: {e}")
            return {
                "type": "recommendations",
                "error": str(e),
                "generated_at": datetime.now().isoformat()
            }
    
    def _prepare_summary_context(self) -> str:
        """
        Prepare context for summary generation
        
        Returns:
            Context string
        """
        if not self.training_data.get('qa_pairs'):
            return "No document data available for summary generation."
        
        # Get relevant Q&A pairs for summary
        relevant_pairs = []
        for qa_pair in self.training_data['qa_pairs'][:10]:  # Use first 10 for summary
            if 'main topic' in qa_pair.get('question', '').lower() or \
               'key finding' in qa_pair.get('question', '').lower() or \
               'overview' in qa_pair.get('question', '').lower():
                relevant_pairs.append(qa_pair)
        
        # Build context
        context = "Document Information:\n\n"
        for i, pair in enumerate(relevant_pairs, 1):
            context += f"{i}. Q: {pair.get('question', '')}\n   A: {pair.get('answer', '')}\n\n"
        
        return context
    
    def _prepare_findings_context(self) -> str:
        """
        Prepare context for findings generation
        
        Returns:
            Context string
        """
        if not self.training_data.get('qa_pairs'):
            return "No document data available for findings generation."
        
        # Get relevant Q&A pairs for findings
        relevant_pairs = []
        for qa_pair in self.training_data['qa_pairs']:
            if 'finding' in qa_pair.get('question', '').lower() or \
               'result' in qa_pair.get('question', '').lower() or \
               'data' in qa_pair.get('question', '').lower() or \
               'analysis' in qa_pair.get('question', '').lower():
                relevant_pairs.append(qa_pair)
        
        # Build context
        context = "Document Findings:\n\n"
        for i, pair in enumerate(relevant_pairs[:15], 1):  # Use up to 15 for findings
            context += f"{i}. Q: {pair.get('question', '')}\n   A: {pair.get('answer', '')}\n\n"
        
        return context
    
    def _prepare_recommendations_context(self) -> str:
        """
        Prepare context for recommendations generation
        
        Returns:
            Context string
        """
        if not self.training_data.get('qa_pairs'):
            return "No document data available for recommendations generation."
        
        # Get relevant Q&A pairs for recommendations
        relevant_pairs = []
        for qa_pair in self.training_data['qa_pairs']:
            if 'recommendation' in qa_pair.get('question', '').lower() or \
               'suggestion' in qa_pair.get('question', '').lower() or \
               'action' in qa_pair.get('question', '').lower() or \
               'strategy' in qa_pair.get('question', '').lower():
                relevant_pairs.append(qa_pair)
        
        # Build context
        context = "Document Analysis for Recommendations:\n\n"
        for i, pair in enumerate(relevant_pairs[:15], 1):  # Use up to 15 for recommendations
            context += f"{i}. Q: {pair.get('question', '')}\n   A: {pair.get('answer', '')}\n\n"
        
        return context
    
    def generate_comprehensive_report(self) -> Dict:
        """
        Generate comprehensive report with all sections
        
        Returns:
            Comprehensive report
        """
        logger.info("Generating comprehensive report")
        
        try:
            # Generate all report sections
            executive_summary = self.generate_executive_summary()
            key_findings = self.generate_key_findings_report()
            recommendations = self.generate_recommendations_report()
            
            # Combine into comprehensive report
            comprehensive_report = {
                "type": "comprehensive",
                "title": "Comprehensive Document Analysis Report",
                "generated_at": datetime.now().isoformat(),
                "model": self.model,
                "sections": {
                    "executive_summary": executive_summary,
                    "key_findings": key_findings,
                    "recommendations": recommendations
                },
                "total_tokens": (
                    executive_summary.get('tokens_used', 0) +
                    key_findings.get('tokens_used', 0) +
                    recommendations.get('tokens_used', 0)
                ),
                "document_count": len(self.training_data.get('qa_pairs', [])),
                "total_word_count": (
                    executive_summary.get('word_count', 0) +
                    key_findings.get('word_count', 0) +
                    recommendations.get('word_count', 0)
                )
            }
            
            logger.info("Generated comprehensive report successfully")
            return comprehensive_report
            
        except Exception as e:
            logger.error(f"Error generating comprehensive report: {e}")
            return {
                "type": "comprehensive",
                "error": str(e),
                "generated_at": datetime.now().isoformat()
            }
    
    def save_report(self, report: Dict, filename: Optional[str] = None) -> str:
        """
        Save report to file
        
        Args:
            report: Report dictionary
            filename: Optional filename
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_type = report.get('type', 'report')
            filename = f"{report_type}_report_{timestamp}.json"
        
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report saved to: {file_path}")
        return str(file_path)
    
    def get_report_stats(self) -> Dict:
        """
        Get report generation statistics
        
        Returns:
            Statistics dictionary
        """
        stats = {
            "model": self.model,
            "training_data_qa_pairs": len(self.training_data.get('qa_pairs', [])),
            "extracted_documents": len(self._load_extracted_data().get('documents', [])),
            "api_key_set": bool(self.api_key),
            "output_directory": str(self.output_dir)
        }
        
        return stats
