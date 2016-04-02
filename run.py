import webapp2, jinja2
import urllib
import os
import json
from datetime import datetime

# Init template directory
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

# Scoreboard url
scoreboard_url = "http://ec2-52-36-61-88.us-west-2.compute.amazonaws.com/api/scoreboard/gpmp"

# Cache for score data
CACHE = None
last_updated = None

# Cache expires in 30 seconds
cache_lifetime = 30

# Main handler class
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):  # write out a string to browser
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template) # gets template
        return t.render(params) # render template with parameters

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
        global last_updated, CACHE, scoreboard_url

        if not is_cache_expired():
            self.render("scoreboard.html", robots=CACHE, time_diff=get_time_diff())
            return

        js = get_request(scoreboard_url)
        robots =  json.loads(js).get("robots")

        # update cache
        last_updated = get_time_in_sec(datetime.utcnow())
        CACHE = robots

        self.render("scoreboard.html", robots=CACHE, time_diff=get_time_diff())

def is_cache_expired():
    global last_updated

    if not last_updated:
        return True

    if get_time_diff() > cache_lifetime:
        return True

    return False

def get_time_diff():
    global last_updated

    if not last_updated:
        return 0

    now = get_time_in_sec(datetime.utcnow())
    return now - last_updated

def get_time_in_sec(time):
    return time.second + time.minute * 60 + time.hour * 3600

def get_request(url):
    try:
        json_file = urllib.urlopen(url)
        return json_file.read()
    except IOError:
        return ""

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
