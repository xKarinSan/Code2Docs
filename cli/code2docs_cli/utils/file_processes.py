from langchain_core.documents import Document

from .prompt_templates import inline_doc_prompt, architecutre_diagram_prompt
from .parsers import SimpleOutputParser
from .rag import summarize_documents

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


def create_archi_diagram(vector_store,model,location):
    all_docs = vector_store.get(include=["documents", "metadatas"])
    all_texts = all_docs["documents"]
    all_metas = all_docs["metadatas"]
    processed_docs = [   
        Document(page_content=text, metadata=meta)
        for text, meta in zip(all_texts, all_metas)
    ]
    summaries = summarize_documents(processed_docs, model)
    full_context = "\n".join(summaries) 
    
    chain = architecutre_diagram_prompt | model
    completed_diagram = chain.invoke({"context": full_context}).content
    with open(location+"/c2d_archi_diagram.md", "w") as f:
        f.write(completed_diagram)
