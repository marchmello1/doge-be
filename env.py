import os
from dotenv import load_dotenv

load_dotenv()

class Environment:
    XAI_KEY:str=os.getenv("XAI_KEY")

    @classmethod
    def to_dict(cls):
        return {key: value for key, value in cls.__dict__.items() if not key.startswith('__')}

env = Environment()
