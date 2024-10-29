from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

Base = declarative_base()

class Actor(Base):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    login = Column(String(255), unique=True, nullable=False)
    avatar_url = Column(String(1024))
    events = relationship("Event", back_populates="actor")


class Repository(Base):
    __tablename__ = 'repositories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    events = relationship("Event", back_populates="repository")


class Event(Base):
    __tablename__ = 'events'
    id = Column(String(255), primary_key=True)  # Event IDs are strings in GitHub
    type = Column(String(255))
    actor_id = Column(Integer, ForeignKey('actors.id'))
    repo_id = Column(Integer, ForeignKey('repositories.id'))
    created_at = Column(DateTime)

    actor = relationship("Actor", back_populates="events")
    repository = relationship("Repository", back_populates="events")

    __table_args__ = (UniqueConstraint('id', name='_event_id_uc'),)
