#!/usr/bin/env python3
"""
Debug tool for testing JD parser
Usage: python debug_jd.py <file_path>
"""

import sys
import argparse
from utils.parse_jd import parse_jd, split_sections

def main():
    parser = argparse.ArgumentParser(description='Debug JD parser')
    parser.add_argument('file_path', help='Path to JD file (PDF/DOC/DOCX/TXT)')
    
    args = parser.parse_args()
    
    try:
        with open(args.file_path, 'rb') as f:
            # Test section splitting
            text = f.read()
            if args.file_path.lower().endswith('.pdf'):
                from utils.parse_jd import _read_pdf
                text, _ = _read_pdf(text)
            elif args.file_path.lower().endswith(('.doc', '.docx')):
                from utils.parse_jd import _read_docx
                text, _ = _read_docx(text)
            elif args.file_path.lower().endswith('.txt'):
                from utils.parse_jd import _read_txt
                text, _ = _read_txt(text)
            else:
                print("Unsupported file type")
                return
            
            print("=== PARSED SECTIONS ===")
            sections = split_sections(text)
            for section_name, content in sections.items():
                print(f"\n--- {section_name.upper()} ---")
                print(content[:300] + "..." if len(content) > 300 else content)
            
            print("\n=== FULL PARSED JD ===")
            f.seek(0)  # Reset file pointer
            jd_data = parse_jd(f, args.file_path)
            for key, value in jd_data.items():
                if isinstance(value, list):
                    print(f"{key}: {len(value)} items")
                    for i, item in enumerate(value[:3]):  # Show first 3 items
                        print(f"  {i+1}. {item[:100]}{'...' if len(item) > 100 else ''}")
                else:
                    print(f"{key}: {value[:200]}{'...' if len(value) > 200 else ''}")
                        
    except FileNotFoundError:
        print(f"File not found: {args.file_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
