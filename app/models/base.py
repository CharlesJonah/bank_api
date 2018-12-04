"""Base model."""

from time import time

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.collections import InstrumentedList

db = SQLAlchemy()


class Base(db.Model):
    """Base model with all main requirements of a model."""

    __abstract__ = True

    created_at = db.Column(
        db.Float(), nullable=False, default=time())
    updated_at = db.Column(
        db.Float(), nullable=False, default=time())

    def save(self):
        """Save an object in the database."""
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            return {
                "message": "Ensure the object you're saving is valid.",
                "exception": str(e)
            }

    def update(self, new_data):
        """Update an object with new information."""
        all_keys = [key for key in self.__dict__]
        keys = [key for key in new_data]
        for key in keys:
            if key in all_keys:
                setattr(self, key, new_data[key])
            else:
                return {
                    "message": "Error encountered when setting attributes."
                }
        setattr(self, 'updated_at', time())
        self.save()

    def delete(self):
        """Delete an object from the database."""
        db.session.delete(self)
        db.session.commit()
        return True

    def serialize(self):
        """Convert sqlalchemy object to python dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def get_field(self, field):
        """Get the value in an object's field."""
        try:
            values = getattr(self, field)
            return values
        except AttributeError:
            return {
                "message": "Ensure the  field passed is valid.",
                "help": "The field should be an attribute of the object."
            }

    def insert(self, field, *values):
        """Insert values into a relationship field."""
        try:
            current_values = self.get_field(field)
            if isinstance(current_values, dict):
                return current_values
            elif isinstance(current_values, InstrumentedList):
                current_values.extend(list(values))
                self.save()
            else:
                setattr(self, field, values[0])
                self.save()
        except Exception as e:
            return {
                "message": "Ensure the fields and values are valid.",
                "exception": str(e)
            }

    def remove(self, field, **kwargs):
        """
        Remove values from a relationship field.

        This replaces the value with None or an empty list.
        Pass in the field and unique argument to isolate object for removal.
        """
        current_values = self.get_field(field)
        if isinstance(current_values, dict):
            return current_values
        elif isinstance(current_values, InstrumentedList):
            if kwargs:
                key = [i for i in kwargs][0]
                try:
                    item_index = current_values.index([
                        i for i in current_values
                        if getattr(i, key) == kwargs[key]
                    ][0])
                    current_values.pop(item_index)
                except Exception as e:
                    return {
                        "message": "Ensure the arguments passed are valid.",
                        "exception": str(e)
                    }
            else:
                setattr(self, field, InstrumentedList([]))
        else:
            setattr(self, field, None)
        self.save()

    @classmethod
    def exists(cls, **kwargs):
        """Checck if object with specific values exists."""
        result = cls.get(**kwargs)
        if isinstance(result, dict):
            return False
        else:
            return True

    @classmethod
    def drop(cls):
        """Delete all objects in a table."""
        for item in cls.query.all():
            item.delete()
        return True

    @classmethod
    def get(cls, **kwargs):
        """Get a specific object from the database."""
        result = cls.query.filter_by(**kwargs).first()
        if not result:
            return {"message": "The object does not exist."}
        return result

    @classmethod
    def get_all(cls):
        """Get all objects of a specific table."""
        result = cls.query.all()
        if not result:
            return {"message": "The class of objects do not exist."}
        return result
