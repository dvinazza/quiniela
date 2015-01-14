#!/usr/bin/python
# -*- coding: utf -*-

from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String, UniqueConstraint, Date
from sqlalchemy.orm import scoped_session, sessionmaker


class Datos():
    def __init__(self, echo=False):

        self.db = create_engine('sqlite:///datos.sqlite',
                                convert_unicode=True,
                                echo=echo)
        # encoding defaults to utf8
        self.metadata = MetaData(bind=self.db)
        self.session = scoped_session(sessionmaker(self.db, autoflush=True,
                                                   autocommit=True))

        try:
            self.quinielas = Table('quinielas', self.metadata, autoload=True)
        except:
            self.quinielas = Table('quinielas', self.metadata,
                                   Column('fecha', Date),
                                   Column('dia', Integer),
                                   Column('tipo', String(3)),
                                   Column('pos', Integer),
                                   Column('numero', Integer),
                                   Column('parteA', Integer),
                                   Column('parteB', Integer),
                                   UniqueConstraint('fecha', 'tipo', 'pos'))
            self.quinielas.create()


