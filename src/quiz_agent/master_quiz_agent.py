import os
import json
from agents import function_tool
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner
import asyncio
import sys
import os

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), 'class_09'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'class_10'))

# Import config - adjust path as needed
from Config.config import config

# Initialize agent mapping
agent_mapping = {'config': config}

# Import Class 09 Agents with error handling
try:
    from class_09.math_quiz_system.math_quiz_agent import math_quiz_agent as math_09
    agent_mapping.update({
        '9 math': math_09, '9 mathematics': math_09, 'class 9 math': math_09
    })
    print("✓ Math 09 imported")
except ImportError as e:
    print(f"✗ Math 09 import failed: {e}")

try:
    from class_09.physics_quiz_system.physics_quiz_agent import physics_quiz_agent as physics_09
    agent_mapping.update({
        '9 physics': physics_09, 'class 9 physics': physics_09
    })
    print("✓ Physics 09 imported")
except ImportError as e:
    print(f"✗ Physics 09 import failed: {e}")

try:
    from class_09.chemistry_quiz_system.chemistry_quiz_agent import chemistry_quiz_agent as chemistry_09
    agent_mapping.update({
        '9 chemistry': chemistry_09, 'class 9 chemistry': chemistry_09
    })
    print("✓ Chemistry 09 imported")
except ImportError as e:
    print(f"✗ Chemistry 09 import failed: {e}")

try:
    from class_09.biology_quiz_system.bio_quiz_agent import biology_quiz_agent as biology_09
    agent_mapping.update({
        '9 biology': biology_09, 'class 9 biology': biology_09, '9 bio': biology_09
    })
    print("✓ Biology 09 imported")
except ImportError as e:
    print(f"✗ Biology 09 import failed: {e}")

try:
    from class_09.computer_quiz_system.computer_quiz_agent import computer_quiz_agent as computer_09
    agent_mapping.update({
        '9 computer': computer_09, 'class 9 computer': computer_09, '9 cs': computer_09
    })
    print("✓ Computer 09 imported")
except ImportError as e:
    print(f"✗ Computer 09 import failed: {e}")

try:
    from class_09.english_quiz_system.english_quiz_agent import english_quiz_agent as english_09
    agent_mapping.update({
        '9 english': english_09, 'class 9 english': english_09
    })
    print("✓ English 09 imported")
except ImportError as e:
    print(f"✗ English 09 import failed: {e}")

# Class 10 Agents  
try:
    from class_10.math_quiz_agent_10.math_quiz_agent import math_quiz_agent as math_10
    agent_mapping.update({
        '10 math': math_10, '10 mathematics': math_10, 'class 10 math': math_10
    })
    print("✓ Math 10 imported")
except ImportError as e:
    print(f"✗ Math 10 import failed: {e}")

try:
    from class_10.physics_quiz_agent_10.physics_quiz_agent import physics_quiz_agent as physics_10
    agent_mapping.update({
        '10 physics': physics_10, 'class 10 physics': physics_10
    })
    print("✓ Physics 10 imported")
except ImportError as e:
    print(f"✗ Physics 10 import failed: {e}")

try:
    from class_10.chemistry_agent_10.chemistry_quiz_agent import chemistry_quiz_agent as chemistry_10
    agent_mapping.update({
        '10 chemistry': chemistry_10, 'class 10 chemistry': chemistry_10
    })
    print("✓ Chemistry 10 imported")
except ImportError as e:
    print(f"✗ Chemistry 10 import failed: {e}")

# ADD THIS SECTION FOR BIOLOGY CLASS 10
try:
    from class_10.biology_agent_10.bio_quiz_agent import biology_quiz_agent as biology_10
    agent_mapping.update({
        '10 biology': biology_10, 'class 10 biology': biology_10, '10 bio': biology_10
    })
    print("✓ Biology 10 imported")
except ImportError as e:
    print(f"✗ Biology 10 import failed: {e}")

# ADD THIS SECTION FOR ENGLISH CLASS 10
try:
    from class_10.english_agent_10.english_quiz_agent import class_10_english_quiz_agent as english_10
    agent_mapping.update({
        '10 english': english_10, 'class 10 english': english_10
    })
    print("✓ English 10 imported")
except ImportError as e:
    print(f"✗ English 10 import failed: {e}")

# ADD THIS SECTION FOR COMPUTER CLASS 10
try:
    from class_10.computer_quiz_agent.computer_quiz_agent import computer_quiz_agent as computer_10
    agent_mapping.update({
        '10 computer': computer_10, 'class 10 computer': computer_10, '10 cs': computer_10
    })
    print("✓ Computer 10 imported")
except ImportError as e:
    print(f"✗ Computer 10 import failed: {e}")
print(f"\n✅ Total agents loaded: {len(agent_mapping) - 1}")  # Subtract config
print("Available subjects:", [k for k in agent_mapping.keys() if k != 'config'])

# Keep the original main function for CLI use
async def main():
    print("\n🎓 Direct Agent Access System")
    print("📚 Available: Class 9/10 - Math, Physics, Chemistry, Biology, Computer, English")
    print("💡 Examples: 'class 9 math', '10 physics', 'biology class 9', '9 bio'")
    print("❌ Type 'exit' to quit\n")
    
    while True:
        user_input = input("You: ").strip().lower()
        
        if user_input in ["exit", "quit", "bye"]:
            print("👋 Goodbye!")
            break
        
        # Find the right agent
        selected_agent = None
        selected_key = None
        
        for key, agent in agent_mapping.items():
            if key != 'config' and key in user_input:
                selected_agent = agent
                selected_key = key
                break
        
        if selected_agent:
            print(f"🔍 Selected: {selected_key.upper()}")
            print("📄 Generating paper...\n" + "="*50)
            
            try:
                agent_response = Runner.run_streamed(
                    selected_agent,
                    input="Generate a comprehensive target paper for 2025",
                    run_config=config
                )
                
                async for event in agent_response.stream_events():
                    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                        print(event.data.delta, end="", flush=True)
                
                print("\n" + "="*50)
                print("✅ Paper generated successfully!")
                
            except Exception as e:
                print(f"❌ Error generating paper: {e}")
        else:
            print("❓ Please specify class and subject clearly.")
            print("   Examples: 'class 9 math', '10 physics', 'biology class 9', '9 bio'")
            print("   Available:", [k for k in agent_mapping.keys() if k != 'config'])

if __name__ == "__main__":
    asyncio.run(main())