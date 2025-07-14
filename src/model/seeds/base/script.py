from .icons import *
from .priorities import *

def exec(session):
    for i, priority in enumerate(priorities):
        priority.icon = icons[i]
    
    session.add_all(priorities)
    session.add_all(other_icons)
    session.commit()