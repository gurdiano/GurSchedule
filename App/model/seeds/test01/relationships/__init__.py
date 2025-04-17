from .tasks_rel import resolve as task_resolve
from .schedulers_rel_ import resolve as scheduler_resolve

__all__ = ['resolve_relationship']

def resolve_relationship():
    task_resolve()
    scheduler_resolve()

    
    