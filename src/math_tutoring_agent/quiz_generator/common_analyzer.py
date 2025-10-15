from collections import Counter, defaultdict
import re
from typing import List, Dict, Tuple

class CommonQuestionAnalyzer:
    def __init__(self, vector_db):
        self.vector_db = vector_db
    
    def analyze_common_questions(self, min_years: int = 2) -> Dict:
        """Find questions that appear across multiple years"""
        print("🔍 Analyzing common questions across years...")
        
        all_questions = self.vector_db.get_all_questions()
        
        # Group by topic and find common patterns
        topic_groups = self._group_questions_by_topic(all_questions)
        common_questions = self._find_common_by_similarity(topic_groups)
        
        # Organize by section
        organized = self._organize_by_section(common_questions)
        
        print(f"📊 Found {len(common_questions)} common question patterns")
        return organized
    
    def _group_questions_by_topic(self, questions: List[Dict]) -> Dict:
        """Group questions by topic and find patterns"""
        topic_groups = defaultdict(list)
        
        for q in questions:
            topic = q.get("topic", "unknown")
            topic_groups[topic].append(q)
        
        return topic_groups
    
    def _find_common_by_similarity(self, topic_groups: Dict) -> List[Dict]:
        """Find common questions using text similarity and patterns"""
        common_questions = []
        
        for topic, questions in topic_groups.items():
            if len(questions) < 2:
                continue
            
            # Group by question type pattern
            type_groups = defaultdict(list)
            for q in questions:
                q_type = self._classify_question_type(q["question_text"])
                type_groups[q_type].append(q)
            
            # Find common patterns in each type group
            for q_type, type_questions in type_groups.items():
                if len(type_questions) >= 2:
                    # Use simple frequency analysis
                    common_patterns = self._extract_common_patterns(type_questions)
                    common_questions.extend(common_patterns)
        
        return common_questions
    
    def _classify_question_type(self, question_text: str) -> str:
        """Classify question type based on text patterns"""
        text = question_text.lower()
        
        if any(word in text for word in ['choose', 'correct', 'option', 'multiple', 'mcq', 'select']):
            return "mcq"
        elif any(word in text for word in ['prove', 'theorem', 'construct', 'show that']):
            return "proof"
        elif any(word in text for word in ['solve', 'find', 'calculate', 'value']):
            if len(text) < 100:  # Short questions
                return "short_answer"
            else:
                return "detailed_answer"
        elif any(word in text for word in ['factor', 'expand', 'simplify']):
            return "algebraic_manipulation"
        else:
            return "general"
    
    def _extract_common_patterns(self, questions: List[Dict]) -> List[Dict]:
        """Extract common question patterns"""
        patterns = []
        
        # Group by year and find cross-year patterns
        year_groups = defaultdict(list)
        for q in questions:
            year = q.get("year", "unknown")
            year_groups[year].append(q)
        
        # Find questions that have similar patterns across years
        if len(year_groups) >= 2:  # Appears in at least 2 different years
            # Take the most representative question from each topic
            representative = self._get_representative_question(questions)
            if representative:
                patterns.append(representative)
        
        return patterns
    
    def _get_representative_question(self, questions: List[Dict]) -> Dict:
        """Get the most representative question from a group"""
        if not questions:
            return None
        
        # Use the question with highest marks (usually more important)
        questions_sorted = sorted(questions, key=lambda x: x.get("marks", 0), reverse=True)
        representative = questions_sorted[0]
        
        # Add frequency information
        representative["frequency"] = len(questions)
        representative["appears_in_years"] = list(set(q.get("year") for q in questions))
        
        return representative
    
    def _organize_by_section(self, common_questions: List[Dict]) -> Dict:
        """Organize common questions by exam sections"""
        organized = {
            "section_a": [],  # MCQs
            "section_b": [],  # Short Answer
            "section_c": []   # Detailed Answer
        }
        
        for question in common_questions:
            question_type = question.get("question_type", "").lower()
            marks = question.get("marks", 1)
            
            if question_type == "mcq" or marks == 1:
                organized["section_a"].append(question)
            elif marks <= 5:  # Short answer typically 5 marks
                organized["section_b"].append(question)
            else:  # Detailed answer typically 10 marks
                organized["section_c"].append(question)
        
        return organized
    
    def get_topic_frequency_report(self) -> Dict:
        """Generate topic frequency report using probability statistics"""
        stats = self.vector_db.get_statistics()
        all_questions = self.vector_db.get_all_questions()
        
        # Calculate probability of each topic appearing
        topic_probability = {}
        total_questions = len(all_questions)
        
        for topic, count in stats["questions_by_topic"].items():
            probability = count / total_questions
            topic_probability[topic] = {
                "frequency": count,
                "probability": round(probability, 4),
                "percentage": stats["topics_frequency"].get(topic, 0)
            }
        
        # Sort by probability (descending)
        sorted_probability = dict(sorted(
            topic_probability.items(), 
            key=lambda x: x[1]["probability"], 
            reverse=True
        ))
        
        return {
            "topic_probabilities": sorted_probability,
            "recommended_topics": list(sorted_probability.keys())[:8],  # Top 8 topics
            "analysis_date": str(datetime.now())
        }