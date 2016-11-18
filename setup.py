from twython import Twython
import ConfigParser

#Global Vars
config = ConfigParser.ConfigParser()
config_file=open('config.cfg', 'w')
#DO NOT CHANGE THESE!
APP_KEY='zwgmMFgzPj3UMCT7cOD5jWOgU'
APP_SECRET='eMJ078aqryWt3fZZFDYZTda3Wvhv9Zu1AsEOwRyKDjRRPbmYF6'

get_auth = Twython(APP_KEY, APP_SECRET)
auth = get_auth.get_authentication_tokens()

OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']


print("Go to: %s" % auth['auth_url'])
oauth_verifier=raw_input("Enter the pin: ")

post_pin = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
final_step = post_pin.get_authorized_tokens(oauth_verifier)

OAUTH_TOKEN = final_step['oauth_token']
OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']

verify = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

username=verify.verify_credentials()['name']

config.add_section(username)
config.set(username, 'APP_KEY', APP_KEY)
config.set(username, 'APP_SECRET', APP_SECRET)
config.set(username, 'OAUTH_TOKEN', OAUTH_TOKEN)
config.set(username, 'OAUTH_TOKEN_SECRET', OAUTH_TOKEN_SECRET)

config.write(config_file)

print("Congratulations! The bot can now access your twitter account.")

