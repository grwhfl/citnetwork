from typing import List, Union
from dataclasses import dataclass
from pydantic import BaseModel


class XInput(BaseModel):
    data: str


@dataclass
class ModelResponse:
    recomendations: Union[List[str], str]
