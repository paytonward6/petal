import typing as t
from jinja2 import Environment, DictLoader
from pydantic import BaseModel


from .template import Template

class TemplateRegistry:
  def __init__(self, environment: t.Optional[Environment] = None):
    if environment is None:
      self._env = Environment()
    else:
      self._env = environment

    self._storage: dict[str, Template] = dict()

  def register(self, name: str, template: BaseModel, text: str):
    template = Template(name=name, attrs=template, text=text)
    self._storage[name] = template

  def unregister(self, name: str):
    del self._storage[name]

  def __getitem__(self, item):
    return self._storage[item]

  def load_templates(self):
    templates = {name: t.text for name, t in self._storage.items()}
    self._env.loader = DictLoader(templates)

  def unregister_all(self):
    self._storage = dict()


template_registry = TemplateRegistry()

