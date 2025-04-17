from App.BackEnd.Seeding.priorities import *
from App.BackEnd.Seeding.icons import *

# Relationship
i1.priority = p1
i2.priority = p3
i3.priority = p4
i4.priority = p7
i5.priority = p8

def pop (session=None):
    # Priorities 
    session.add(p1)
    session.add(p2)
    session.add(p3)
    session.add(p4)
    session.add(p5)
    session.add(p6)
    session.add(p7)
    session.add(p8)

    # Icons
    session.add(i1)
    session.add(i2)
    session.add(i3)
    session.add(i4)
    session.add(i5)

    session.commit()