

from audit_tarcker.config import get_connection
from flask import blueprints, request, Blueprint,jsonify

mango_base=Blueprint("base",__name__)
# to delete data in mongodb
@mango_base.route('/admin/delete_data', methods=['DELETE'])
def delete_data():
    del_query="""truncate table audit_report"""
    with get_connection() as conn:
        pointer = conn.cursor()
        pointer.execute(del_query)
    return jsonify({"message":"data deleted from data base..."})


