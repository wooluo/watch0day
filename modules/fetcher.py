from abc import ABC, abstractmethod
from typing import List, Dict

class Fetcher(ABC):
    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def fetch(self) -> List[Dict]:
        pass