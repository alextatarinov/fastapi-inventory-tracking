import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Config:
    DATABASE_URL: str


@lru_cache
def get_config() -> Config:
    return Config(
        os.environ['DATABASE_URL']
    )
