from abc import ABC, abstractmethod

class EncryptAlgorithm(ABC):
    secret_key = None
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    @abstractmethod
    def encrypt(self, message: str) -> str:
        pass
    @abstractmethod
    def decrypt(self, secret: str) -> str:
        pass
