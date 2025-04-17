from App.model.seeds.models.Priority import priorities

def exec(session):
    session.add_all(priorities)
    session.commit()
