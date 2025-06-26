from App.model.models.Priority import Priority

p0 = Priority(name='DEFAULT', color=None) 
p1 = Priority(name='CRITICAL', color='#ff0000')
p2 = Priority(name='REGULAR', color='#c7d0d8')
p3 = Priority(name='IMPORTANT', color='#ffd366')
p4 = Priority(name='FREE', color='#3f7237')
p5 = Priority(name='PERSONAL', color='#6141ac')

priorities = [p0, p1, p2, p3, p4, p5]