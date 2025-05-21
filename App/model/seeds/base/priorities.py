from App.model.models.Priority import Priority

p0 = Priority(name='CRITICAL', color='#ff0000')
p1 = Priority(name='ESSENTIAL', color='#fe9218')
p2 = Priority(name='IMPORTANT', color='#ffd366')
p3 = Priority(name='REGULAR', color='#c7d0d8')
p4 = Priority(name='OPPORTUNITY', color='#036bb6')
p5 = Priority(name='FOLLOW', color='#1358d0')
p6 = Priority(name='PERSONAL', color='#6141ac')
p7 = Priority(name='FREE', color='#3f7237')
p8 = Priority(name='DEFAULT', color=None)

priorities = [p0, p1, p2, p3, p4, p5, p6, p7, p8]