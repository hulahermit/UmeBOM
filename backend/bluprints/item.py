from . import item_bp
from .. import db
import re
from sqlalchemy import event
from flask import jsonify

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)
    type = db.Column(db.String(40), nullable=True)
    cost = db.Column(db.Float, nullable=True)
    unit = db.Column(db.String(40), nullable=True)
    note = db.Column(db.Text, nullable=True)
    chart_of_accounts_id = db.Column(db.Integer, nullable=True)

    @staticmethod
    def get_next_name():
        items = Item.query.all()
        numbers = []
        for item in items:
            match = re.match(r'^\d{5}', item.name)
            if match:
                numbers.append(int(match.group()))
        if numbers:
            next_number = max(numbers) + 1
        else:
            next_number = 10000
        return str(next_number).zfill(5)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'cost': self.cost,
            'unit': self.unit,
            'note': self.note,
            'chart_of_accounts_id': self.chart_of_accounts_id
        }
        
@event.listens_for(Item.__table__, 'after_create')
def insert_initial_items(*args, **kwargs):
    print('Creating demo records...')
    db.session.add(Item(name='10001', description='Item 1', type='Manufactured', cost=10.0, unit='EA', chart_of_accounts_id=4, note = 'This is a note'))
    db.session.add(Item(name='10002', description='Item 2', type='Manufactured', cost=15.0, unit='EA', chart_of_accounts_id=4))
    db.session.add(Item(name='10003', description='Item 3', type='Manufactured', cost=20.0, unit='EA', chart_of_accounts_id=4))
    db.session.add(Item(name='10004', description='Item 4', type='Purchased', cost=25.0, unit='EA', chart_of_accounts_id=4))
    db.session.add(Item(name='10005', description='Item 5', type='Purchased', cost=30.0, unit='EA', chart_of_accounts_id=4))
    db.session.commit()

@item_bp.route('/items', methods=['GET'])
def get_item():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

