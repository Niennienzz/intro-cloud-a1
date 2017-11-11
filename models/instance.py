from db import db


class EC2InstanceModel(db.Model):
    """EC2InstanceModel provides AWS EC2 instance data model ORM.

        It saves instance ID for an EC2 instance in database.
        It provides the get-all helper.

        Schema:
            CREATE TABLE instances (
                id INTEGER NOT NULL,
                instance VARCHAR(64),
                PRIMARY KEY (id)
            )
    """

    __tablename__ = 'instances'

    id = db.Column(db.Integer, primary_key=True)
    instance = db.Column(db.String(64))

    def __init__(self, instance):
        self.instance = instance

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_instance_id(cls, instance):
        return cls.query.filter_by(instance=instance).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()
