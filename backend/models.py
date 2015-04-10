#-*- coding: utf-8 -*-

from sqlalchemy import Column, DateTime, String, Text, Integer, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Log(Base):
    __tablename__ = "log"
    
    id = Column(Integer, primary_key=True)
    host = Column(String)
    event = Column(String)
    event_desc = Column(Text)
    obj = Column(String)
    obj_desc = Column(Text)
    subj = Column(String)
    subj_desc = Column(Text)
    result = Column(String)
    result_desc = Column(Text)
    timestamp = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return """
        <log id="{0}">
            <host>{1}</host>
            <event>{2}</event>
            <event_desc>{3}</event_desc>
            <obj>{4}</obj>
            <obj_desc>{5}</obj_desc>
            <subj>{6}</subj>
            <subj_desc>{7}</subj_desc>
            <result>{8}</result>
            <result_desc>{9}</result_desc>
            <timestamp>{10}</timestamp>
        </log>
        """.format(str(self.id), self.host, self.event, self.event_desc, 
        self.obj, self.obj_desc, self.subj, self.subj_desc, self.result, 
        self.result_desc, str(self.timestamp.isoformat()))
