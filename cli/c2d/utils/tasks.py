import asyncio
from .file_processes import document_code_file
async def run_all(read_files: list,model):
    async def wrapped(file):
        # async with semaphore:
        await asyncio.to_thread(document_code_file, file["filePath"], file["contents"], file["extension"],model)
    tasks = [wrapped(file) for file in read_files]
    await asyncio.gather(*tasks)