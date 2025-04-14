from typing import List, Dict
import tiktoken
import os
import pandas as pd
import docx
from pypdf import PdfReader
import config  # Import the config module

class AdvancedFileProcessor:
    def __init__(self):
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.chunk_size = config.CHUNK_SIZE
        self.chunk_overlap = config.CHUNK_OVERLAP
        
    def process_file(self, file_path: str) -> List[Dict]:
        """Process any supported file type with configurable chunking"""
        try:
            file_path = os.path.normpath(file_path)
            
            if file_path.endswith('.pdf'):
                full_text = self._extract_pdf_text(file_path)
            elif file_path.endswith('.docx'):
                full_text = self._extract_docx_text(file_path)
            elif file_path.endswith(('.csv', '.xlsx', '.xls', '.xlsm')):
                full_text = self._extract_spreadsheet_text(file_path)
            else:
                print(f"Unsupported file type: {file_path}")
                return []
            
            if not full_text:
                return []
                
            return self._chunk_text(full_text, os.path.basename(file_path))
            
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return []

    def _chunk_text(self, text: str, source: str) -> List[Dict]:
        """Split text into chunks with overlap using configurable sizes"""
        tokens = self.tokenizer.encode(text)
        chunks = []
        start = 0
        
        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            
            chunks.append({
                'text': chunk_text,
                'source': source,
                'chunk_num': len(chunks) + 1,
                'page': 1,  # Default page number
                'token_count': len(chunk_tokens),
                'is_table': False  # Explicit default
            })
            
            start += (self.chunk_size - self.chunk_overlap)
            if start == end:  # Prevent infinite loop
                start += 1
                
        return chunks

    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract all text from PDF with page markers"""
        try:
            reader = PdfReader(file_path)
            return "\n".join(
                f"PAGE {i+1}:\n{page.extract_text()}" 
                for i, page in enumerate(reader.pages) 
                if page.extract_text()
            )
        except Exception as e:
            print(f"PDF extraction error: {str(e)}")
            return ""

    def _extract_docx_text(self, file_path: str) -> str:
        """Extract all text from Word document"""
        try:
            doc = docx.Document(file_path)
            text = "\n".join(para.text for para in doc.paragraphs if para.text.strip())
            
            if doc.tables:
                text += "\n\nTABLES:\n" + "\n".join(
                    " | ".join(cell.text for cell in row.cells)
                    for table in doc.tables
                    for row in table.rows
                )
            return text
        except Exception as e:
            print(f"DOCX extraction error: {str(e)}")
            return ""

    def _extract_spreadsheet_text(self, file_path: str) -> str:
        """Extract all text from spreadsheet"""
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            
            # Mark tables explicitly
            table_text = df.to_string()
            return f"TABLE:\n{table_text}"
        except Exception as e:
            print(f"Spreadsheet extraction error: {str(e)}")
            return ""