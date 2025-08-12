"""
Report Processor Module
======================

This module handles extracting structured data from documents
and creating training datasets for AI fine-tuning.

Author: Report GPT Team
Date: 2024
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportProcessor:
    """
    Report Processor Class
    
    Extracts structured data from documents and creates
    training datasets for AI fine-tuning.
    """
    
    def __init__(self, output_dir: str = "data/output"):
        """
        Initialize Report Processor
        
        Args:
            output_dir (str): Directory to save processed data
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Common report patterns
        self.section_patterns = {
            'executive_summary': r'(executive\s+summary|summary|overview)',
            'introduction': r'(introduction|background|context)',
            'methodology': r'(methodology|methods|approach)',
            'results': r'(results|findings|analysis)',
            'conclusion': r'(conclusion|conclusions|summary)',
            'recommendations': r'(recommendations|suggestions|next\s+steps)'
        }
        
        # Key metrics patterns
        self.metrics_patterns = {
            'percentage': r'(\d+(?:\.\d+)?\s*%)',
            'currency': r'(\$[\d,]+(?:\.\d{2})?)',
            'numbers': r'(\d+(?:,\d{3})*(?:\.\d+)?)',
            'dates': r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})'
        }
    
    def extract_sections(self, text_content: List[Dict]) -> Dict:
        """
        Extract report sections from text content
        
        Args:
            text_content (List[Dict]): List of text content with page numbers
            
        Returns:
            Dict: Extracted sections
        """
        try:
            # Combine all text
            full_text = ' '.join([item['text'] for item in text_content])
            
            sections = {}
            
            # Extract sections based on patterns
            for section_name, pattern in self.section_patterns.items():
                matches = re.finditer(pattern, full_text, re.IGNORECASE)
                for match in matches:
                    start_pos = match.start()
                    # Extract text around the section
                    section_start = max(0, start_pos - 100)
                    section_end = min(len(full_text), start_pos + 1000)
                    section_text = full_text[section_start:section_end]
                    
                    if section_name not in sections:
                        sections[section_name] = []
                    
                    sections[section_name].append({
                        'text': section_text.strip(),
                        'position': start_pos
                    })
            
            return sections
            
        except Exception as e:
            logger.error(f"Error extracting sections: {e}")
            return {}
    
    def extract_metrics(self, text_content: List[Dict]) -> Dict:
        """
        Extract key metrics from text content
        
        Args:
            text_content (List[Dict]): List of text content
            
        Returns:
            Dict: Extracted metrics
        """
        try:
            # Combine all text
            full_text = ' '.join([item['text'] for item in text_content])
            
            metrics = {}
            
            # Extract metrics based on patterns
            for metric_type, pattern in self.metrics_patterns.items():
                matches = re.findall(pattern, full_text)
                if matches:
                    metrics[metric_type] = list(set(matches))  # Remove duplicates
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error extracting metrics: {e}")
            return {}
    
    def create_qa_pairs(self, text_content: List[Dict], tables: List[Dict]) -> List[Dict]:
        """
        Create Q&A pairs from document content
        
        Args:
            text_content (List[Dict]): Text content
            tables (List[Dict]): Table data
            
        Returns:
            List[Dict]: Q&A pairs
        """
        try:
            qa_pairs = []
            
            # Combine all text
            full_text = ' '.join([item['text'] for item in text_content])
            
            # Create basic Q&A pairs
            basic_questions = [
                "What is the main topic of this document?",
                "What are the key findings?",
                "What are the main conclusions?",
                "What recommendations are provided?",
                "What methodology was used?"
            ]
            
            # For now, we'll create simple Q&A pairs
            # In a real implementation, you'd use more sophisticated NLP
            for question in basic_questions:
                qa_pairs.append({
                    'question': question,
                    'answer': f"Based on the document content: {full_text[:200]}...",
                    'source': 'document_analysis',
                    'confidence': 0.8
                })
            
            # Add table-based Q&A pairs
            for table in tables:
                if table['data'] and len(table['data']) > 1:
                    # Create questions about table data
                    table_qa = self._create_table_qa(table)
                    qa_pairs.extend(table_qa)
            
            return qa_pairs
            
        except Exception as e:
            logger.error(f"Error creating Q&A pairs: {e}")
            return []
    
    def _create_table_qa(self, table: Dict) -> List[Dict]:
        """
        Create Q&A pairs from table data
        
        Args:
            table (Dict): Table data
            
        Returns:
            List[Dict]: Table-based Q&A pairs
        """
        try:
            qa_pairs = []
            table_data = table['data']
            
            if not table_data or len(table_data) < 2:
                return qa_pairs
            
            # Extract headers
            headers = table_data[0] if table_data else []
            
            # Create questions about table structure
            if headers:
                # Filter out None values from headers
                clean_headers = [str(h) for h in headers if h is not None]
                if clean_headers:
                    qa_pairs.append({
                        'question': f"What are the columns in the table on page {table['page']}?",
                        'answer': f"The table has the following columns: {', '.join(clean_headers)}",
                        'source': 'table_analysis',
                        'confidence': 0.9
                    })
            
            # Create questions about data
            if len(table_data) > 1:
                qa_pairs.append({
                    'question': f"How many rows are in the table on page {table['page']}?",
                    'answer': f"The table has {len(table_data) - 1} data rows.",
                    'source': 'table_analysis',
                    'confidence': 0.95
                })
            
            return qa_pairs
            
        except Exception as e:
            logger.error(f"Error creating table Q&A pairs: {e}")
            return []
    
    def process_document(self, document_data: Dict) -> Dict:
        """
        Process a single document and extract structured data
        
        Args:
            document_data (Dict): Document data from file reader
            
        Returns:
            Dict: Processed document data
        """
        try:
            logger.info(f"Processing document: {document_data.get('file_path', 'Unknown')}")
            
            text_content = document_data.get('text', [])
            tables = document_data.get('tables', [])
            
            # Extract sections
            sections = self.extract_sections(text_content)
            
            # Extract metrics
            metrics = self.extract_metrics(text_content)
            
            # Create Q&A pairs
            qa_pairs = self.create_qa_pairs(text_content, tables)
            
            # Create structured output
            processed_data = {
                'file_path': document_data.get('file_path', ''),
                'processing_timestamp': datetime.now().isoformat(),
                'sections': sections,
                'metrics': metrics,
                'qa_pairs': qa_pairs,
                'tables': tables,
                'text_summary': {
                    'total_pages': len(text_content),
                    'total_tables': len(tables),
                    'total_qa_pairs': len(qa_pairs)
                }
            }
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            return {}
    
    def save_processed_data(self, processed_data: Dict, filename: str = None) -> str:
        """
        Save processed data to JSON file
        
        Args:
            processed_data (Dict): Processed document data
            filename (str, optional): Custom filename
            
        Returns:
            str: Path to saved file
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"processed_data_{timestamp}.json"
            
            file_path = self.output_dir / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Processed data saved to: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Error saving processed data: {e}")
            raise
    
    def create_training_dataset(self, processed_documents: List[Dict]) -> Dict:
        """
        Create training dataset from processed documents
        
        Args:
            processed_documents (List[Dict]): List of processed documents
            
        Returns:
            Dict: Training dataset
        """
        try:
            training_data = {
                'metadata': {
                    'created_at': datetime.now().isoformat(),
                    'total_documents': len(processed_documents),
                    'total_qa_pairs': 0,
                    'version': '1.0'
                },
                'qa_pairs': [],
                'documents': []
            }
            
            for doc in processed_documents:
                # Add Q&A pairs
                qa_pairs = doc.get('qa_pairs', [])
                training_data['qa_pairs'].extend(qa_pairs)
                training_data['metadata']['total_qa_pairs'] += len(qa_pairs)
                
                # Add document summary
                training_data['documents'].append({
                    'file_path': doc.get('file_path', ''),
                    'sections': list(doc.get('sections', {}).keys()),
                    'metrics_count': len(doc.get('metrics', {})),
                    'qa_pairs_count': len(qa_pairs)
                })
            
            return training_data
            
        except Exception as e:
            logger.error(f"Error creating training dataset: {e}")
            return {}
