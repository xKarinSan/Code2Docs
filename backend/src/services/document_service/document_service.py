from io import BytesIO
import os
from pathlib import Path
from typing import BinaryIO
from zipfile import ZipFile

from dotenv import load_dotenv, find_dotenv
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.reduce import ReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain

_ = load_dotenv(find_dotenv())


# The `DocumentService` class in Python provides functionality for processing and summarizing code
# files using map-reduce chains.
class DocumentService:
    def __init__(self):
        self.llm = OpenAI(api_key=os.environ["OPENAI_API_KEY"], temperature=0)
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

    def unzip_file(self, file: BinaryIO) -> dict[str, str]:
        """
        The `unzip_file` function reads a zip file, extracts files with specified code extensions, and
        returns a dictionary mapping directories to lists of file names and their contents.

        :param file: The `unzip_file` method takes a file object (`file`) as input, which is expected to be
        a binary file. The method reads the binary content of the file, treats it as a zip file, and then
        extracts the contents of the zip file. The extracted files are stored in a
        :type file: BinaryIO
        :return: A dictionary containing the extracted files from the input zip file. The keys of the
        dictionary represent the directories where the files were located within the zip file, and the
        values are lists of tuples. Each tuple contains the file name and its content as a string.
        """
        try:
            files = {}
            with ZipFile(BytesIO(file.read())) as read_zip_file:
                for file_name in read_zip_file.namelist():
                    if any(file_name.endswith(ext) for ext in self.code_extensions):
                        with read_zip_file.open(file_name) as curr_file:
                            content = curr_file.read().decode("utf-8")
                            directory = str(Path(file_name).parent) or "."

                            if directory not in files:
                                files[directory] = []

                            files[directory].append((file_name, content))
            return files
        except:
            return None

    def create_documents(self, unzipped_files: dict[str, str]) -> list[Document]:
        """
        The `create_documents` function takes a dictionary of unzipped files, splits the content into chunks
        using a text splitter, and creates a list of Document objects with metadata including the file name
        and part number.

        :param unzipped_files: `unzipped_files` is a dictionary where the keys are directory names and the
        values are dictionaries where the keys are file names and the values are the content of the files as
        strings
        :type unzipped_files: dict[str, str]
        :return: A list of `Document` objects is being returned.
        """
        docs = []
        for directory, files in unzipped_files.items():
            for file_name, content in files:
                chunks = self.text_splitter.split_text(content)
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
        return docs

    def create_map_chain(self) -> LLMChain:
        """
        This function creates a map chain with a prompt template for documenting key functions/routes.
        :return: The `create_map_chain` method returns an instance of `LLMChain` with a prompt template that
        documents key functions/routes from code snippets.
        """
        map_template = """Concisely document the key functions/routes from the following code snippets:
        {content} 
        """
        map_prompt = PromptTemplate.from_template(map_template)
        return LLMChain(prompt=map_prompt, llm=self.llm)

    def create_reduce_chain(self) -> LLMChain:
        """
        This function creates a reduce chain with concise documentations for each file in a markdown format
        with headings for each part.
        :return: The `create_reduce_chain` method returns an instance of `LLMChain` with a prompt generated
        from the `reduce_template` string and the `llm` attribute of the class instance. The prompt is
        created using a `PromptTemplate` from the `reduce_template` string.
        """
        reduce_template = """Here are the concise documentations of each file:
        {code_summaries}
        
        Rearrange them into a markdown format with headings for each part
        """
        reduce_prompt = PromptTemplate.from_template(reduce_template)
        return LLMChain(prompt=reduce_prompt, llm=self.llm)

    def create_stuff_chain(self, reduce_chain: LLMChain) -> StuffDocumentsChain:
        """
        The function `create_stuff_chain` creates a `StuffDocumentsChain` object with a specified
        `llm_chain` and `document_variable_name`.

        :param reduce_chain: Reduce_chain is an instance of the LLMChain class, which is passed as a
        parameter to the create_stuff_chain method
        :type reduce_chain: LLMChain
        :return: An instance of `StuffDocumentsChain` is being returned with the `llm_chain` attribute set
        to the `reduce_chain` parameter and the `document_variable_name` attribute set to "code_summaries".
        """
        return StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="code_summaries"
        )

    def create_reduce_documents_chain(
        self, stuff_chain: StuffDocumentsChain
    ) -> ReduceDocumentsChain:
        """
        The function `create_reduce_documents_chain` creates a `ReduceDocumentsChain` object with a
        `combine_documents_chain` attribute set to the input `stuff_chain`.

        :param stuff_chain: StuffDocumentsChain object that contains a chain of documents to be processed
        :type stuff_chain: StuffDocumentsChain
        :return: An instance of ReduceDocumentsChain with the combine_documents_chain attribute set to the
        provided stuff_chain.
        """
        return ReduceDocumentsChain(combine_documents_chain=stuff_chain)

    def create_map_reduce_chain(
        self, map_chain: LLMChain, reduce_documents_chain: ReduceDocumentsChain
    ) -> MapReduceDocumentsChain:
        """
        The function `create_map_reduce_chain` creates a MapReduceDocumentsChain object with specified map
        and reduce chains.

        :param map_chain: The `map_chain` parameter in the `create_map_reduce_chain` function is expected to
        be an instance of the `LLMChain` class. This parameter represents the chain of map operations that
        will be applied during the map phase of the MapReduce process
        :type map_chain: LLMChain
        :param reduce_documents_chain: The `reduce_documents_chain` parameter in the
        `create_map_reduce_chain` function is of type `ReduceDocumentsChain`. It is used to specify the
        chain of reduce operations that will be applied to the mapped documents in the MapReduce process
        :type reduce_documents_chain: ReduceDocumentsChain
        :return: MapReduceDocumentsChain object is being returned with the specified parameters - llm_chain,
        document_variable_name, and reduce_documents_chain.
        """
        return MapReduceDocumentsChain(
            llm_chain=map_chain,
            document_variable_name="content",
            reduce_documents_chain=reduce_documents_chain,
        )

    def write_result_to_file(self, result: str):
        """
        The function `write_result_to_file` writes the given result string to a file named "resultant.md".

        :param result: The `write_result_to_file` method takes a string `result` as a parameter, which
        represents the content that will be written to a file named "resultant.md". The method opens the
        file in write mode ("w") and writes the content of the `result` string to the file
        :type result: str
        """
        with open("resultant.md", "w") as file:
            file.write(result)

    def summarise_files(self, unzipped_files: dict[str, str]) -> str | None:
        """
        The function `summarise_files` processes unzipped files using map-reduce chains and writes the
        result to a file.

        :param unzipped_files: The `unzipped_files` parameter is a dictionary where the keys are strings
        representing file names and the values are strings representing the content of the files after they
        have been unzipped
        :type unzipped_files: dict[str, str]
        :return: The `summarise_files` method returns a string, which is the result of running the
        `map_reduce_chain` on the documents and then writing the result to a file.
        """
        try:
            docs = self.create_documents(unzipped_files)
            map_chain = self.create_map_chain()
            reduce_chain = self.create_reduce_chain()
            stuff_chain = self.create_stuff_chain(reduce_chain)
            reduce_documents_chain = self.create_reduce_documents_chain(stuff_chain)
            map_reduce_chain = self.create_map_reduce_chain(
                map_chain, reduce_documents_chain
            )

            result = map_reduce_chain.run(docs)
            self.write_result_to_file(result)
            return result
        except:
            return None


document_service = DocumentService()
