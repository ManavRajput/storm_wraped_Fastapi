from typing import List
from knowledge_storm.interface import Retriever, Information

class MockRetriever(Retriever):
    def __init__(self):
        super().__init__(rm=None)

    def retrieve(self, queries: List[str], exclude_urls: List[str] = []) -> List[Information]:
        dummy_snippets = [
            f"{query} is a well-known concept with broad implications in the modern world."
            for query in queries
        ]
        info = Information(source_url=f"https://example.com", snippets=dummy_snippets)
        return [info]

