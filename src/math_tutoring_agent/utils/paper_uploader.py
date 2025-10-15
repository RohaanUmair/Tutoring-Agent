import json
import os
from typing import Dict, List

class PaperUploader:
    def __init__(self, vector_db):
        self.vector_db = vector_db
    
    def upload_paper_from_json(self, json_file_path: str):
        """Upload paper from JSON file"""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                paper_data = json.load(f)
            
            self.vector_db.add_paper(paper_data)
            print(f"✅ Paper uploaded successfully from {json_file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error uploading paper: {e}")
            return False
    
    def upload_multiple_papers(self, folder_path: str):
        """Upload all papers from a folder"""
        if not os.path.exists(folder_path):
            print(f"❌ Folder not found: {folder_path}")
            return
        
        json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
        
        for json_file in json_files:
            file_path = os.path.join(folder_path, json_file)
            self.upload_paper_from_json(file_path)
    
    def create_sample_paper_template(self, year: int, class_level: str = "9") -> Dict:
        """Create a template for paper data structure"""
        return {
            "year": year,
            "class_level": class_level,
            "subject": "math",
            "total_marks": 75,
            "time_duration": "3 hours",
            "sections": {
                "A": [],  # Will contain MCQs
                "B": [],  # Will contain short answer questions
                "C": []   # Will contain detailed answer questions
            }
        }
    
    def add_question_to_template(self, template: Dict, question_text: str, section: str, 
                               topic: str, marks: int, question_type: str = None):
        """Add a question to paper template"""
        if section not in template["sections"]:
            template["sections"][section] = []
        
        if question_type is None:
            question_type = self._infer_question_type(section, marks)
        
        question_data = {
            "question_text": question_text,
            "topic": topic,
            "marks": marks,
            "question_type": question_type,
            "difficulty": "medium"  # Can be enhanced
        }
        
        template["sections"][section].append(question_data)
    
    def _infer_question_type(self, section: str, marks: int) -> str:
        """Infer question type based on section and marks"""
        if section == "A" or marks == 1:
            return "mcq"
        elif section == "B" or marks <= 5:
            return "short_answer"
        else:
            return "detailed_answer"