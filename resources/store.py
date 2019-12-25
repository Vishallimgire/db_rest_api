from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store_info = StoreModel.find_by_name(name)
        if store_info:
            return store_info.json()
        return {'message':'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'Store is already exist {name}'}, 400
        store_model = StoreModel(name)
        try:
            store_model.save_to_db()
        except:
            return {'message':'Problem in storing db'}, 500
        return store_model.json()

    def delete(self, name):
        store_model = StoreModel.find_by_name(name)
        try:
            store_model.delete_from_db()
        except Exception as e:
            print(e)
            return {'message':'Problem in deleting db'}, 500
        return {'message':f'Store Deleted successfully by name {name}'}

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}