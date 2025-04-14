from typing import List, Dict, Optional

class TableProcessor:
    def process_table(self, table) -> str:
        """Convert table to structured text representation"""
        table_data = []
        
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                row_data.append(cell.text.strip())
            table_data.append(row_data)
        
        # Convert to markdown-like format
        markdown = []
        headers = table_data[0]
        markdown.append("| " + " | ".join(headers) + " |")
        markdown.append("| " + " | ".join(["---"] * len(headers)) + " |")
        
        for row in table_data[1:]:
            markdown.append("| " + " | ".join(row) + " |")
        
        return "\n".join(markdown) + "\n\nTable summary: " + self._summarize_table(table_data)
    
    def _summarize_table(self, table_data: List[List[str]]) -> str:
        """Generate a summary of the table contents"""
        if not table_data or len(table_data) < 2:
            return "Empty or single-row table"
        
        num_rows = len(table_data) - 1  # exclude header
        num_cols = len(table_data[0])
        
        sample_data = []
        for row in table_data[1:min(4, len(table_data))]:
            sample_data.append(", ".join(f"{k}:{v}" for k, v in zip(table_data[0], row)))
        
        return (f"A table with {num_rows} rows and {num_cols} columns. "
                f"Columns: {', '.join(table_data[0])}. "
                f"Sample data: {'; '.join(sample_data)}")