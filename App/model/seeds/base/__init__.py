from .relationship import resolve
from .script import exec

def create_base(session):
    resolve()
    exec(session)