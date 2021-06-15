from flask import Blueprint, request, session

from module.favorite import Favorite

favorite = Blueprint('favorite', __name__)

@favorite.route('/favorite', methods=['POST'])
def add_favorite():
    articleid = request.form.get('articleid')
    if session.get('islogin') is None:
        return 'not-login'
    else:
        try:
            Favorite().insert_favorite(articleid)
            return 'favorite-pass'
        except:
            return 'favorite-fail'

@favorite.route('/favorite/<int:articleid>', methods=['DELETE'])
def cancel_favorite(articleid):
    try:
        Favorite().cancel_favorite(articleid)
        return 'cancel-pass'
    except:
        return 'cancel-fail'

