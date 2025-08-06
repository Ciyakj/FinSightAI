# utils/file_reader.py

def read_code_files(uploaded_files):
    content = ""
    for file in uploaded_files:
        file_content = file.read().decode("utf-8", errors="ignore")
        content += file_content + "\n\n"
    return content
