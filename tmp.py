import typing
from pydantic import BaseModel

class Port(BaseModel):
    num: int

class Deploy(BaseModel):
    ports: list[Port]



hints = typing.get_type_hints(Deploy)
print(typing.get_origin(hints["ports"]) is list)
print(typing.get_args(hints["ports"]))
print(typing.get_args(hints["ports"]))
