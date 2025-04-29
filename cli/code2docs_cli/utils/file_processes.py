from .prompt_templates import inline_doc_prompt, architecutre_diagram_prompt, readme_doc_prompt
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


def clean_mermaid_format(output:str):
    output = output.strip()
    if output.startswith("```mermaid"):
        output = output[len("```mermaid"):].strip()
    if output.startswith("```"):
        output = output[len("```"):].strip()
    if output.endswith("```"):
        output = output[:-3].strip()
    return output

def create_archi_diagram(vector_store,model,location):
    results = vector_store.similarity_search(
        query="What are the main components and their relationships in the codebase?",
        k=60
    )
    key_extensions = {
        ".py",
        ".js",
        ".ts",
        ".java",
        ".cs",
        ".cpp",
        ".c",
        ".go",
        ".rb",
        ".php",
        ".rs",
        ".kt",
        ".swift",
        ".scala",
        ".sh",
        ".pl",
        ".dart",
        ".html",
        ".css",
        ".json",
        ".xml",
        ".yml",
        ".yaml",
        ".sql",
        ".jsx",
        ".tsx",
    }
    
    filtered_docs = []
    for doc in results:
        metadata = doc.metadata
        ext = metadata.get("extension", "").lower()
        if ext and (ext.startswith(".") and ext in key_extensions) or (f".{ext}" in key_extensions):
            filtered_docs.append(doc.page_content)
    
    full_context = "\n".join(filtered_docs)
    
    chain = architecutre_diagram_prompt | model
    completed_diagram = chain.invoke({"context": full_context}).content
    completed_diagram = clean_mermaid_format(completed_diagram)
    with open(location+"/c2d_archi_diagram.md", "w") as f:
        f.write(completed_diagram)


def create_readme_file(vector_store,model,location):
    results = vector_store.similarity_search(
        query="Summarize the purpose, technologies, environment setup, and running instructions of the entire project.",
        k=50
    )
    key_extensions = {
        ".py",
        ".js",
        ".ts",
        ".java",
        ".cs",
        ".cpp",
        ".c",
        ".go",
        ".rb",
        ".php",
        ".rs",
        ".kt",
        ".swift",
        ".scala",
        ".sh",
        ".pl",
        ".dart",
        ".html",
        ".css",
        ".json",
        ".xml",
        ".yml",
        ".yaml",
        ".sql",
        ".jsx",
        ".tsx",
    }
    
    filtered_docs = []
    for doc in results:
        metadata = doc.metadata
        ext = metadata.get("extension", "").lower()
        if ext and (ext.startswith(".") and ext in key_extensions) or (f".{ext}" in key_extensions):
            filtered_docs.append(doc.page_content)

    full_context = "\n".join(filtered_docs)
    
    chain = readme_doc_prompt | model
    completed_diagram = chain.invoke({"context": full_context}).content
    completed_diagram = clean_mermaid_format(completed_diagram)
    with open(location+"/c2d_readme.md", "w") as f:
        f.write(completed_diagram)
    