import os
import json
# from openai import function_tool
# from openai.agents import Agent, Runner
# from Config.config import config


def load_past_papers():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    papers_dir = os.path.join(base_dir, "past_papers")

    files = [
        "2022_questions_maths.json",
        "2023_questions_math.json",
        "2024_questions_math.json"
    ]

    papers = []
    for file in files:
        file_path = os.path.join(papers_dir, file)
        with open(file_path, "r", encoding="utf-8") as f:
            papers.append(json.load(f))
    return papers



def MCQs(papers):
    mcqs = []
    for paper in papers:
        mcqs.extend(paper["sections"]["A"])
    return mcqs


def Short_question(papers):
    short_qs = []
    for paper in papers:
        short_qs.extend(paper["sections"]["B"])
    return short_qs





def Long_Question(papers):
    long_qs = []
    for paper in papers:
        long_qs.extend(paper["sections"]["C"])
    return long_qs

# Now you can access them like:
# print("2022 data:", past_papers["2022_questions_maths.json"])
# print("2023 data:", past_papers["2023_questions_math.json"])
# print("2024 data:", past_papers["2024_questions_math.json"])


if __name__ == "__main__":
    past_papers = load_past_papers()
    all_mcqs = MCQs(past_papers)
    print(f"Total MCQs: {all_mcqs}")