# Public Scoreboard for Trinity's Robotics Contest
The scoreboard data is fetched from the main scoring system server. The data is cached locally and updated at certain interval (currently 30 seconds).

# To test app locally
`/path_to_app_engine/dev_appserver.py .`

# To deploy to app engine
- Authenticate the Google App Engine API (so that resources can be assigned) using auth json (which can be obtained from GAE console) with command `gcloud auth activate-service-account --key-file ./<auth json>`
- Authenticate Google Account by loginning in using `gcloud auth login`
- Set environmental variable SERVER\_IP that points to IP address of the scoring server
- Deploy using `gcloud app deploy`

# Requirements
- Python 2.7.6
- Google App Engine
