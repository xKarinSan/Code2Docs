from uuid import uuid4
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .prompt_templates import rag_file_summarise_prompt
from concurrent.futures import ThreadPoolExecutor, as_completed


def read_all_file_contents(read_files,chunk_size=500, chunk_overlap=75):
    """
    Convert the files into LangChain Document objects.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
         separators=["\n\n", "\n", " ", ""]
    )
    # split per file
    # then into chunks, metadata more or less the same
    documents = []
    id = 0
    for file in read_files:
        chunks = text_splitter.split_text(file["contents"])
        for idx, chunk in enumerate(chunks):
            new_doc = Document(
                page_content=chunk,
                metadata={
                    "source": file["filePath"],
                    "extension": file["extension"],
                    "id": id,
                },
            )
            id += 1
            documents.append(new_doc)
    uuids = [str(uuid4()) for _ in range(len(documents))]
    return documents, uuids

def summarize_documents(docs, model, max_workers=6):
    """
    Summarize each file concurrently to reduce total token usage and speed up processing.
    """
    print(f"[⚡️] Summarizing {len(docs)} documents in parallel...")

    chain = rag_file_summarise_prompt | model

    summaries = []

    def summarize_doc(doc):
        content = doc.page_content.strip()
        if len(content) <= 50:
            return None
        summary = chain.invoke({"code": content}).content
        return f"File: {doc.metadata['source']}\n{summary}\n"

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_doc = {executor.submit(summarize_doc, doc): doc for doc in docs}
        for future in as_completed(future_to_doc):
            result = future.result()
            if result:
                summaries.append(result)

    return summaries