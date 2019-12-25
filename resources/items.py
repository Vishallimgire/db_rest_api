from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.items import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
            'price',
            type=float,
            required=True,
            help='This field cannot be blank'
        )
    
    parser.add_argument(
            'store_id',
            type=int,
            required=True,
            help='Every item has an store_id'
        )

    @jwt_required()
    def get(self, name):
        items = ItemModel.item_by_name(name)
        if items:
            return items.json()
        return {'message':'item is not found'}, 404

    
    def post(self, name):
        print(name)
        items = ItemModel.item_by_name(name)
        # print('items___',items)
        if items:
            return {'message': f'Item has already exists with {name} name'}, 400
        data = self.parser.parse_args()
        item = ItemModel(name, **data)
        # print(item)
        try:
            item.save_to_db()
        except Exception as e:
            print(e)
            return {'message':'Error occured'}, 500
        else:
            return item.json(), 201

    def delete(self, name):
        item = ItemModel.item_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'items deleted'}
    
    def put(self, name):       
        data = Item.parser.parse_args()
        item = ItemModel.item_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}