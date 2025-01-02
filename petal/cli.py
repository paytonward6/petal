import argparse

from .registry import template_registry
from .template import recurse_attrs
from ._utils import eprint
from .autocomplete import autocomplete


def first_found(iterable, target, default=None):
    try:
      return iterable[iterable.index(target)]
    except ValueError:
      return default


def handle_list_opts(first_arg: str):
  templates = template_registry._env.list_templates()
  template_name = first_found(templates, first_arg)

  if template_name is None:
    return templates

  template = template_registry[template_name]

  attrs = recurse_attrs(template, hyphenate=True)
  return attrs


class PetalArgumentParser(argparse.ArgumentParser):
  def __init__(self):
    super().__init__()
    self.add_argument("--list-opts", required=False, action="store", default=None)
    self.add_argument("--autocomplete", required=False, action="store_true")

  def run(self):
    args = self.parse_args()

    if args.list_opts is not None:
      list_opts = args.list_opts.split(" ")[0]
      opts = handle_list_opts(list_opts)
      if opts:
        print(" ".join(opts))
    elif args.autocomplete:
      print(autocomplete())

