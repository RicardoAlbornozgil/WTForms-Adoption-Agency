"""SQLAlchemy models for WTForms-Adoption Agency."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://mylostpetalert.com/wp-content/themes/mlpa-child/images/nophoto.gif"
class Pet(db.Model):
    """Individual Pets"""
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer)
    photo_url = db.Column(db.Text)
    notes = db.Column(db.Text)  
    available = db.Column(db.Boolean)  

    # Define species_id as a foreign key referencing Species.id
    species_id = db.Column(db.Integer, db.ForeignKey('species.id', ondelete='CASCADE'), nullable=False)
    
    # Define a relationship to Species without cascade delete
    species = db.relationship("Species", backref="pets", single_parent=True)

    def image_url(self):
        """Return image for pet -- bespoke or generic."""
        return self.photo_url or DEFAULT_IMAGE_URL


class Species(db.Model):
    """Different Species"""
    __tablename__ = "species"
    
    id = db.Column(db.Integer, primary_key=True)
    species_name = db.Column(db.Text, nullable=False)


def connect_db(app):
    """Connect this database Flask app."""
    db.app = app
    db.init_app(app)
