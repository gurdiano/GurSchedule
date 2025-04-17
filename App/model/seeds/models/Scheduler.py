from App.model.models.Scheduler import Scheduler
from datetime import time

s0 = Scheduler(hour=15, begin=time(15, 0))
s1 = Scheduler(hour=16, begin=time(16, 0))
s2 = Scheduler(hour=17, begin=time(17, 0))
s3 = Scheduler(hour=18, begin=time(18, 0))
s4 = Scheduler(hour=19, begin=time(19, 0))
s5 = Scheduler(hour=20, begin=time(20, 0))

s6 = Scheduler(hour=10, begin=time(10, 0))
s7 = Scheduler(hour=11, begin=time(11, 0))
s8 = Scheduler(hour=12, begin=time(12, 0))
s9 = Scheduler(hour=13, begin=time(13, 0))
s10 = Scheduler(hour=14, begin=time(14, 0))
s11 = Scheduler(hour=15, begin=time(15, 0))
s12 = Scheduler(hour=16, begin=time(16, 0))

s13 = Scheduler(hour=11, begin=time(11, 0))
s14 = Scheduler(hour=12, begin=time(12, 0))

s15 = Scheduler(hour=23, begin=time(23, 0))
s16 = Scheduler(hour=22, begin=time(22, 0))
s17 = Scheduler(hour=11, begin=time(11, 0))
s18 = Scheduler(hour=13, begin=time(13, 0))

schedulers = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18]