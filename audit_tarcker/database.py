from audit_tarcker.config import collection
from flask import blueprints, request, Blueprint,jsonify

mango_base=Blueprint("base",__name__)
# to delete data in mongodb
@mango_base.route('/admin/delete_data', methods=['DELETE'])
def delete_data():
    collection.drop()
    return jsonify({"message":"data deleted from data base..."})


