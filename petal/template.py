import typing
from pydantic import BaseModel
from jinja2 import meta

from ._utils import eprint


class Template(BaseModel):
    name: str
    attrs: type[BaseModel]
    text: str


def get_globals(env, template_name: str) -> set[str]:
  source, filename, uptodate = env.loader.get_source(env, template_name)
  assert env.loader is not None

  template_ast = env.parse(source)
  return meta.find_undeclared_variables(template_ast)


def update_name(curr_name, name):
  return name if curr_name == "" else f"{curr_name}.{name}"


def schema_path(schema: dict, path: str):
  def get_nd(d, keys):
      if not keys:
          return d
      return get_nd(d[keys[0]], keys[1:]) 

  _, *p = path.split("/")
  return get_nd(schema, p)


def _recurse_attrs(curr_property, curr_name, schema, cumulative):
  for name, definition in curr_property.items():
    if "anyOf" in definition:
      # TODO: not holistic, fix
      curr_property = definition["anyOf"][0]
      curr_name = update_name(curr_name, name)

      # An object, find it
      if "$ref" in curr_property:
        curr_property = schema_path(schema, curr_property["$ref"])["properties"]
        return _recurse_attrs(curr_property, curr_name, schema, cumulative)
      else:
        cumulative.append(curr_name)
        continue

    # # list[_]
    # elif typing.get_origin(curr_type) is list:
    #   curr_type = typing.get_origin(curr_type)
    #   curr_name = update_name(curr_name, name)
    #   return _recurse_attrs(curr_type, curr_name, cumulative)
    elif "$ref" in definition:
      curr_name = update_name(curr_name, name)
      curr_property = schema_path(schema, definition["$ref"])["properties"]
      return _recurse_attrs(curr_property, curr_name, schema, cumulative)

    cumulative.append(update_name(curr_name, name))
  return cumulative


def recurse_attrs(template: Template, hyphenate: bool = True):
  init_type = template.attrs
  schema = init_type.model_json_schema()
  # eprint(init_type)
  acc = []
  attrs = _recurse_attrs(schema["properties"], "", schema, acc)
  if hyphenate:
    _hyphenate = lambda x: f"--{x}"
    return [_hyphenate(x) for x in attrs]

  return attrs
