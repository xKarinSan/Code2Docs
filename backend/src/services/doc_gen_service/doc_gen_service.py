import os
from io import BytesIO
from pathlib import Path
from typing import BinaryIO, Dict, List, Any
from zipfile import ZipFile
from dotenv import load_dotenv, find_dotenv
from langchain.schema.output_parser import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import (
    RunnableParallel,
    RunnableLambda,
    RunnableSerializable,
)
from datetime import datetime

from backend.src.services.db_service.db import get_db
from backend.src.services.codebase_service.codebase_service import codebase_service
from backend.src.services.db_service.models.DocModel import DocModel
from backend.src.services.db_service.models.DocSetModel import DocSetModel
import json

# OPENAI_MODEL


# The `DocumentService` class provides methods for summarizing and documenting code files.
class DocumentService:
    def __init__(self):
        _ = load_dotenv(find_dotenv())
        self.llm = ChatOpenAI(
            model=os.environ["OPENAI_MODEL"],
            api_key=os.environ["OPENAI_API_KEY"],
            temperature=0,
            max_tokens=2500,
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=10
        )
        self.code_extensions = self._get_code_extensions()

    # ================ for the GenAI integration ================
    def _get_code_extensions(self) -> set:
        # Move the long list of extensions to a separate method
        return {
            ".html",
            ".htm",
            ".css",
            ".js",
            ".jsx",
            ".ts",
            ".tsx",
            ".php",
            ".asp",
            ".aspx",
            ".py",
            ".pyw",
            ".pyc",
            ".pyo",
            ".pyd",
            ".java",
            ".class",
            ".c",
            ".cpp",
            ".h",
            ".hpp",
            ".cs",
            ".csx",
            ".rb",
            ".rbw",
            ".go",
            ".swift",
            ".kt",
            ".kts",
            ".rs",
            ".rlib",
            ".scala",
            ".sc",
            ".hs",
            ".lhs",
            ".lua",
            ".pl",
            ".pm",
            ".sh",
            ".bash",
            ".csh",
            ".tcsh",
            ".zsh",
            ".sql",
            ".r",
            ".R",
            ".m",
            ".vb",
            ".vbs",
            ".dart",
            ".groovy",
            ".ps1",
            ".psm1",
            ".coffee",
            ".erl",
            ".hrl",
            ".f",
            ".for",
            ".f90",
            ".lisp",
            ".lsp",
            ".clj",
            ".cljs",
            ".jl",
            ".ex",
            ".exs",
            ".fs",
            ".fsx",
            ".cob",
            ".cbl",
            ".asm",
            ".s",
            ".d",
            ".scm",
            ".ss",
            ".ada",
            ".adb",
            ".ads",
            ".tcl",
            ".st",
            ".v",
            ".vh",
            ".sv",
            ".vhd",
            ".vhdl",
            ".md",
            ".markdown",
        }

    def unzip_file(self, file: BinaryIO) -> Dict[str, str] | None:
        """
        The `unzip_file` function reads a zip file, extracts text files with specified extensions, and
        returns a dictionary mapping file paths to their contents.

        :param file: The `unzip_file` method takes a file object (`file`) as input, which is expected to be
        a binary file. The method attempts to unzip the contents of the provided zip file and extract text
        content from files with specific code extensions. The extracted content is stored in a dictionary
        where the keys
        :type file: BinaryIO
        :return: The `unzip_file` method returns a dictionary where the keys are file paths and the values
        are the content of the files extracted from the provided zip file. If an exception occurs during the
        extraction process, it returns `None`.
        """
        try:
            files = {}
            with ZipFile(BytesIO(file.read())) as read_zip_file:
                for file_name in read_zip_file.namelist():
                    if any(file_name.endswith(ext) for ext in self.code_extensions):
                        with read_zip_file.open(file_name) as curr_file:
                            content = curr_file.read()
                            # .decode("utf-8")
                            directory = str(Path(file_name).parent) or "."
                            path_key = f"{directory}/{file_name.replace(' ', '_')}"
                            files[path_key] = content
            return files
        except Exception as e:
            print("E:", e)
            return None

    def get_file_summary(self, file_contents: str) -> PromptTemplate:
        """
        The function `get_file_summary` takes in a string of file contents and returns a formatted markdown
        prompt template with the file contents included.

        :param file_contents: The `get_file_summary` method takes in a string `file_contents` as input and
        returns a formatted prompt template using the provided `file_contents` in a markdown format. The
        `PromptTemplate` class is used to create the template, and the `format_prompt` method is used to
        substitute the
        :type file_contents: str
        :return: The function `get_file_summary` returns a formatted prompt template that documents the key
        content from the provided `file_contents` in a markdown format.
        """
        file_summary_prompt = """Concisely document the key content from the following code in a markdown format:

        {file_contents}
        """
        return PromptTemplate.from_template(file_summary_prompt).format_prompt(
            file_contents=file_contents
        )

    def create_summary_chain(self, file_content: str) -> RunnableSerializable:
        """
        The function `create_summary_chain` returns a chain of operations to process file content and
        generate a summary.

        :param file_content: The `file_content` parameter is a string that contains the content of a file.
        It is used as input to the `create_summary_chain` method to generate a summary chain for the file
        content
        :type file_content: str
        :return: A chain of operations is being returned, which includes a lambda function that calls the
        `get_file_summary` method on the `file_content`, followed by the `llm` operation, and finally the
        `StrOutputParser` operation.
        """
        return (
            RunnableLambda(lambda x: self.get_file_summary(file_content))
            | self.llm
            | StrOutputParser()
        )

    def summarise_files_demo(self, unzipped_files: Dict[str, str]) -> str | None:
        """
        The function `summarise_files` processes unzipped files in parallel to create summaries and write
        them to files.

        :param unzipped_files: The `unzipped_files` parameter is a dictionary where the keys are file names
        and the values are the content of the files. The `summarise_files` method takes this dictionary as
        input, processes the content of each file in parallel using a summary chain, writes the individual
        summaries to files
        :type unzipped_files: Dict[str, str]
        :return: The `summarise_files` method returns the full summary of the files processed, or `None` if
        an exception occurs during the processing.
        """
        try:
            parallel_tasks = {
                key: self.create_summary_chain(content)
                for key, content in unzipped_files.items()
            }
            parallel_chain = RunnableParallel(**parallel_tasks)
            results = parallel_chain.invoke({key: key for key in unzipped_files})

            summaries = []
            for _, (_, value) in enumerate(results.items()):
                # self.write_result_to_file(value,f"summary_{i}")
                summaries.append(value)

            full_summary = "\n\n".join(summaries)
            # self.write_result_to_file(full_summary,"result")
            return full_summary
        except Exception as e:
            print(e)
            return None

    def summarise_files(self, unzipped_files: Dict[str, str]) -> List[str] | None:
        try:
            parallel_tasks = {
                key: self.create_summary_chain(content)
                for key, content in unzipped_files.items()
            }
            parallel_chain = RunnableParallel(**parallel_tasks)
            results = parallel_chain.invoke({key: key for key in unzipped_files})

            summaries = []
            print(results.items())
            for _, (file_name, contents) in enumerate(results.items()):
                # self.write_result_to_file(value,f"summary_{i}")
                summaries.append({"file_name": file_name, "contents": contents})

            # full_summary = "\n\n".join(summaries)
            # self.write_result_to_file(full_summary, "result")
            return summaries
        except Exception as e:
            print(e)
            return None

    # def write_result_to_file(self, result: str, file_name: str):
    #     """
    #     NOTE: THIS IS TO BE REMOVED DURING PRODUCTION

    #     The function `_write_result_to_file` writes the given result to a file with the specified file name
    #     in Markdown format.

    #     :param result: The `result` parameter in the `_write_result_to_file` method is a string that
    #     contains the data or content that you want to write to a file
    #     :type result: str
    #     :param file_name: The `file_name` parameter is a string that represents the name of the file where
    #     the result will be written. In the `_write_result_to_file` method, the `result` string will be
    #     written to a file with the name specified by the `file_name` parameter
    #     :type file_name: str
    #     """
    #     with open(f"{file_name}.md", "w") as file:
    #         file.write(result)


doc_gen_service = DocumentService()
