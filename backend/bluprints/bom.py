from . import bom_bp
from .. import db
from sqlalchemy import event
from flask import jsonify

class BOM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    line_number = db.Column(db.Integer, nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)

    parent_item = db.relationship('Item', foreign_keys=[parent_id], backref='parent')
    child_item = db.relationship('Item', foreign_keys=[child_id], backref='child')

    def to_dict(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'child_id': self.child_id,
            'quantity': self.quantity,
            # 'parent_number': self.parent_item.name,
            # 'parent_description': self.parent_item.description,
            'child_number': self.child_item.name,
            'child_description': self.child_item.description
        }
    
@event.listens_for(BOM.__table__, 'after_create')
def insert_initial_items(*args, **kwargs):
    db.session.add(BOM(parent_id='1', line_number='10', child_id='2', quantity=2))
    db.session.add(BOM(parent_id='1', line_number='20', child_id='3', quantity=1))
    db.session.add(BOM(parent_id='2', line_number='10', child_id='4', quantity=3))
    db.session.add(BOM(parent_id='2', line_number='20', child_id='5', quantity=2))

    db.session.commit()

@bom_bp.route('/bom', methods=['GET'])
def get_item():
    bom_list = BOM.query.all()
    return jsonify([line.to_dict() for line in bom_list])