"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Get all family members
@app.route('/members', methods=['GET'])
def get_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# Retrieve one member
@app.route('/member/<int:id>', methods=['GET'])
def get_one_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"msg":"Member does not exists"}), 401

# Add new member
@app.route('/member', methods=['POST'])
def add_new_member():
    new_member = request.json

    if new_member:
        jackson_family.add_member(new_member)
        return jsonify({"msg":"New member added"}), 200
    else:
        return jsonify({"msg":"Failed to add new member"}), 400

# Delete one member  
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_one_member(id):
    member = jackson_family.delete_member(id)
    if member:
        print("Member deleted")
        response = {
            "done": True
        }
        return jsonify(response), 200
    else:
        return jsonify({"msg":"Member does not exists"}), 401

# Update member
@app.route('/update-member/<int:id>', methods=['PUT'])
def update_member(id):
    member = request.json
        if not member:
        return jsonify({"msg":"Invalid member"}), 401
    jackson_family.update_member(id, member)
    return jsonify(member)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
