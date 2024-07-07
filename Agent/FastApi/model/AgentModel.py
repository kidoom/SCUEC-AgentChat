from pydantic import  BaseModel
from typing import  List
#Agent请求体
class PostAgentRequest(BaseModel):
    content:str

#Agent返回体
class AgentResponse(BaseModel):
    response: str


