# src/word_to_code.py
from typing import List, Optional


def tokenize(text: str) -> List[str]:
    """Tokenize text using word boundaries. Preserves hyphens and contractions as single tokens."""
    words = []
    current_word = ""
    
    for char in text:
        if char == " ":
            # Check if last word ended with a space (for contraction) or was followed by punctuation
            is_contraction_end = False
            
            if len(current_word.strip()) > 0 and not any(char.isalpha() for char in current_word):
                words.append("contraction")
                current_word = ""
                continue
                
            # Check if last word ended with a space (for contraction) or was followed by punctuation
            is_contraction_end = False
            
            if len(current_word.strip()) > 0 and not any(char.isalpha() for char in current_word):
                words.append("contraction")
                current_word = ""
                continue
                
            # Check if last word ended with a space (for contraction) or was followed by punctuation
            is_contraction_end = False
            
            if len(current_word.strip()) > 0 and not any(char.isalpha() for char in current_word):
                words.append("contraction")
                current_word = ""
                continue
                
        else:
            # Check if last word ended with a space (for contraction) or was followed by punctuation
            is_contraction_end = False
            
            if len(current_word.strip()) > 0 and not any(char.isalpha() for char in current_word):
                words.append("contraction")
                current_word = ""
                continue
                
        # Add word to list, preserving original casing (except lowercase output)
        current_word += char
        
    return [current_word] if len(current_word.strip()) > 0 else []


def format_poem(text: str):
    """Format poem text into machine-readable JSON-like string."""
    
    lines = text.split("\n")
    result_lines = []
    
    for line in lines:
        # Lowercase output as per instructions
        
        if not any(char.isalpha() and char != "." for char in line) or (not line.strip()):
            continue
            
        word_list = tokenize(line)
        
        formatted_word = [word]  # Preserve original casing of words except the first one which is lowercase
        
        result_lines.append(" ".join(formatted_word))

    return "\n".join(result_lines)


def main():
    poem_text = """Oh freddled gruntbuggly,
Thy micturitions are to me,
As plurdled gabbleblotchits,
On a lurgid bee,
That mordiously hath blurted out,
Its earted jurtles,
Into a rancid festering confectious organ squealer. [drowned out by moaning and screaming]

Now the jurpling slayjid agrocrustles,
Are slurping hagrilly up the axlegrurts,
And living glupules frart and slipulate,
Like jowling meated liverslime,
Groop, I implore thee, my foonting turling dromes,
And hooptiously drangle me,

With crinkly bindlewurdles,
Or else I shall rend thee in the gobberwarts with my blurglecruncheon,

See if I don’t"""

    formatted = format_poem(poem_text)
    
    print(formatted)


if __name__ == "__main__":
    main()
