import os
import re

# 1. Define the project directory to scan (the current directory)
PROJECT_ROOT = '.'

# 2. Define file extensions to search within
FILE_EXTENSIONS = ('.html', '.css', '.js', '.jsx') 

# 3. Define the patterns to fix:
#    The script looks for any string 'asset/...' that DOES NOT start with a slash
#    and replaces it with '/asset/...'
#    It also handles 'assets/...' (plural) just in case.
#
#    Note: This is a robust regex to ensure we don't accidentally break existing absolute paths.
PATTERNS_TO_FIX = [
    (r'(["\'(])assets/(?![a-zA-Z0-9\.]+:\/\/)', r'\1/assets/'), # Finds "assets/..." or 'assets/...' or (assets/...
    (r'(["\'(])asset/(?![a-zA-Z0-9\.]+:\/\/)', r'\1/asset/')   # Finds "asset/..." or 'asset/...' or (asset/...
]

def fix_paths_in_file(filepath):
    """Reads a file, performs the path replacement, and writes the changes back."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all defined patterns
        for old_pattern, new_pattern in PATTERNS_TO_FIX:
            content = re.sub(old_pattern, new_pattern, content)
            
        # Write back to file only if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed paths in: {filepath}")
            return True
        else:
            return False

    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def run_path_fixer():
    """Walks through the project directory and fixes paths in all targeted files."""
    print("--- Starting Asset Path Fixer ---")
    files_processed = 0
    files_modified = 0
    
    for root, _, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.lower().endswith(FILE_EXTENSIONS):
                files_processed += 1
                filepath = os.path.join(root, file)
                
                if fix_paths_in_file(filepath):
                    files_modified += 1
                    
    print(f"\n--- Processing Complete ---")
    print(f"Total files scanned: {files_processed}")
    print(f"Total files modified: {files_modified}")

if __name__ == "__main__":
    run_path_fixer()
