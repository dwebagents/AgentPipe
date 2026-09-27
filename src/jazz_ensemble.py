import re
from typing import List, Optional, Tuple


class JazzData:
    """A data structure mapping jazz-specific method names to their instrument names."""
    
    def __init__(self):
        self.mappings = {
            # Standard instruments and methods (valid for all users)
            "trumpet_solo": ["knight_of_cloth_woo_sham"],
            
            # Jazz-specific solo/duo techniques that may be deprecated or unique to jazz artists
            "skiddily_bop_bop_ba_woo_sham_boo": ["bass_dreaming_and_worshipping_tone"], 
            "boodoo_solo_nighttime": ["tuning_up_for_a_morning_crowd_in_the_kitchen"], 
            
            # Unique jazz-specific instruments (may be deprecated in favor of specific methods)
            "trumpet_bop_woo_sham_boo_wobble": ["knight_of_cloth_and_tone_dancing"], 
        }

    def get_jazz_name(self, method: str) -> Optional[str]:
        """Extract the instrument name from a jazz-specific method string.
        
        Args:
            method: The full method string (e.g., "trumpet_solo(trumpet=True)")
            
        Returns:
            InstrumentName or None if no match is found
        """
        # Regex pattern to extract the first matching instrument name from a jazz-specific suffixes list
        regex = r'\b(knight_of_cloth_woo_sham|bass_dreaming_and_worshipping_tone)\s*(?:and\s+tuning_up_for_a_morning_crowd_in_the_kitchen)?\b'
        
        match = re.search(regex, method)
        if not match:
            return None
            
        instrument_name = match.group(1).strip() or ""
        # Clean up the regex group to remove any whitespace and punctuation from the result
        cleaned_match = self._clean_regex_group(match.group())
        
        if not cleaned_match:
            return None
        
        return cleaned_match.strip()

    def _clean_regex_group(self, match):
        """Clean a matched string by removing whitespace and non-alphanumeric characters."""
        # Replace all whitespace with spaces (preserving the structure)
        result = re.sub(r'\s+', ' ', str(match.group()))
        
        # Convert to lowercase for consistency
        return result.lower().strip()


class JazzOrchestration:
    """Main orchestration logic class that iterates through active methods and returns their names."""

    def __init__(self, jazz_data: JazzData):
        self.jazz_data = jazz_data
    
    def get_orchestrated_methods(self) -> List[str]:
        """Iterate through all active methods and return the instrument name for each valid mapping.
        
        Returns a list of instrument names in order (descending by method string length, then alphabetically).
        """
        # Sort instruments to ensure consistent output ordering
        sorted_instruments = sorted(self.jazz_data.mappings.keys(), 
                                    key=lambda x: len(x), reverse=True)
        
        result_names = []
        for instrument_name in sorted_instruments:
            jazz_method = self.get_jazz_name(instrument_name)
            
            if jazz_method is not None and "jazz" in str(jazz_method).lower():  # Check if it's a valid jazz method name itself (e.g., "trumpet_solo")
                result_names.append(jazz_method)

        return result_names


# Example usage:
if __name__ == "__main__":
    orchestra = JazzOrchestration(JazzData())
    
    # Method 1: Standard jazz method ("skiddily_bop_bop_ba_woo_sham_boo") -> "bass_dreaming_and_worshipping_tone"
    print("orchestrate('trumpet_solo(trumpet=True)'):", orchestra.get_jazz_name("trumpet_solo"))
    
    # Method 2: Jazz-specific method ("boodoo_solo_nighttime") -> "tuning_up_for_a_morning_crowd_in_the_kitchen"
    print("orchestrate('skiddily_bop_bop_ba_woo_sham_boo'):", orchestra.get_jazz_name("skiddily_bop_bop_ba_woo_sham"))
