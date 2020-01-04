import logging
import os
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from models import Base


class Anbar:

    def __init__(self, engine: Engine):
        # type
        self._engine = engine
        self.session = sessionmaker(bind=engine)()

    def batch_save(self, obj_list: List[Base]) -> None:
        self.session.add_all(obj_list)
        self.session.commit()

    def save(self, obj: Base) -> None:
        self.session.add(obj)
        self.session.commit()


# creating Anbar. using factory design pattern
class AnbarFactory:

    @staticmethod
    def with_sqlite(db_name: str = os.getcwd()) -> Anbar:
        engine = create_engine("sqlite:///" + db_name, echo=False)
        return Anbar(engine)

    @staticmethod
    def with_postgres(host: str, port: str, username: str, password: str) -> Anbar:
        # TODO
        pass
