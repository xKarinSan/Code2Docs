import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

from .file_processes import document_code_file,summarize_doc
async def run_all(read_files: list,model):
    async def wrapped(file):
        # async with semaphore:
        await asyncio.to_thread(document_code_file, file["filePath"], file["contents"], file["extension"],model)
    tasks = [wrapped(file) for file in read_files]
    await asyncio.gather(*tasks)
    
def summarize_documents(docs, model, max_workers=6):
    """
    Summarize each file concurrently to reduce total token usage and speed up processing.
    """
    print(f"[⚡️] Summarizing {len(docs)} documents in parallel...")
    
    summaries = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_doc = {executor.submit(summarize_doc, doc,model): doc for doc in docs}
        for future in as_completed(future_to_doc):
            result = future.result()
            if result:
                summaries.append(result)
    
    return summaries