
from .prompt_templates import inline_doc_prompt
from .parsers import SimpleOutputParser

def document_code_file(file_path: str, code: str, extension: str,model):
    
    print(f"[✏️] Documenting: {file_path} ({extension})")
    chain = inline_doc_prompt | model | SimpleOutputParser()
    
    try:
        result = chain.invoke({"code": code, "language": extension})
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"[✅] Finished: {file_path}")
    except Exception as e:
        print(f"[❌] Error processing {file_path}: {e}")
        
        
