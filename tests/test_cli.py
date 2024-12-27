import typing as t

import pytest
from pydantic import BaseModel

from petal.registry import template_registry
from petal.cli import handle_list_opts

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

@pytest.mark.parametrize("arg,want", [
        ("", ["deployment1234", "deployment5678", "other"]),
        ("de", ["deployment1234", "deployment5678", "other"]),
        ("deployment1", ["deployment1234", "deployment5678", "other"]),
        ("deployment1234", ["--name", "--image", "--ports.number", "--ports.type"]),
    ]
)
def test_handle_list_opts(arg, want):
  template_registry.register("deployment1234", template, text)
  template_registry.register("deployment5678", template, text)
  template_registry.register("other", template, text)
  template_registry.load_templates()

  assert want == handle_list_opts(arg)

