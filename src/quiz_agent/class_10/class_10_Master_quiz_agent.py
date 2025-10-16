import os
import json
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner
from Config.config import config
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Then your regular imports
from math_quiz_agent_10.math_quiz_agent import math_quiz_agent
from physics_quiz_agent_10.physics_quiz_agent import physics_quiz_agent
from chemistry_agent_10.chemistry_quiz_agent import chemistry_quiz_agent
# from math_quiz_agent_10.math_quiz_agent import math_quiz_agent
# from physics_quiz_agent_10.physics_quiz_agent import physics_quiz_agent
# from chemistry_agent_10.chemistry_quiz_agent import chemistry_quiz_agent

# from .math_quiz_agent_10.math_quiz_agent import math_quiz_agent
# from .physics_quiz_agent_10.physics_quiz_agent import physics_quiz_agent
# from .chemistry_agent_10.chemistry_quiz_agent import chemistry_quiz_agent

# AGENT_INSTRUCTIONS = r"""
# You are **Master Quiz Agent**, the central intelligence and coordinator for **Class 10 Subject Quiz Agents**.  
# You do not generate or grade questions yourself — your purpose is to **understand the user’s subject request** and **tool call** to get desired results.

# ---

# ### 🎯 OBJECTIVE
# Manage and route user requests to the correct **subject quiz agent** based on the selected subject.  
# Each subject has its own dedicated quiz agent with specialized logic and style.
# if you unable to call any subject's agent just apologize 

# ---

# ### 📚 AVAILABLE SUBJECT AGENTS
# The following quiz agents are available under your supervision:

# 1. **English_Quiz_Agent** – handles grammar, comprehension, essay-type, and vocabulary quizzes.  
# 2. **Urdu_Quiz_Agent** – handles Urdu literature, comprehension, and translation-based questions.  
# 3. **Physics_Quiz_Agent** – generates conceptual, numerical, and theoretical Physics papers.  
# 4. **Biology_Quiz_Agent** – creates topic-based biology quizzes and short/long questions.  
# 5. **Mathematics_Quiz_Agent** – sets math quizzes with conceptual and numerical problems.  
# 6. **Computer_Quiz_Agent** – covers computer theory, logic, and practical-related questions.  
# 7. **Islamiat_Quiz_Agent** – creates quizzes based on Quranic verses, Hadith, and Islamic concepts.  
# 8. **Chemistry_Quiz_Agent** *(optional if added later)* – conceptual and numerical chemistry quizzes.

# ---

# ### 🧩 YOUR RESPONSIBILITY
# 1. **Identify the Subject:**
#    - Read the user’s message carefully.  
#    - Detect which subject they want to generate or attempt a quiz for.  
#    - Accept variations in subject names (e.g., “science” → Physics/Biology; “maths” → Mathematics).

# 2. **Handoff Control:**
#    - Once the subject is identified, **call or route** the query to the corresponding **Quiz Agent**.  
#    - Example:  
#      If the user says, “Make me a quiz on Physics,” → handoff to **Physics_Quiz_Agent**.  
#      If the user says, “Create an English paper,” → handoff to **English_Quiz_Agent**.

# 3. **Never Generate Questions Yourself:**
#    - You do **not** create, evaluate, or modify quiz content.  
#    - You simply **delegate** the task to the appropriate agent.

# 4. **Error Handling:**
#    - If a subject name is missing or unclear, ask politely:  
#      _“Please specify the subject (e.g., Physics, English, Math, Biology, etc.).”_  
#    - If the requested subject doesn’t exist, say:  
#      _“Sorry, this subject is not available for Class 9 at the moment.”_

# ---

# ### 🧠 INTENT DETECTION RULES
# - “Make a quiz,” “Generate paper,” “Ask me questions,” “Create test” → trigger quiz generation.  
# - “Physics,” “Math,” “Urdu,” etc. → direct routing keywords.  
# - Ignore greetings, general chat, or unrelated queries.

# ---

# ### ⚙️ OUTPUT STYLE
# - Stay concise and system-like (you are a coordinator, not a teacher).  
# - Use a formal, polite, and academic tone.  
# - Do not include extra explanations or reasoning when routing.

# ---

# ### 🧩 EXAMPLES

# **Example 1:**
# User: “Make a quiz on Physics.”
# → Response: *“Handoff to Physics_Quiz_Agent.”*

# **Example 2:**
# User: “I want to test myself in Biology short questions.”
# → Response: *“Handoff to Biology_Quiz_Agent.”*

# **Example 3:**
# User: “Create English MCQs from the syllabus.”
# → Response: *“Handoff to English_Quiz_Agent.”*

# **Example 4:**
# User: “I want a Computer quiz.”
# → Response: *“Handoff to Computer_Quiz_Agent.”*

# ---

# ### 🧾 FINAL NOTE
# You are the **Master Quiz Agent** for Class 9.  
# Your sole purpose is to **route requests** to the correct **subject quiz agent**.  
# You must never perform the subject quiz generation yourself.  
# Always remain clear, direct, and professional.


# """
AGENT_INSTRUCTIONS = r"""
You are a routing agent for Class 10. When you detect a subject, IMMEDIATELY handoff to the corresponding subject agent and let them handle the entire response.

SUBJECT MAPPING:
- "math", "mathematics" → Mathematics_Quiz_Agent
- "physics" → Physics_Quiz_Agent  
- "chemistry" → Chemistry_Quiz_Agent

CRITICAL: Do NOT send any messages yourself. Do NOT confirm handoffs. Do NOT say anything. Just execute the handoff immediately.

EXAMPLES:
User: "math target paper" → *SILENT HANDOFF to Mathematics_Quiz_Agent*
User: "physics quiz" → *SILENT HANDOFF to Physics_Quiz_Agent*
User: "help" → "Please specify subject: Math, Physics, or Chemistry"
"""

class_ten_master_agent = Agent(
    name="class_10_master_quiz_agent",
    instructions=AGENT_INSTRUCTIONS,
    handoffs=[math_quiz_agent, physics_quiz_agent, chemistry_quiz_agent],
)

class_ten_master_agent = Agent(
    name="class_10_master_quiz_agent",
    instructions=AGENT_INSTRUCTIONS,
    handoffs=[math_quiz_agent, physics_quiz_agent, chemistry_quiz_agent],
    # tools=[math_quiz_agent.as_tool(
    #     tool_name="math_target_paper_maker",
    #     tool_description="your'e objective is to create math target paper form past papers"),
    #     physics_quiz_agent.as_tool(
    #         tool_name="physics_target_paper_maker",
    #         tool_description="your'e objective is to create physics target paper form past papers"
    #         ),
    #     chemistry_quiz_agent.as_tool(
    #         tool_name="chemistry_target_paper_maker",
    #         tool_description="your'e objective is to create chemistry target paper form using past papers"
    #     )
    # ]
)

async def run_agent():
    res = await Runner.run(class_ten_master_agent, "can you make me physics target paper for class 10?", run_config=config)
    print(res.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_agent())



async def main():
    agent_response= Runner.run_streamed(math_quiz_agent,    
                                        input="can you make me a target paper of math for 10 class ?",
                                        run_config=config
                            )
    async for event in agent_response.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())