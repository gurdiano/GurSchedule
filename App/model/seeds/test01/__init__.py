from .relationships import resolve_relationship
from .scripts.script import exec

_all__ = ['create_test01']

def create_test01(session):
    resolve_relationship()
    exec(session)