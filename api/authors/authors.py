from flask import current_app as api
from flask import make_response, request, jsonify
from api.log import logger
from api import sms


@logger.catch
@api.route('/authors/posts/created', methods=['POST'])
def author_created_post_notification():
    data = request.get_json()['post']['current']
    title = data['title']
    image = data.get('feature_image', None)
    excerpt = data.get('custom_excerpt', None)
    status = data.get('status')
    author_name = data['primary_author']['name']
    author_slug = data['primary_author']['slug']
    if author_slug != 'todd':
        action = 'updated'
        if status != 'draft':
            action = 'PUBLISHED'
        msg = f'{author_name} just {action} `{title}`: {excerpt}.'
        if image is None:
            msg = msg.join([msg, 'Needs feature image.'])
            logger.info(f'Message sent: {msg}')
            sms.send_message(msg)
        return make_response(msg, 200)
    return make_response(jsonify({'response': f'Author is {author_name}, carry on.'}), 204)
