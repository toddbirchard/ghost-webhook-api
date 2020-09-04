"""Author management."""
from flask import current_app as api
from flask import make_response, request, jsonify
from clients.log import LOGGER
from clients import sms


@LOGGER.catch
@api.route('/authors/posts/created', methods=['POST'])
def author_created_post_notification():
    """Notify admin upon author post creation."""
    data = request.get_json()['post']['current']
    title = data['title']
    image = data.get('feature_image', None)
    status = data.get('status')
    author_name = data['primary_author']['name']
    author_slug = data['primary_author']['slug']
    if author_slug != 'todd':
        action_taken = 'UPDATED'
        if status != 'draft':
            action_taken = 'PUBLISHED'
        msg = f'{author_name} just {action_taken} a post: `{title}`.'
        if image is None and data['primary_tag']['slug'] != 'roundup':
            msg = msg.join([msg, 'Needs feature image.'])
            LOGGER.info(f'SMS notification triggered by post edit: {msg}')
            sms.send_message(msg)
        return make_response(msg, 200)
    return make_response(jsonify({'response': f'Author is {author_name}, carry on.'}), 204)
