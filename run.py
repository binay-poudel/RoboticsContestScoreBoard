import webapp2, jinja2
import urllib2
import os
import json
from datetime import datetime
import time

# Init template directory
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

# Scoreboard url
scoreboard_url = "http://{0}:8090/api/scoreboard/gpmp".format(os.environ["SERVER_IP"])

# Cache for score data
CACHE = None
last_updated = None

# Cache expires in 30 seconds
cache_lifetime = 30

# Page refreshes in 30000 milliseconds
refresh_duration = 30000

# Main handler class
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):  # write out a string to browser
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template) # gets template
        return t.render(params) # render template with parameters

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

# Handler for scoreboard page
class MainPage(Handler):
    def get(self):
        global last_updated, CACHE, scoreboard_url

        request_params = self.request.GET

        auto_refresh = None
        try:
            refresh_param = int(request_params['refresh'])
            if refresh_param in [0,1]:
              auto_refresh = bool(refresh_param)
        except KeyError:
            pass

        if not is_cache_expired():
            self.render(
              "scoreboard.html",
              robots=CACHE,
              time_diff=get_time_diff(),
              auto_refresh=auto_refresh,
              refresh_duration=refresh_duration)
            return

        # make a get request from scoreboard api
        js = get_request(scoreboard_url)

	try:
            robots =  json.loads(js).get("robots")

            # update cache
            last_updated = time.time()
            CACHE = robots
        except ValueError:
            self.write("Scoreboard not available at the moment.")
            return

        self.render(
          "scoreboard.html",
          robots=CACHE,
          time_diff=get_time_diff(),
          auto_refresh=auto_refresh,
          refresh_duration=refresh_duration)

# Checks if cache is expired or not by comparing
# current time with time cache got last updated
def is_cache_expired():
    global last_updated

    if not last_updated:
        return True

    if get_time_diff() > cache_lifetime:
        return True

    return False

# Get time difference between now and time cache
# got last updated
def get_time_diff():
    global last_updated

    if not last_updated:
        return 0

    #now = get_time_in_sec(datetime.utcnow())
    now = time.time()
    return int(now - last_updated)

# Sends a get request to specified url and returns data
def get_request(url):
    try:
        json_file = urllib2.urlopen(url, timeout=30)
        return json_file.read()
    except IOError:
        return ""

# Application
app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
