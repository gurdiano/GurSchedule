from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import relationship, declarative_base

from App.BackEnd.Entities.colorenum import PriorityColor as Priority

Base = declarative_base()


class Day(Base):
    __tablename__= 'tb_day'

    date  = Column(Date, primary_key=True)

    hours = relationship('Hour', back_populates='day')

    def __repr__(self):
        return f'<Day(date={self.date})>'
    
class Hour(Base):
    __tablename__ = 'tb_hour'

    id = Column(Integer, primary_key=True)
    hour = Column(Integer, nullable=True)
    day_id = Column(Date, ForeignKey('tb_day.date'))

    day = relationship('Day', back_populates='hours')
    tasks = relationship('Task', back_populates='hour')
    
    __table_args__ = (
        UniqueConstraint('hour', 'day_id'),
    )

    def __repr__ (self):
        return f'<Hour(hour={self.hour})>'

class Work(Base):
    __tablename__ = 'tb_work'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    duration = Column(Integer, nullable=True)
    annotation = Column(String, nullable=True)

    priority_id = Column(Integer, ForeignKey('tb_priority.id'), nullable=False)
    icon_id = Column(Integer, ForeignKey('tb_icon.id'), nullable=True)

    priority = relationship('Priority', back_populates='works')
    icon = relationship('Icon', back_populates='works')
    tasks = relationship('Task', back_populates='work')

    __table_args__ = (
        UniqueConstraint('name', 'duration'),
    )

    def __repr__(self):
        return f'<Work(name={self.name}, duration={self.duration}, annotation={self.annotation}, priority={self.priority}, icon={self.icon})>'
    
class Task(Base):
    __tablename__ = 'tb_task'
    
    id = Column(Integer, primary_key=True)
    beginning = Column(Time, nullable=False)
    hour_id = Column(Integer, ForeignKey('tb_hour.id'), nullable=False)
    work_id = Column(Integer, ForeignKey('tb_work.id'), nullable=False)

    hour = relationship('Hour', back_populates='tasks')
    work = relationship('Work', back_populates='tasks')

    __table_args__ = (
        UniqueConstraint('hour_id', 'work_id'),
    )

    def __repr__(self):
        return f'<Task(beginning = {self.beginning})>'
    
class Icon(Base):
    __tablename__ = 'tb_icon'

    id = Column(Integer, primary_key=True)
    src = Column(String, nullable=False)
    icon_id = Column(Integer, ForeignKey('tb_priority.id'), nullable=False)
    
    priority = relationship('Priority', back_populates='icons')
    works = relationship('Work', back_populates='icon')

    def __repr__(self):
        return f'Icon<id ={self.id}, src={self.src}>'
    
class Priority(Base):
    __tablename__ = 'tb_priority'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    color = Column(String, nullable=True)
    
    icons = relationship('Icon', back_populates='priority')
    works = relationship('Work', back_populates='priority')


    def __repr__(self):
        return f'Priority<id = {self.id}, name={self.name}, color={self.color}>'

 