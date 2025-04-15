
from .prompt_templates import inline_doc_prompt, rag_file_summarise_prompt, architecutre_diagram_prompt
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

def summarize_doc(doc,model):
    chain = rag_file_summarise_prompt | model
    # print("doc",doc)
    content = doc.page_content.strip()
    if len(content) <= 50:
        return None
    summary = chain.invoke({"code": content}).content
    return f"File: {doc.metadata['source']}\n{summary}\n"

def create_archi_diagram(context,model,location):
    chain = architecutre_diagram_prompt | model
    completed_diagram = chain.invoke({"context": context}).content
    with open(location+"/c2d_archi_diagram.md", "w") as f:
        f.write(completed_diagram)
