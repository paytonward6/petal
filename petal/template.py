from pydantic import BaseModel
from jinja2 import meta

from ._utils import eprint


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


def _recurse_attrs(curr_type, curr_name, cumulative):
  for name, value in curr_type.model_fields.items():
    annotation = value.annotation

    # Unions: only supports typing.Optional at the moment
    if hasattr(annotation, "__args__"):
      union_type =  annotation.__args__
      curr_type = union_type[0]
      curr_name = update_name(curr_name, name)

      if issubclass(curr_type, BaseModel):
        return _recurse_attrs(curr_type, curr_name, cumulative)
      else:
        cumulative.append(curr_name)
        continue

    elif issubclass(annotation, BaseModel):
      curr_name = update_name(curr_name, name)
      return _recurse_attrs(annotation, curr_name, cumulative)

    cumulative.append(update_name(curr_name, name))
  return cumulative

for i in range(10):
  print(i)


def recurse_attrs(template: Template, hyphenate: bool = True):
  init_type = type(template.attrs)
  acc = []
  attrs = _recurse_attrs(init_type, "", acc)
  if hyphenate:
    _hyphenate = lambda x: f"--{x}"
    return [_hyphenate(x) for x in attrs]
  
  return attrs
