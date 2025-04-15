import os
from pathlib import Path
from uuid import uuid4

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain.prompts.chat import ChatPromptTemplate

from concurrent.futures import ThreadPoolExecutor, as_completed


def read_all_file_contents(read_files):
    """
    Convert the files into LangChain Document objects.
    """
    documents = []
    id = 0
    for file in read_files:
        new_doc = Document(
            page_content=file["contents"],
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

    """
    Summarize each file concurrently to reduce total token usage and speed up processing.
    """
    print(f"[⚡️] Summarizing {len(docs)} documents in parallel...")

    summarization_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a software engineer summarizing source code for internal documentation. "
        "You need to retain key technical elements without formatting it for external readability."
    ),
    (
        "user",
        """Summarize the following file while keeping all important implementation details.

        Include:
        - All function and class definitions (keep signatures and bodies)
        - Import statements
        - Core logic (retain control flow and important operations)
        - All environment variable usage (e.g., os.getenv, os.environ, process.env)

        Ignore:
        - Docstrings
        - Markdown formatting
        - Unnecessary comments

        You may simplify some repeated logic, but do not omit anything important.

        --- FILE START ---

        {code}

        --- FILE END ---"""
            )
        ])

    chain = summarization_prompt | model

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