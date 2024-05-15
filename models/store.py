from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
     # lazy="dynamic" tells python to not load the items until you tell it to
     # cascade="all, delete"  tells python to delete all items upon store delete
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete" )