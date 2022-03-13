from app import app, db
from flask import jsonify


@app.route('/', methods=['GET'])
def test():

    artists = db.search_artists('t')

    return jsonify(artists.to_dict('records'))