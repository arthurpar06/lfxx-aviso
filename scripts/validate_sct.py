#!/usr/bin/env python3
import os
import re
import sys

def validate_sct_file(filepath):
    """
    Validates a single .sct file.
    Rules:
    - Text must be placed into sections.
    - Sections are defined by headers like [INFO], [VOR], [NDB], [FIXES].
    - No text allowed outside of a section (only whitespace).
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_section = None
    errors = []
    
    # Regex for section header: Starts with [, uppercase letters/numbers/underscores, ends with ]
    # Allowing some flexibility, but strictly it seems to require uppercase based on prompt examples.
    section_header_pattern = re.compile(r'^\[([A-Z0-9_]+)\]\s*$')

    for line_num, line in enumerate(lines, 1):
        stripped_line = line.strip()
        
        # Skip empty lines
        if not stripped_line:
            continue
            
        # Check if it's a section header
        match = section_header_pattern.match(stripped_line)
        if match:
            current_section = match.group(1)
            continue
            
        # If not a header, check if we are in a section
        if current_section is None:
            # Found content before any section
            errors.append(f"Line {line_num}: Content found before the first section header: '{stripped_line}'")
        
        # If we are in a section, content is valid.
        # We assume ANY content is valid inside a section as per "Some random text".

    return errors

def main():
    root_dir = os.getcwd()
    sct_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.sct'):
                sct_files.append(os.path.join(root, file))

    if not sct_files:
        print("No .sct files found to validate.")
        sys.exit(0)

    print(f"Found {len(sct_files)} .sct files. Starting validation...")
    
    any_errors = False
    for filepath in sct_files:
        rel_path = os.path.relpath(filepath, root_dir)
        errors = validate_sct_file(filepath)
        
        if errors:
            any_errors = True
            print(f"❌ {rel_path}: FAILED")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"✅ {rel_path}: PASSED")

    if any_errors:
        print("\nValidation failed for one or more files.")
        sys.exit(1)
    else:
        print("\nAll .sct files validated successfully.")
        sys.exit(0)

if __name__ == "__main__":
    main()
