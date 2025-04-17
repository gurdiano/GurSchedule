from App.model.seeds.models import days, tasks, schedulers

def exec(session):
    session.add_all(days)
    session.add_all(tasks)
    session.add_all(schedulers)
    session.commit()