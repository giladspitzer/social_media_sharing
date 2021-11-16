from flask import jsonify, request, current_app
from flask_login import current_user
from backend.api.main import bp
from flask_login import login_required
from backend.models import SocialProfile, ProfileLookup
from backend.utils import query_string_decoder

@bp.route('/submit-profile', methods=['POST'])
@login_required
def submit_profile():
    account_data = request.json
    # TODO -- Implement validation for handles, img upload
    if sorted(['bio', 'phone', 'snap', 'insta', 'spotify', 'linkedin']) != sorted(account_data.keys()):
        return "Illegal Payload", 400
    current_user.social_profile.update(account_data)
    return "Success", 200


@bp.route('/profile/<p_id>')
@login_required
def register(p_id):
    if p_id == "me":
        profile = current_user.social_profile
    else:
        profile = SocialProfile.get(p_id)
    if profile is None:
        return "Invalid Payload", 404
    if profile.id != current_user.social_profile.id:
        ProfileLookup.create(current_user.id, profile.id)
    return jsonify(profile.jsonify())

@bp.route('/my-viewed')
@login_required
def get_my_viewed():
    page = query_string_decoder(request.query_string, 'page', 'int', 1)
    profiles = current_user.get_viewed(page)
    return jsonify([profile.jsonify() for profile in profiles])

@bp.route('/my-viewers')
@login_required
def get_my_viewers():
    page = query_string_decoder(request.query_string, 'page', 'int', 1)
    users = current_user.social_profile.get_viewers(page)
    return jsonify([user.social_profile.jsonify() for user in users])
