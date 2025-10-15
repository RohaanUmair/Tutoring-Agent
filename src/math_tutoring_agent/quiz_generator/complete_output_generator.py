import json
from typing import Dict, List
from datetime import datetime

class OutputGenerator:
    def __init__(self, vector_db, analyzer):
        self.vector_db = vector_db
        self.analyzer = analyzer
    
    def generate_target_paper_output(self) -> Dict:
        """Generate complete output for target paper creation"""
        print("🎯 Generating target paper analysis...")
        
        # Get common questions organized by section
        common_questions = self.analyzer.analyze_common_questions()
        
        # Get topic frequency analysis
        topic_report = self.analyzer.get_topic_frequency_report()
        
        # Generate output structure
        output = {
            "generated_at": str(datetime.now()),
            "analysis_summary": {
                "total_common_questions": sum(len(q) for q in common_questions.values()),
                "mcqs_found": len(common_questions["section_a"]),
                "short_questions_found": len(common_questions["section_b"]),
                "long_questions_found": len(common_questions["section_c"]),
                "top_topics": topic_report["recommended_topics"][:5]
            },
            "common_questions_by_section": common_questions,
            "topic_analysis": topic_report,
            "paper_structure_recommendation": self._generate_paper_structure(),
            "agent_prompts": self._generate_agent_prompts(common_questions)
        }
        
        return output
    
    def _generate_paper_structure(self) -> Dict:
        """Generate recommended paper structure"""
        return {
            "section_a": {
                "type": "MCQs",
                "count": 15,
                "marks_per_question": 1,
                "total_marks": 15,
                "recommended_topics": ["Algebra", "Logarithms", "Geometry", "Coordinate Geometry"]
            },
            "section_b": {
                "type": "Short Answer",
                "count": 6,
                "marks_per_question": 5,
                "total_marks": 30,
                "recommended_topics": ["Algebra", "Complex Numbers", "Factorization"]
            },
            "section_c": {
                "type": "Detailed Answer",
                "count": 3,
                "marks_per_question": 10,
                "total_marks": 30,
                "recommended_topics": ["Geometry Proofs", "Algebra", "Coordinate Geometry"]
            }
        }
    
    def _generate_agent_prompts(self, common_questions: Dict) -> Dict:
        """Generate prompts for AI agent to create variations"""
        prompts = {}
        
        for section, questions in common_questions.items():
            if section == "section_a":
                prompts[section] = self._create_mcq_prompt(questions)
            elif section == "section_b":
                prompts[section] = self._create_short_answer_prompt(questions)
            else:
                prompts[section] = self._create_detailed_answer_prompt(questions)
        
        return prompts
    
    def _create_mcq_prompt(self, questions: List[Dict]) -> str:
        """Create prompt for MCQ generation"""
        topic_list = list(set(q["topic"] for q in questions))
        
        prompt = f"""
        Generate 15 Multiple Choice Questions (MCQs) for mathematics based on the following analysis:
        
        Most Common Topics: {', '.join(topic_list[:5])}
        
        Sample Common MCQs Found:
        {self._format_sample_questions(questions[:3])}
        
        Requirements:
        - 15 MCQs total
        - 1 mark each
        - Cover topics: {', '.join(topic_list[:5])}
        - Include 4 options for each question
        - Mark the correct answer with [CORRECT]
        - Follow past paper pattern
        """
        return prompt
    
    def _create_short_answer_prompt(self, questions: List[Dict]) -> str:
        """Create prompt for short answer generation"""
        return f"""
        Generate 6 Short Answer Questions for mathematics based on common patterns.
        
        Common Question Types Found:
        {self._format_sample_questions(questions[:3])}
        
        Requirements:
        - 6 questions total
        - 5 marks each
        - Focus on problem-solving and calculations
        - Include step-by-step solutions
        """
    
    def _create_detailed_answer_prompt(self, questions: List[Dict]) -> str:
        """Create prompt for detailed answer generation"""
        return f"""
        Generate 3 Detailed Answer Questions for mathematics final exam.
        
        Common Detailed Questions Found:
        {self._format_sample_questions(questions[:2])}
        
        Requirements:
        - 3 questions total
        - 10 marks each
        - Include proofs, constructions, or multi-step problems
        - Provide detailed marking scheme
        """
    
    def _format_sample_questions(self, questions: List[Dict]) -> str:
        """Format sample questions for prompts"""
        if not questions:
            return "No sample questions available."
        
        formatted = []
        for i, q in enumerate(questions, 1):
            formatted.append(f"{i}. {q['question_text']} (Topic: {q['topic']}, Marks: {q['marks']})")
        
        return "\n".join(formatted)
    
    def save_output_to_file(self, output: Dict, filename: str = "target_paper_analysis.json"):
        """Save output to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"✅ Analysis saved to {filename}")