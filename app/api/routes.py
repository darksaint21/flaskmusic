from flask import Blueprint, request, jsonify, render_template
from helper import token_required
from models import db, User, Playlist, playlist_schema, playlists_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/playlists', methods = ['POST'])
@token_required
def create_contact(current_user_token):
    title = request.json['title']
    artist = request.json['artist']
    length = request.json['length']
    album = request.json['album']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    contact = Playlist(album, title, artist, length, user_token=user_token)

    db.session.add(contact)
    db.session.commit()

    response = playlist_schema.dump(Playlist)
    return jsonify(response)

@api.route('/playlists', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    Playlist = Playlist.query.filter_by(user_token = a_user).all()
    response = playlists_schema.dump(Playlist)
    return jsonify(response)



@api.route('/playlists/<id>', methods = ['GET'])
@token_required
def get_single_contact(current_user_token, id):
    Playlist = Playlist.query.get(id)
    response = playlist_schema.dump(Playlist)
    return jsonify(response)
    

# Update endpoint
@api.route('/playlists/<id>', methods = ['POST', 'PUT'])
@token_required
def update_contact(current_user_token, id):
    Playlist = Playlist.query.get(id)
    Playlist.title = request.json['title']
    Playlist.artist = request.json['artist']
    Playlist.length = request.json['length']
    Playlist.album = request.json['album']
    Playlist.user_token = current_user_token.token

    db.session.commit()
    response = playlist_schema.dump(Playlist)
    return jsonify(response)

# Delete endpoint
@api.route('/playlists/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    Playlist = Playlist.query.get(id)
    db.session.delete(Playlist)
    db.session.commit()
    response = playlist_schema.dump(Playlist)
    return jsonify(response)