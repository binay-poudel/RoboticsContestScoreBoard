import webapp2, jinja2
import urllib
import os
import json

# Init template directory
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

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
    	js = get_file("http://ec2-52-36-61-88.us-west-2.compute.amazonaws.com/api/scoreboard/gpmp")
        robots =  json.loads(js).get("robots")
        for robot in robots:
        	print robot
        self.render("scoreboard.html", robots=robots)


def get_file(url):
	try:
		json_file = urllib.urlopen(url)
		return json_file.read()
	except IOError:
		return ""

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
