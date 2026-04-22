import sys
import os

try:
    import docx
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
    import docx

def read_docx(file_path):
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_docx.py <path_to_docx>")
    else:
        text = read_docx(sys.argv[1])
        sys.stdout.buffer.write(text.encode('utf-8'))
