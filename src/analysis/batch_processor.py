"""Batch Processing Module"""

import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


class BatchProcessor:
    """Process multiple audio files in batch"""
    
    def __init__(self, max_workers: int = 4):
        """
        Initialize batch processor
        
        Args:
            max_workers: Maximum number of parallel processing threads
        """
        self.max_workers = max_workers
        self.results = []
        self.errors = []
    
    def process_directory(self, directory: Path, file_pattern: str = "*.wav",
                         process_func=None, recursive: bool = False) -> Dict:
        """
        Process all files in directory
        
        Args:
            directory: Directory path
            file_pattern: File glob pattern
            process_func: Function to process each file
            recursive: Search recursively in subdirectories
            
        Returns:
            Processing results
        """
        directory = Path(directory)
        
        # Find files
        if recursive:
            files = list(directory.rglob(file_pattern))
        else:
            files = list(directory.glob(file_pattern))
        
        logger.info(f"Found {len(files)} files to process")
        
        self.results = []
        self.errors = []
        
        # Process files
        if process_func:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {executor.submit(process_func, f): f for f in files}
                
                for future in as_completed(futures):
                    file = futures[future]
                    try:
                        result = future.result()
                        self.results.append({
                            'file': file.name,
                            'result': result,
                            'status': 'success'
                        })
                        logger.info(f"Processed: {file.name}")
                    except Exception as e:
                        self.errors.append({
                            'file': file.name,
                            'error': str(e)
                        })
                        logger.error(f"Error processing {file.name}: {e}")
        
        return {
            'total_files': len(files),
            'successful': len(self.results),
            'failed': len(self.errors),
            'results': self.results,
            'errors': self.errors
        }
    
    def get_results_summary(self) -> Dict:
        """
        Get summary of batch processing results
        
        Returns:
            Summary dictionary
        """
        return {
            'total_processed': len(self.results),
            'total_errors': len(self.errors),
            'success_rate': len(self.results) / (len(self.results) + len(self.errors)) * 100 if (len(self.results) + len(self.errors)) > 0 else 0,
            'results': self.results,
            'errors': self.errors
        }


if __name__ == "__main__":
    print("Batch Processor module loaded")
