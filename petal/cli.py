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

  # eprint(template)
  attrs = recurse_attrs(template, hyphenate=True)
  return attrs


class PetalArgumentParser(argparse.ArgumentParser):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.add_argument("--list-opts", required=False, default=None, action="store")
    self.add_argument("--autocomplete", required=False, action="store_true")

  def run(self):
    args = self.parse_args()

    if args.list_opts is not None:
      opts = handle_list_opts(args.list_opts)
      if opts:
        print(" ".join(opts))
    elif args.autocomplete:
      print(autocomplete())
    elif args.template is not None:
      template = template_registry[args.template]
      arg_names = recurse_attrs(template, hyphenate=False)
      arg_values = vars(args)
      for arg in arg_names:
          print(arg_values[arg])

