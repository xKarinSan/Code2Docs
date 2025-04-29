from uuid import uuid4
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def read_all_file_contents(read_files,chunk_size=500, chunk_overlap=75):
    """
    Convert the files into LangChain Document objects.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
         separators=["\n\n", "\n", " ", ""]
    )
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