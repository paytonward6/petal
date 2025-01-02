from pydantic import BaseModel

from pydantic._internal._typing_extra import (
  is_union,
  get_model_type_hints
)
from pydantic._internal._generics import (
  get_args
)


def is_model(tp) -> bool:
  try:
    return issubclass(tp, BaseModel)
  except TypeError:
    return False


__all__ = (
  "is_model",
  "is_union",
  "get_model_type_hints",
  "get_args"
)
