from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))


######################################################################
# RETURN HEALTH OF THE APP
######################################################################

@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture), 200
    return {"message": "person not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=['POST'])
def create_picture():
    picture_data = request.json
    if not picture_data:
        return {"message": "Invalid input parameter"}, 422

    try:
        data.append(picture_data)
    except NameError:
        return {"message": f"Picture with id {picture_id} already present"}, 500
    return {"message": "Picture created successfully"}, 200
######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Endpoint to update an existing picture"""
    picture_data = request.json

    # Find the picture in the data list
    for pic in data:
        if pic.get('id') == id:
            # Update the picture with the incoming request
            pic.update(picture_data)
            with open(json_url, 'w') as json_file:
                json.dump(data, json_file)
            return jsonify({"message": f"Picture with id {id} updated successfully"}), 200

    # If picture does not exist, return 404
    return jsonify({"message": "Picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for person in data:
        if person["id"] == id:
            data.remove(person)
            return '', 204
            
    return jsonify({"message": "Picture not found"}), 404

