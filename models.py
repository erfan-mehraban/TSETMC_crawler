import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Namaad(Base):
    __tablename__ = 'namaad'

    i = Column(Integer, primary_key=True)
    name = Column(String(64))
    overall_history = relationship("OverallHistoryRecord", back_populates="namaad")

    def __repr__(self):
        return "<Namaad i='%s', name='%s'>" % (self.i, self.name)


class OverallHistoryRecord(Base):
    __tablename__ = 'overall_histrory_record'

    id = Column(Integer, primary_key=True)
    namaad_id = Column(Integer, ForeignKey('namaad.i'))
    namaad = relationship("Namaad", back_populates="overall_history")
    max_value = Column(Integer)
    min_value = Column(Integer)
    closing_price = Column(Integer)
    last_trade_price = Column(Integer)
    first_price = Column(Integer)
    yesterday_price = Column(Integer)
    value = Column(Integer)
    volume = Column(Integer)
    count = Column(Integer)
    date = Column(DateTime)
