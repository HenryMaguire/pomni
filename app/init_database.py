import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()



class Story(Base):
    """docstring for Story."""

    __tablename__ = 'story'
    id = Column(Integer, primary_key = True)
    story_text = String(550)
    ## Add JSON feature so that external applications could
    ## access the story data without all the HTML and CSS
    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return {
            'id'          :self.id,
            'story'         :self.story
            }

####### AT END OF FILE #######

engine =create_engine(
    'sqlite:///stories.db')
Base.metadata.create_all(engine)
