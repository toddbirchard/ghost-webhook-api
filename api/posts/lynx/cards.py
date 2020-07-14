"""Replace <a> tags in Lynx posts with cards."""
import re
import simplejson as json
from api.log import LOGGER
from .scrape import scrape_link
from .doc import mobile_doc


@LOGGER.catch
def format_lynx_posts(post):
    """Replace <a> tags in Lynx posts with link previews."""
    html = post.get('html')
    links = re.findall('<a href="(.*?)"', html)
    link_previews = [scrape_link(link) for link in links]
    try:
        link_previews.remove(None)
    except ValueError:
        pass
    mobile_doc['cards'] = link_previews
    for i, link in enumerate(link_previews):
        mobile_doc['sections'].append([10, i])
    return json.dumps(mobile_doc)
