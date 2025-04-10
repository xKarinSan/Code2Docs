from langchain.schema import BaseOutputParser
class SimpleOutputParser(BaseOutputParser):
    def parse(self, text: str) -> str:
        return text.strip()