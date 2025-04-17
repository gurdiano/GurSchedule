from App.BackEnd.Seeding.works import *
from App.BackEnd.Seeding.days import *
from App.BackEnd.Seeding.hours import *
from App.BackEnd.Seeding.icons import *
from App.BackEnd.Seeding.priorities import *
from App.BackEnd.Seeding.task import *

# Relationship
w1.icon = i2
w1.priority = p3
w2.icon = i2
w2.priority = p3
w3.icon = i3
w3.priority = p4
w4.icon = i2
w4.priority = p3
w5.icon = i4
w5.priority = p7
w6.icon = i1
w6.priority = p1
w7.icon = i4
w7.priority = p7
w8.icon = i4
w8.priority = p7
w9.icon = i5
w9.priority = p8
w10.icon = i1
w10.priority = p1

# Relationship
h1.day = d1
h2.day = d1
h3.day = d1
h4.day = d1
h5.day = d1
h6.day = d1
h7.day = d2
h8.day = d2
h9.day = d2
h10.day = d2
h11.day = d2
h12.day = d2
h13.day = d2
h19.day = d4
h14.day = d3
h15.day = d3
h16.day = d5
h17.day = d6
h18.day = d7

# Relationship
t1.hour = h1
t2.hour = h2
t3.hour = h3
t4.hour = h4
t5.hour = h5
t6.hour = h6
t7.hour = h7
t8.hour = h8
t9.hour = h9
t10.hour = h10
t11.hour = h11
t12.hour = h12
t13.hour = h13
t14.hour = h14
t15.hour = h15
t16.hour = h16
t17.hour = h17
t18.hour = h18
t19.hour = h19
t1.work = w1
t2.work = w1
t3.work = w2
t4.work = w2
t5.work = w2
t6.work = w2
t7.work = w3
t8.work = w4
t9.work = w4
t10.work = w5
t11.work = w5
t12.work = w5
t13.work = w5
t14.work = w6
t15.work = w4
t19.work = w7
t16.work = w8
t17.work = w9
t18.work = w10

def pop (session=None):
    # Works
    session.add(w1)
    session.add(w2)
    session.add(w3)
    session.add(w4)
    session.add(w5)
    session.add(w6)
    session.add(w7)
    session.add(w8)
    session.add(w9)
    session.add(w10)

    # Days
    session.add(d1)
    session.add(d2)
    session.add(d3)
    session.add(d4)
    session.add(d5)
    session.add(d6)
    session.add(d7)

    # Hours
    session.add(h1)
    session.add(h2)
    session.add(h3)
    session.add(h4)
    session.add(h5)
    session.add(h6)
    session.add(h7)
    session.add(h8)
    session.add(h9)
    session.add(h10)
    session.add(h11)
    session.add(h12)
    session.add(h13)
    session.add(h14)
    session.add(h15)
    session.add(h16)
    session.add(h17)
    session.add(h18)
    session.add(h19)

    # Task
    session.add(t1)
    session.add(t2)
    session.add(t3)
    session.add(t4)
    session.add(t5)
    session.add(t6)
    session.add(t7)
    session.add(t8)
    session.add(t9)
    session.add(t10)
    session.add(t11)
    session.add(t12)
    session.add(t13)
    session.add(t14)
    session.add(t15)
    session.add(t16)
    session.add(t17)
    session.add(t18)
    session.add(t19)

    session.commit()
