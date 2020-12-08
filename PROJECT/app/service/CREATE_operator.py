from app import db


def add_object_to_db(cls, **kwargs):
    obj = cls()
    for atr, value in kwargs.items():
        setattr(obj, atr, value)

    db.session.add(obj)
    db.session.commit()

    return obj
