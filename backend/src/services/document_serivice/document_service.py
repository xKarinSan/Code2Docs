from io import BytesIO
import os
from typing import BinaryIO
from zipfile import ZipFile

from dotenv import load_dotenv, find_dotenv
from langchain.document_loaders import Blob
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAI

_ = load_dotenv(find_dotenv())

class DocumentService:
    def __init__(self):
        self.llm = OpenAI(api_key=os.environ["OPENAI_API_KEY"], temperature=0.2)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=10
        )
        self.files = []
        self.code_extensions = { # Web development
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
            ".markdown",}


    def generate_docs(self, contents):
        """
        Load & index files
        """
        # Implement this method if needed

    def unzip_file(self, file: BinaryIO) -> None:
        read_zip_file = ZipFile(BytesIO(file.read()))

        for file_name in read_zip_file.namelist():
            if any(file_name.endswith(ext) for ext in self.code_extensions):
                with read_zip_file.open(file_name) as curr_file:
                    content = curr_file.read()
                    blob = Blob(data=content, mime_type="text/plain")
                    self.files.append((file_name, blob))

    def summarise_files(self):
        for file_name, blob in self.files:
            content = blob.as_string()
            doc = Document(page_content=content, metadata={"source": file_name})
            chain = load_summarize_chain(llm=self.llm, chain_type="map_reduce")
            summary = chain.run([doc])  # Pass a list containing the file
            print("summary: ", summary)

document_service = DocumentService()
