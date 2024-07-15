from io import BytesIO
import os
from pathlib import Path
from typing import BinaryIO
from zipfile import ZipFile

from dotenv import load_dotenv, find_dotenv
from langchain.schema import Document
from langchain.schema.output_parser import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.schema.runnable import RunnableParallel, RunnableLambda
from langchain.chains.combine_documents.reduce import ReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain
from langchain_community.callbacks import get_openai_callback

_ = load_dotenv(find_dotenv())


# The `DocumentService` class in Python provides functionality for processing and summarizing code
# files using map-reduce chains.
class DocumentService:
    def __init__(self):
        self.llm = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"], temperature=0, max_tokens=2500
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=10
        )
        self.code_extensions = {  # Web development
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
            # Python
            ".py",
            ".pyw",
            ".pyc",
            ".pyo",
            ".pyd",
            # Java
            ".java",
            ".class",
            # ".jar",
            # C and C++
            ".c",
            ".cpp",
            ".h",
            ".hpp",
            # C#
            ".cs",
            ".csx",
            # Ruby
            ".rb",
            ".rbw",
            # Go
            ".go",
            # Swift
            ".swift",
            # Kotlin
            ".kt",
            ".kts",
            # Rust
            ".rs",
            ".rlib",
            # Scala
            ".scala",
            ".sc",
            # Haskell
            ".hs",
            ".lhs",
            # Lua
            ".lua",
            # Perl
            ".pl",
            ".pm",
            # Shell scripting
            ".sh",
            ".bash",
            ".csh",
            ".tcsh",
            ".zsh",
            # SQL
            ".sql",
            # R
            ".r",
            ".R",
            # MATLAB
            ".m",
            # Visual Basic
            ".vb",
            ".vbs",
            # Objective-C
            ".m",
            ".mm",
            # Dart
            ".dart",
            # Groovy
            ".groovy",
            # PowerShell
            ".ps1",
            ".psm1",
            # TypeScript
            ".ts",
            ".tsx",
            # CoffeeScript
            ".coffee",
            # Erlang
            ".erl",
            ".hrl",
            # Fortran
            ".f",
            ".for",
            ".f90",
            # Lisp
            ".lisp",
            ".lsp",
            # Clojure
            ".clj",
            ".cljs",
            # Julia
            ".jl",
            # Elixir
            ".ex",
            ".exs",
            # F#
            ".fs",
            ".fsx",
            # COBOL
            ".cob",
            ".cbl",
            # Assembly
            ".asm",
            ".s",
            # D
            ".d",
            # Scheme
            ".scm",
            ".ss",
            # Prolog
            ".pl",
            ".pro",
            # Ada
            ".ada",
            ".adb",
            ".ads",
            # Tcl
            ".tcl",
            # Smalltalk
            ".st",
            # Verilog
            ".v",
            ".vh",
            ".sv",
            # VHDL
            ".vhd",
            ".vhdl",
            # Markdown (for documentation)
            ".md",
            ".markdown",
        }

        self.file_contents_chain = (
            RunnableLambda(lambda x: self.get_file_summary(x))
            | self.llm
            | StrOutputParser()
        )

    def unzip_file(self, file: BinaryIO) -> dict[str, str]:
        try:
            files = {}
            with ZipFile(BytesIO(file.read())) as read_zip_file:
                for file_name in read_zip_file.namelist():
                    if any(file_name.endswith(ext) for ext in self.code_extensions):
                        with read_zip_file.open(file_name) as curr_file:
                            content = curr_file.read().decode("utf-8")
                            directory = str(Path(file_name).parent) or "."

                            path_key = directory + "/" + file_name.replace(" ", "_")
                            files[path_key] = content
            return files
        except:
            return None

    def write_result_to_file(self, result: str, file_name: str):
        with open(file_name + ".md", "w") as file:
            file.write(result)

    def get_file_summary(self, file_contents):
        file_summary_prompt = """Concisely document the key content from the following code in a markdown format:
        {file_contents} 
        """

        files_summary_prompt_template = PromptTemplate.from_template(
            file_summary_prompt
        )

        return files_summary_prompt_template.format_prompt(file_contents=file_contents)

    def create_summary_chain(self, file_content):
        return (
            RunnableLambda(lambda x: self.get_file_summary(file_content))
            | self.llm
            | StrOutputParser()
        )

    def summarise_files(self, unzipped_files: dict[str, str]) -> str | None:
        parallel_tasks = {}
        # list_of_dicts = []

        for key, content in unzipped_files.items():
            parallel_tasks[key] = self.create_summary_chain(content)
        parallel_chain = RunnableParallel(**parallel_tasks)
        res = ""
        
        with get_openai_callback() as cb:
            results = parallel_chain.invoke({key: key for key in unzipped_files})
            i = 0
            for i, (key, value) in enumerate(results.items()):
                print(f"Summary for {key}: {value[:100]}...")  # Debug print
                self.write_result_to_file(value, f"summary_{i}")
                res += value

            self.write_result_to_file(res, "readmeee")
            print(cb)
        return res


document_service = DocumentService()
