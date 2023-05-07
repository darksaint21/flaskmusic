from flask import Blueprint, request, jsonify, render_template
from helper import token_required
from models import db, User, Playlist, playlist_schema, playlists_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yaa':'oohh'}

@api.route('/playlists', methods = ['POST'])
@token_required
def create_playlist(current_user_token):
    artist = request.json['artist']
    song = request.json['song']
    album = request.json['album']
    length = request.json['length']
    
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    playlist = Playlist(artist, song, album, length, user_token=user_token)

    db.session.add(playlist)
    db.session.commit()

    response = playlist_schema.dump(playlist)
    return jsonify(response)

@api.route('/playlists', methods = ['GET'])
@token_required
def get_playlist(current_user_token):
    a_user = current_user_token.token
    playlists = Playlist.query.filter_by(user_token = a_user).all()
    response = playlists_schema.dump(playlists)
    return jsonify(response)

# Optional, (might not work)
# @api.route('/whiskeys/<id>', methods = ['GET'])
# @token_required
# def get_single_whiskey(current_user_token, id):
#    whiskeys = Whiskey.query.get(id)
#    response = whiskey_schema.dump(whiskeys)
#        return jsonify(response)

# Update endpoint
@api.route('/playlists/<id>', methods = ['GET', 'PUT'])
@token_required
def update_whiskey(current_user_token, id):
    playlist = Playlist.query.get(id)
    playlist.name = request.json['artist']
    playlist.brand = request.json['song']
    playlist.size = request.json['album']
    playlist.proof = request.json['length']
    
    playlist.user_token = current_user_token.token

    db.session.commit()
    response = playlist_schema.dump(playlist)
    return jsonify(response)

@api.route('/playlists/<id>', methods = ['DELETE'])
@token_required
def delete_playlist(current_user_token, id):
    playlist = Playlist.query.get(id)
    db.session.delete(playlist)
    db.session.commit()
    response = playlist_schema.dump(playlist)
    return jsonify(response)