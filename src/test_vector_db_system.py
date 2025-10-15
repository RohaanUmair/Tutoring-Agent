import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from math_tutoring_agent.database.vector_store import PastPaperVectorDB
from math_tutoring_agent.quiz_generator.common_analyzer import CommonQuestionAnalyzer
from math_tutoring_agent.quiz_generator.complete_output_generator import OutputGenerator
from math_tutoring_agent.utils.paper_uploader import PaperUploader

def main():
    print("=== PAST PAPER ANALYSIS SYSTEM ===")
    
    # Initialize system
    vector_db = PastPaperVectorDB()
    uploader = PaperUploader(vector_db)
    analyzer = CommonQuestionAnalyzer(vector_db)
    output_gen = OutputGenerator(vector_db, analyzer)
    
    # Step 1: Upload past papers
    print("📚 Step 1: Uploading past papers...")
    uploader.upload_multiple_papers("../past_papers")  # Go one level up to find past_papers folder
    
    # Step 2: Generate analysis
    print("🔍 Step 2: Analyzing common questions...")
    output = output_gen.generate_target_paper_output()
    
    # Step 3: Save results
    output_gen.save_output_to_file(output, "../target_paper_analysis.json")
    
    print("✅ DONE! Check 'target_paper_analysis.json' for your analysis")
    
    # Show quick summary
    stats = vector_db.get_statistics()
    print(f"\n📊 Summary:")
    print(f"   - Papers analyzed: {stats['total_papers']}")
    print(f"   - Total questions: {stats['total_questions']}")
    print(f"   - Common patterns found: {output['analysis_summary']['total_common_questions']}")

if __name__ == "__main__":
    main()