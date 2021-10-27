"""Defines database models for our game's classes in Flask"""

from main import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Game(db.Model):
    """Class for a Beer Game individual game"""

    __tablename__ = "Game"

    id = db.Column(db.Integer, primary_key=True)
    session_length = db.Column(db.Integer, nullable=False)
    distributor_present = db.Column(db.Boolean, nullable=False)
    wholesaler_present = db.Column(db.Boolean, nullable=False)
    holding_cost = db.Column(db.Integer, nullable=False)
    backlog_cost = db.Column(db.Integer, nullable=False)
    session_id = db.Column(db.Integer, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('Instructor.id'))
    instructor = db.relationship("Instructor", backref=db.backref("Instructor", uselist=True), foreign_keys=[instructor_id])
    active = db.Column(db.Integer, nullable=False)
    info_sharing = db.Column(db.Integer, nullable=False)
    info_delay = db.Column(db.Integer, nullable=False)
    rounds_complete = db.Column(db.Integer, nullable=False)
    is_default_game = db.Column(db.Boolean, nullable=False)
    starting_inventory = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Game {}>'.format(self.id)

class Instructor(db.Model):
    """Class for a Beer Game instructor"""

    __tablename__ = "Instructor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    default_game = db.Column(db.Integer, db.ForeignKey('Game.id'))
    game = db.relationship("Game", backref=db.backref("game_instructor", uselist=False), foreign_keys=[default_game])

    def __repr__(self):
        return '<Instructor {}>'.format(self.id)

class Student(db.Model):
    """Class for a Beer Game instructor"""

    __tablename__ = "Student"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('Game.id'))
    student_game_id = db.relationship("Game", backref=db.backref('student_id', uselist=False), foreign_keys=[game_id])

class Demand(db.Model):
    """Class for demand pattern"""
    __tablename__ = "Demand"

    # Concept of Composite Key
    id = db.Column(db.Integer, db.ForeignKey('Game.id'), primary_key=True, autoincrement=True)
    demand = db.Column(db.Integer)
    week_number = db.Column(db.Integer)
    demand_id_fr = db.relationship("Game", backref=db.backref('demand_id_frk', uselist=False), foreign_keys=[id])

class DemandPattern(db.Model):
    """ A relationship Table for Demand ID and Demand"""
    game_id = db.Column(db.Integer, primary_key=True)
    demand = db.Column(db.Integer, primary_key=True)
    back_order = db.Column(db.Integer)
    week_number = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<DemandPattern {}>'.format(self.id)

class Order(db.Model):
    """Class for order pattern"""

    __tablename__ = "order_table"
    # Concept of Composite Key
    id = db.Column(db.Integer, db.ForeignKey('Game.id'), primary_key=True, autoincrement=True)
    order_amount = db.Column(db.Integer)
    week_number = db.Column(db.Integer)
    order_id_fr = db.relationship("Game", backref=db.backref('order_id_frk', uselist=False), foreign_keys=[id])

class OrderPattern(db.Model):
    """ A relationship Table for Demand ID and Demand"""

    __tablename__ = "order_pattern"


    game_id = db.Column(db.Integer, primary_key=True)
    order_amount = db.Column(db.Integer, primary_key=True)
    back_order = db.Column(db.Integer)
    week_number = db.Column(db.Integer, primary_key=True)
    