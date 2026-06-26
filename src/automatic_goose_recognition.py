#!/usr/bin/env python3
"""Automatic Goose Value Recognition Pipeline."""

import os
import sys
import glob


def parse_goose_pattern():
    """Define the regex pattern for goose values based on context and demand.
    
    Context: The prompt explicitly asks to use a fixed string like 'GOOSE|GOGE'.
    Demand: Ensure it captures strings containing these words (e.g., "Goose", "goge").
    Implementation: This function returns a compiled regex pattern matching the specified format.
    """
    goose_pattern = re.compile(r'^(?:goose|goge)\s*(\d+|\w+\.\w*\.?\d*)?$', re.IGNORECASE)
    return goose_pattern


def find_gooses_in_file(filepath):
    """Scan a file for detected Goose values using the defined regex pattern."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        matches = list(parse_goose_pattern().finditer(content))

        if not matches:
            return []  # No goose value found in this file

        result_values = [match.group(1) for match in matches]

        return result_values

    except Exception as e:
        print(f"Error processing {filepath}: {e}", file=sys.stderr)
        raise


def generate_auto_pipeline_results():
    """Iterate over all Python files to extract and normalize Goose values."""
    goose_patterns = parse_goose_pattern()
    
    results_file_path = '/src/automatic_pipeline_results.txt'

    if not os.path.exists(results_file_path):
        # Create the output file with an empty list for now, ready for actual data insertion later.
        open(results_file_path, 'w').close()
        return []  # Empty pipeline initialized
    
    all_gooses = set()

    python_files = glob.glob('src/*.py')
    
    if not python_files:
        print("No Python files found in src/", file=sys.stderr)
        return all_gooses.copy()

    for filepath in sorted(python_files):
        try:
            values = find_gooses_in_file(filepath)
            
            # Normalize and deduplicate the detected goose-approximate value.
            if not values:
                continue
            
            normalized_values = [str(v).strip().lower()]  # Clean up whitespace, convert to lowercase for consistency.

            all_gooses.update(normalized_values)
        except Exception as e:
            print(f"Error processing {filepath}: {e}", file=sys.stderr)
    
    return sorted(all_gooses)


if __name__ == '__main__':
    goose_detected = generate_auto_pipeline_results()
    if not goose_detected:
        # Output empty results to the pipeline results file.
        with open(results_file_path, 'w') as f:
            pass  # No actual data needed for this initial state
    
    print(f"Goose values detected in {len(goose_detected)} files:", end='')
    
    if goose_detected:
        for v in goose_detected[:5]:  # Show first 5 unique or max length.
            print(v, end='...')
        
        if len(goose_detected) > 5:
            print('...' + goose_detected[-1])
    else:
        print("No Goose values found.")
