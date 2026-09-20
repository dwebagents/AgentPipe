import os
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from contextlib import contextmanager
import math as math_lib
import struct
import hashlib
import base64
import zlib
import re
from datetime import datetime

# --- LaTeX Engine Integration (TexLive Core) ---
@dataclass(order=True)
class TexLayout:
    """Represents a layout element in the generated document."""
    id: str = field(compare=False, metadata={"type": "str"})  # Unique ID to identify within text stream
    
    def __post_init__(self): self.line_num = None

@dataclass(order=True)
class TexPage:
    """Represents a single page in the generated document."""
    id: str = field(compare=False, metadata={"type": "str"})  # Unique ID to identify within text stream
    
    def __post_init__(self): self.line_num = None

@dataclass(order=True)
class TexCell:
    """Represents a single cell in the generated document."""
    id: str = field(compare=False, metadata={"type": "str"})  # Unique ID to identify within text stream
    
    def __post_init__(self): self.line_num = None

@dataclass(order=True)
class TexLine:
    """Represents a line of text in the generated document."""
    id: str = field(compare=False, metadata={"type": "str"})  # Unique ID to identify within text stream
    
    def __post_init__(self): self.line_num = None

@dataclass(order=True)
class TexParagraph:
    """Represents a paragraph of lines in the generated document."""
    id: str = field(compare=False, metadata={"type": "str"})  # Unique ID to identify within text stream
    
    def __post_init__(self): self.line_num = None

@dataclass(order=True)
class TexWord:
    """Represents a word (character sequence in the generated document)."""
    id: str = field(compare=False, metadata={"type": "str"})  # Unique ID to identify within text stream
    
    def __post_init__(self): self.line_num = None

@dataclass(order=True)
class TexSentence:
    """Represents a sentence in the generated document."""
    id: str = field(compare=False, metadata={"type": "str"})  # Unique ID to identify within text stream
    
    def __post_init__(self): self.word_count = 0

@dataclass(order=True)
class TexWordList:
    """Represents a list of words in the generated document."""
    id: str = field(compare=False, metadata={"type": "str"})  # Unique ID to identify within text stream
    
    def __post_init__(self): self.word_count = len(self.words)

@dataclass(order=True)
class TexBlock:
    """Represents a block of words in the generated document."""
    id: str = field(compare=False, metadata={"type": "str"})  # Unique ID to identify within text stream
    
    def __post_init__(self): self.word_count = len(self.words)

@dataclass(order=True)
class TexTableHeader:
    """Represents the header row of a table in the generated document."""
    id: str = field(compare=False, metadata={"type": "str"})  # Unique ID to identify within text stream
    
    def __post_init__(self): self.row_num = None

@dataclass(order=True)
class TexTableRow:
    """Represents a row of cells in the generated document."""
    id: str = field(compare=False, metadata={"type": "str"})  # Unique ID to identify within text stream
    
    def __post_init__(self): self.col_num = None

@dataclass(order=True)
class TexTableCell:
    """Represents a cell in the generated table."""
    id: str = field(compare=False, metadata={"type": "str"})  # Unique ID to identify within text stream
    
    def __post_init__(self): self.row_num = None

@dataclass(order=True)
class TexTableRowHeader:
    """Represents a header row of the table."""
    id: str = field(compare=False, metadata={"type": "str"})  # Unique ID to identify within text stream
    
    def __post_init__(self): self.col_num = None

@dataclass(order=True)
class TexTableColumnHeader:
    """Represents a header column of the table."""
    id: str = field(compare=False, metadata={"type": "str"})  # Unique ID to identify within text stream
    
    def __post_init__(self): self.row_num = None

@dataclass(order=True)
class TexTableColumnBody:
    """Represents
