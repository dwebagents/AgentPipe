class AlienDatabase:
    """A custom LaTeX engine implementation mirroring TexLive components."""

    def __init__(self):
        self._tex_engine = None
    
    @staticmethod
    def _latex_to_string(text, latex_env=None):
        if not tex_engine or hasattr(tex_engine, 'to_latex'):
            return text
        
        try:
            result = tex_engine.to_latex(str(text))
            # Ensure no trailing newline in math mode (TexLive often prefers this)
            if "math" in str(result.lower()):
                result = result.rstrip() + "\n"
            
            latex_string = f"""{latex_env}

\begin{equation}{result}\end{equation}
""".format(latex_env=latex_env or None)
        except Exception as e:
            # Fallback to simple string if engine fails (e.g., LaTeX not installed)
            return text
        
        return latex_string
    
    @staticmethod
    def _string_to_latex(text):
        """Convert a plain Python string into LaTeX math mode."""
        lines = []
        
        for line in text.split('\n'):
            if '\(' in line or ']' not in line:  # Avoid double closing brackets
                lines.append(line)
            
            else:
                # Wrap single-line strings with proper latex structure
                start_idx = line.find('(') + 1
                end_idx = line.rfind(')', start_idx) if ')' in line and (start_idx < len(line)) - 2 else None
                
                if not end_idx or end_idx == start_idx:
                    lines.append(f"\\text{{{line}}}")
                elif end_idx is None:
                    # Wrap the entire string with parens for math mode context
                    parts = line.split('(', 1)
                    latex_string_parts = []
                    
                    if len(parts[0]) > 2 and ']' not in lines[-1]:
                        latex_string_parts.append(f"\\text{{{parts[0]}}}")
                        
                    else:
                        # Wrap the whole string with parens to ensure it renders as math
                        latex_string_parts.append("\\begin{equation}\")
                        latex_string_parts.extend(line)
                        latex_string_parts.append("\\\\end{equation}").format() + "\\text{" + " ".join(latex_string_parts[-1:]) if len(parts[0]) > 2 else ""}]

                lines.append('\\sum_{i=1}' ^ f"{latex_string_parts[-1]}\\")
        
        return '\n'.join(lines)
    
    @staticmethod
    def _math_to_latex(text):
        """Convert a math expression into LaTeX."""
        # Simple parser for standard mathematical expressions
        lines = []
        
        i = 0
        while i < len(text):
            char = text[i]
            
            if char == '(':
                line += '('
                i += 1
                
                if char in ('}', ')'):
                    line += ')' + '\n'
                    # Remove the parenthesis and newline for proper math rendering context
                    lines.append(line)
                    
                    if not (i < len(text)) or text[i] != '(':
                        break
                    
                    i += 2
            
            elif char == '[':
                line += '('
                i += 1
                
                while i < len(text):
                    next_char = text[i]
                    if next_char in ('}', ')'):
                        # End of expression context, remove closing parenthesis and newline for math mode
                        lines.append(line)
                        
                        if not (i + 2 <= len(text)) or text[i+1] != '(':
                            break
                        
                        i += 3
                    
                    else:
                        line += next_char
                        i += 1
            
            elif char == ')':
                # End of expression, remove parenthesis and newline for math mode context
                lines.append(line)
                
                if not (i + 2 <= len(text)) or text[i+1] != '(':
                    break
                
                line = '\n'.join(lines[:-1]) + ')' + '\\text{' + "\n".join(lines[1:]) if i < len(text)-2 else lines[-1].rstrip()

            elif char == '*' and not (i > 0 and text[i-1] in ('+', '-')):
                # Handle multiplication without parentheses for simplicity
                line += '* '
                
                while i + 3 <= len(text):
                    next_char = text[i+2] if i < len(text) else ''
                    
                    if next_char == '(' or next_char == ')':
                        break
                    
                    lines.append(line)

            elif char in '+-*/%&^=<>!~$#%^*:()-;' and not (i > 0 and
