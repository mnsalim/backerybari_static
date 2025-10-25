import os
import re

# Regex pattern to match the conflict lines
conflict_pattern = re.compile(r'^(<<<<<<<|=======|>>>>>>>).*$', re.MULTILINE)

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith(('.html', '.js', '.css')): # Focus on web files
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r+', encoding='utf-8') as f:
                    content = f.read()
                    new_content = re.sub(conflict_pattern, '', content)

                    if new_content != content:
                        f.seek(0)
                        f.truncate()
                        f.write(new_content)
                        print(f"Cleaned: {filepath}")

            except Exception as e:
                print(f"Could not process {filepath}: {e}")