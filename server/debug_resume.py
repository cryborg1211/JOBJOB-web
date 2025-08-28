#!/usr/bin/env python3
"""
Debug tool for testing resume parser
Usage: python debug_resume.py --print-sections <file_path>
"""

import sys
import argparse
from utils.parse_resume import extract_profile, split_sections

def main():
    parser = argparse.ArgumentParser(description='Debug resume parser')
    parser.add_argument('--print-sections', action='store_true', help='Print parsed sections')
    parser.add_argument('file_path', help='Path to resume file (PDF/DOC/DOCX)')
    
    args = parser.parse_args()
    
    try:
        with open(args.file_path, 'rb') as f:
            if args.print_sections:
                # Test section splitting
                text = f.read()
                if args.file_path.lower().endswith('.pdf'):
                    from utils.parse_resume import _read_pdf
                    text, _ = _read_pdf(text)
                elif args.file_path.lower().endswith(('.doc', '.docx')):
                    from utils.parse_resume import _read_docx
                    text, _ = _read_docx(text)
                else:
                    print("Unsupported file type")
                    return
                
                sections = split_sections(text)
                print("=== PARSED SECTIONS ===")
                for section_name, content in sections.items():
                    print(f"\n--- {section_name.upper()} ---")
                    print(content[:500] + "..." if len(content) > 500 else content)
                
                print("\n=== FULL PROFILE ===")
                f.seek(0)  # Reset file pointer
                profile = extract_profile(f, args.file_path)
                for key, value in profile.items():
                    if key == 'avatar_data_url':
                        print(f"{key}: [AVATAR DATA]")
                    else:
                        print(f"{key}: {value}")
            else:
                # Extract full profile
                profile = extract_profile(f, args.file_path)
                print("=== EXTRACTED PROFILE ===")
                for key, value in profile.items():
                    if key == 'avatar_data_url':
                        print(f"{key}: [AVATAR DATA]")
                    else:
                        print(f"{key}: {value}")
                        
    except FileNotFoundError:
        print(f"File not found: {args.file_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()


