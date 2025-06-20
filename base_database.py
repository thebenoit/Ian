from abc import ABC, abstractmethod
from typing import List


class BaseDatabase(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """name of the database"""
        raise NotImplementedError
    
    @property
    @abstractmethod
    def collection_name(self) -> List[str]:
        """names of the collections"""
        raise NotImplementedError
    
    @property
    @abstractmethod
    def url(self) -> str:
        """url of the database"""
        raise NotImplementedError
    
    @abstractmethod
    def search(self, query: str) -> List[dict]:
        """search for a listing in the database"""
        raise NotImplementedError
    
    @abstractmethod
    def insert(self, data: dict) -> None:
        """insert a listing in the database"""
        raise NotImplementedError
    
    @abstractmethod
    def update(self, data: dict) -> None:
        """update a listing in the database"""
        raise NotImplementedError
    
