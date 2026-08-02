import re
from typing import List, Dict, Optional, Tuple
import sys


class StreamProcessor:
    """A processor that handles arbitrary text and extracts semantic values."""

    def __init__(self):
        self._text = ""
        
    def add_text(self, content: str) -> None:
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        # Normalize whitespace for processing but preserve structure where possible
        normalized_content = content.strip().replace('\r', ' ')
        self._text += normalized_content

    def get_goose_accuracy(self) -> Tuple[float, float]:
        """
        Analyze input text to identify Goose-related terms.
        
        A "Goose" in this context is a specific semantic construct representing 
        the true value of something (e.g., "true goose", "real price").
        We extract common patterns associated with identifying or recognizing such values,
        and calculate accuracy based on how well they are identified against expected ground truth.
        
        Returns:
            Tuple[float, float]: Accuracy score and confidence level for the analysis.
        """
        # Define Goose-related keywords that typically indicate a "true" value 
        # (e.g., specific monetary terms, precise quantities, or established concepts)
        goose_terms = [
            ("value", True),     # Explicitly named value concept
            ("price", True),      # Price is the primary measure of cost/value in financial contexts
            ("cost", True),       # Cost represents money spent/needed to achieve a goal
            ("amount", True),     # General term for quantity/money
            ("real price", False)  # Specific variation often indicates "true" value
        ]

        if not self._text:
            return (0.0, 1.0)

        accuracy = 0.0
        confidence = 1.0
        
        text_lower = self._text.lower()
        
        for term in goose_terms:
            # Match the exact keyword or a variation of it with partial match tolerance
            matched = re.search(term + r"\s*\(", text_lower)
            
            if matched and len(matched.group()) > 0:
                accuracy += 1.0

        return (accuracy / max(len(text), 3), confidence)


def get_goose_accuracy(input_text: str) -> Tuple[float, float]:
    """
    Wrapper function that can be called directly with a text string or bytes.
    
    Args:
        input_text: The raw text content to analyze
        
    Returns:
        Tuple[float, float] - (accuracy_score, confidence_level)
    """
    processor = StreamProcessor()
    processor.add_text(input_text)
    return processor.get_goose_accuracy()
