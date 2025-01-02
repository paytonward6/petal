from pydantic import BaseModel

from jinja2 import meta

from ._utils import eprint
from ._internal import *


class Template(BaseModel):
    name: str
    attrs: BaseModel
    text: str


def get_globals(env, template_name: str) -> set[str]:
  source, filename, uptodate = env.loader.get_source(env, template_name)
  assert env.loader is not None

  template_ast = env.parse(source)
  return meta.find_undeclared_variables(template_ast)


def update_name(curr_name, name):
  return name if curr_name == "" else f"{curr_name}.{name}"

def _recurse_union(curr_type, curr_name, cumulative):
    curr_type =  get_args(curr_type)[0]
    _recurse_attrs(curr_type, curr_name, cumulative)


def _recurse_attrs(curr_type, curr_name: list[str], cumulative):
  types = get_model_type_hints(curr_type).items()
  if len(types) == 0:
    cumulative.append(".".join(curr_name))
    return

  for name, (tp, success) in types:
    if not success:
      raise Exception("Failed to parse type")

    curr_name.append(name)

    if is_model(tp):
      _recurse_attrs(tp, curr_name, cumulative)

    elif is_union(tp):
      _recurse_union(tp, curr_name, cumulative)

    else:
      cumulative.append(".".join(curr_name))

    curr_name.pop()


def recurse_attrs(template: Template, hyphenate: bool = True):
  init_type = type(template.attrs)
  acc = []
  _recurse_attrs(init_type, [], acc)
  if hyphenate:
    _hyphenate = lambda x: f"--{x}"
    return [_hyphenate(x) for x in acc]
  
  return acc

