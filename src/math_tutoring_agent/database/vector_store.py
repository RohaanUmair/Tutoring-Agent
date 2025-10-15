import chromadb
import uuid
import json
import os
from typing import List, Dict, Optional
from datetime import datetime

class PastPaperVectorDB:
    def __init__(self, persist_directory="./vector_db/past_papers"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="past_papers",
            metadata={"description": "Storage for past papers and questions"}
        )
        self.metadata_file = os.path.join(persist_directory, "paper_metadata.json")
        self._load_metadata()
    
    def _load_metadata(self):
        """Load paper metadata"""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                self.paper_metadata = json.load(f)
        else:
            self.paper_metadata = {}
    
    def _save_metadata(self):
        """Save paper metadata"""
        os.makedirs(os.path.dirname(self.metadata_file), exist_ok=True)
        with open(self.metadata_file, 'w') as f:
            json.dump(self.paper_metadata, f, indent=2)
    
    def add_paper(self, paper_data: Dict, paper_id: str = None):
        """Add a complete past paper to vector DB"""
        if paper_id is None:
            paper_id = str(uuid.uuid4())
        
        # Store paper metadata
        self.paper_metadata[paper_id] = {
            "year": paper_data.get("year"),
            "class_level": paper_data.get("class_level", "9"),
            "subject": paper_data.get("subject", "math"),
            "total_marks": paper_data.get("total_marks"),
            "upload_time": datetime.now().isoformat(),
            "sections": {}
        }
        
        # Add each question to vector DB
        for section, questions in paper_data.get("sections", {}).items():
            self.paper_metadata[paper_id]["sections"][section] = len(questions)
            
            for i, question in enumerate(questions):
                question_id = f"{paper_id}_{section}_{i}"
                
                metadata = {
                    "paper_id": paper_id,
                    "section": section,
                    "question_type": question.get("question_type", "unknown"),
                    "topic": question.get("topic", "unknown"),
                    "marks": question.get("marks", 1),
                    "year": paper_data.get("year"),
                    "class_level": paper_data.get("class_level", "9"),
                    "difficulty": question.get("difficulty", "medium"),
                    "question_text": question.get("question_text", "")[:100]  # First 100 chars
                }
                
                self.collection.add(
                    documents=[question.get("question_text", "")],
                    metadatas=[metadata],
                    ids=[question_id]
                )
        
        self._save_metadata()
        print(f"✅ Paper {paper_id} added with {sum(len(q) for q in paper_data.get('sections', {}).values())} questions")
    
    def get_all_questions(self, filters: Dict = None) -> List[Dict]:
        """Get all questions with optional filters"""
        where_clause = {}
        if filters:
            where_clause = filters
        
        results = self.collection.get(where=where_clause)
        return self._format_results(results)
    
    def get_questions_by_section(self, section: str) -> List[Dict]:
        """Get all questions from a specific section"""
        return self.get_all_questions({"section": section})
    
    def get_questions_by_topic(self, topic: str) -> List[Dict]:
        """Get all questions from a specific topic"""
        return self.get_all_questions({"topic": topic})
    
    def search_similar_questions(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for similar questions using semantic search"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return self._format_results(results)
    
    def _format_results(self, results) -> List[Dict]:
        """Format chromaDB results into readable format"""
        formatted = []
        for doc, metadata in zip(results['documents'], results['metadatas']):
            formatted.append({
                "question_text": doc,
                "section": metadata.get("section"),
                "question_type": metadata.get("question_type"),
                "topic": metadata.get("topic"),
                "marks": metadata.get("marks"),
                "year": metadata.get("year"),
                "difficulty": metadata.get("difficulty"),
                "paper_id": metadata.get("paper_id")
            })
        return formatted
    
    def get_statistics(self) -> Dict:
        """Get statistics about stored papers"""
        all_questions = self.get_all_questions()
        
        stats = {
            "total_papers": len(self.paper_metadata),
            "total_questions": len(all_questions),
            "papers_by_year": {},
            "questions_by_section": {},
            "questions_by_topic": {},
            "topics_frequency": {}
        }
        
        # Count by year
        for paper_id, meta in self.paper_metadata.items():
            year = meta.get("year", "unknown")
            stats["papers_by_year"][year] = stats["papers_by_year"].get(year, 0) + 1
        
        # Count by section and topic
        for question in all_questions:
            section = question.get("section", "unknown")
            topic = question.get("topic", "unknown")
            
            stats["questions_by_section"][section] = stats["questions_by_section"].get(section, 0) + 1
            stats["questions_by_topic"][topic] = stats["questions_by_topic"].get(topic, 0) + 1
        
        # Calculate topic frequency
        total_questions = len(all_questions)
        for topic, count in stats["questions_by_topic"].items():
            stats["topics_frequency"][topic] = round((count / total_questions) * 100, 2)
        
        return stats