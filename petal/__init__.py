#!/usr/bin/env python3

import typing as t

from pydantic import BaseModel

from .cli import PetalArgumentParser
from .registry import template_registry
from .autocomplete import autocomplete


class Range(BaseModel):
    top: int
    bottom: int

class Port(BaseModel):
    number: int
    type: t.Optional[str] = None
    range: Range

class Deployment(BaseModel):
    name: str
    image: str
    # TODO: make this a list
    ports: t.Optional[Port] = None


def main():
    parser = PetalArgumentParser()
    text = """
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: {{ name }}
    labels:
      app: {{ name }}
  spec:
    replicas: {{ replicas }}
    selector:
      matchLabels:
        app: {{ name }}
    template:
      metadata:
        labels:
          app: {{ name }}
      spec:
        containers:
        - name: nginx
          image: {{  image }}
          {% if ports %}
          ports:
          {% for port in ports %}
          - containerPort: {{ port.number }}
          {% endfor %} {% endif %}
  
    """
    template = Deployment(
      name="nginx",
      image="nginx-1.1",
      ports=Port(number=8080, range=Range(top=1, bottom=7))
    )
    template_registry.register("deployment", template, text)
    template_registry.register("this", template, text)
    template_registry.load_templates()
  
  
    parser.run()
  

if __name__ == "__main__":
  main()
