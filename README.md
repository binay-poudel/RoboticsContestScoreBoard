# Public Scoreboard for Trinity's Robotics Contest
The scoreboard data is fetched from the main scoring system server. The data is cached locally and updated at certain interval (currently 30 seconds).

# To test app locally
`/path_to_app_engine/dev_appserver.py .`

# To deploy to app engine
`/path_to_app_engine/appcfg.py --oauth2_credential_file=~/.appcfg_oauth2_tokens_personal update  .`

The app is hosted on Google App Engine (GAE) account: `robotics.scoring.test@gmail.com` with a project ID: `contestscoreboard.` The option `--oauth2_credential_file=~/.appcfg_oauth2_tokens_personal` is needed only if you have different GAE accounts you are working with locally and would like to specify which one.

# Requirements
- Python 2.7.6
- Google App Engine
