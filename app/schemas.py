from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.messages import BaseMessage
from typing import List


class Input(BaseModel):
    input: str
    chat_history: List[BaseMessage] = Field(
        ...,
        extra={"widget": {"type": "chat", "input": "location"}},
    )


class Output(BaseModel):
    output: str
