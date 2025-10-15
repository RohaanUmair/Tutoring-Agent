# src/utils/voice_utils.py
import re

def get_voice_config():
    """Configuration for voice settings"""
    return {
        "language": "en-US",
        "rate": 0.95,       # Slightly slower for clarity
        "pitch": 1.0,
        "volume": 1.0
    }

def format_for_speech(text: str) -> str:
    """
    Format text to be voice-friendly
    Remove LaTeX, JSON, and make conversational
    """
    
    # Remove JSON blocks
    text = re.sub(r'```json.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'\{[^}]*"detected_class"[^}]*\}', '', text)
    
    # Remove markdown code blocks
    text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
    
    # Remove LaTeX formatting
    text = re.sub(r'\\\[.*?\\\]', '', text, flags=re.DOTALL)  # Display math
    text = re.sub(r'\\\(([^)]*)\\\)', r'\1', text)  # Inline math
    text = re.sub(r'\$\$([^$]*)\$\$', r'\1', text)  # Display math
    text = re.sub(r'\$([^$]*)\$', r'\1', text)  # Inline math
    
    # Remove boxed answers
    text = re.sub(r'\\boxed\{([^}]*)\}', r'The answer is \1', text)
    
    # Remove markdown headers
    text = re.sub(r'#{1,6}\s*', '', text)
    
    # Remove bold/italic markdown
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    
    # Remove bullets and numbering
    text = re.sub(r'^\s*[-*•]\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s*', '', text, flags=re.MULTILINE)
    
    # Convert math symbols to words
    replacements = {
        '\\log': ' log ',
        '\\sin': ' sine ',
        '\\cos': ' cosine ',
        '\\tan': ' tangent ',
        '\\frac': ' fraction ',
        '^': ' to the power of ',
        '_': ' sub ',
        '±': ' plus or minus ',
        '≤': ' less than or equal to ',
        '≥': ' greater than or equal to ',
        '≠': ' not equal to ',
        '∞': ' infinity ',
        'π': ' pi ',
        '√': ' square root of ',
        '∫': ' integral of ',
        '∑': ' sum of ',
        '×': ' times ',
        '÷': ' divided by ',
        '\\cdot': ' times ',
        '\\times': ' times ',
        '\\div': ' divided by ',
    }
    
    for symbol, word in replacements.items():
        text = text.replace(symbol, word)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Limit length for voice (first 500 characters + "...")
    if len(text) > 500:
        text = text[:500].rsplit(' ', 1)[0] + "... Would you like me to continue?"
    
    return text.strip()

def format_for_display(text: str) -> str:
    """
    Format text for visual display (keeps LaTeX, removes only JSON)
    """
    # Remove JSON blocks
    text = re.sub(r'```json.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'\{[^}]*"detected_class"[^}]*\}', '', text)
    
    # Clean up extra whitespace
    text = ' '.join(text.split())
    
    return text.strip()