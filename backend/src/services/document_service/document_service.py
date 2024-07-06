from io import BytesIO
import os
from pathlib import Path
from typing import BinaryIO
from zipfile import ZipFile

from typing import Any
from dotenv import load_dotenv, find_dotenv
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, TokenTextSplitter
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.reduce import ReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain

_ = load_dotenv(find_dotenv())


class DocumentService:
    def __init__(self):
        self.llm = OpenAI(api_key=os.environ["OPENAI_API_KEY"], temperature=0.2)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=10
        )
        self.files = {}
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

    def unzip_file(self, file: BinaryIO) -> Any:
        """
        The `unzip_file` function reads a zip file, extracts files with specified code extensions, and
        stores their content in a dictionary based on their directory.

        :param file: The `file` parameter in the `unzip_file` method is expected to be a BinaryIO object,
        which represents a binary input/output stream. This method reads the content of the provided zip
        file, extracts files with specific code extensions, and stores the extracted file content in a
        dictionary based on their
        :type file: BinaryIO
        """
        with ZipFile(BytesIO(file.read())) as read_zip_file:
            for file_name in read_zip_file.namelist():
                if any(file_name.endswith(ext) for ext in self.code_extensions):
                    with read_zip_file.open(file_name) as curr_file:
                        content = curr_file.read().decode("utf-8")
                        directory = str(Path(file_name).parent) or "."

                        if directory not in self.files:
                            self.files[directory] = []

                        self.files[directory].append((file_name, content))

    def summarise_files(self):
        """
        This Python function processes files by splitting their content into chunks, creating documents with
        metadata, and then running a series of chain operations to summarize and rearrange the
        documentations.
        :return: The `summarise_files` method returns the result of running the `map_reduce_chain` on the
        list of documents (`docs`). The result is the output generated by processing the documents through
        the entire chain of operations defined in the method.
        """
        text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)

        docs = []
        for directory, files in self.files.items():
            for file_name, content in files:
                chunks = text_splitter.split_text(content)
                docs.extend(
                    [
                        Document(
                            page_content=chunk,
                            metadata={
                                "file_name": f"{file_name} (Part {i+1}/{len(chunks)}"
                            },
                        )
                        for i, chunk in enumerate(chunks)
                    ]
                )

        # Map chain
        map_template = """Concisely document the key functions/routes from the following code snippets:
        {content} 
        """
        map_prompt = PromptTemplate.from_template(map_template)
        map_chain = LLMChain(prompt=map_prompt, llm=self.llm)

        # Reduce chain
        reduce_template = """Here are the concise documentations of each file:
        {code_summaries}
        
        Rearrange them into a markdown format with headings for each part
        """
        reduce_prompt = PromptTemplate.from_template(reduce_template)
        reduce_chain = LLMChain(prompt=reduce_prompt, llm=self.llm)

        # Stuff chain
        stuff_chain = StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="code_summaries"
        )

        # Reduce documents chain
        reduce_documents_chain = ReduceDocumentsChain(
            combine_documents_chain=stuff_chain
        )

        # Map-reduce chain
        map_reduce_chain = MapReduceDocumentsChain(
            llm_chain=map_chain,
            document_variable_name="content",
            reduce_documents_chain=reduce_documents_chain,
        )

        # Run the chain
        result = map_reduce_chain.run(docs)
        
        with open("resultant.md", "w") as file:
            file.write(result)
            
        return result


document_service = DocumentService()
