import ConfigParser, datetime
from os import path
from twython import Twython
import pyCron

######## Global Vars #########
Config = ConfigParser.ConfigParser()

"""
Eventually this will be replaced to remove the *.default check
Replace with *.cfg check
"""
def LoadConfiguration(user):
	if(path.isfile("config.cfg.default")):
		# Log("Exists!")
		Config.read("config.cfg.default")
	else:
		# Log("Does not exist!")
		# exit()
		Config.read("config.cfg")
	options=Config.options(user)
	"""
	Iterate over options loaded for the section
	Load into a dictionary dict1
	"""
	dict1 = {}
	for option in options:
		try:
			dict1[option] = Config.get(user, option)
		except:
			dict1[option] = None

	return dict1

def LoadPolls():
	if(path.isfile("polls.cfg.default")):
		Config.read("polls.cfg.default")
	else:
		Config.read("polls.cfg")
	polls = {}
	names=Config.sections()
	for name in names:
		options=Config.options(name)
		polls[name] = pyCron.Poll(Config.get(name, "time"), GenerateStatus, 
					dict(
						user=Config.get(name, "user"),
						function=Config.get(name, "function"),
						date=Config.get(name, "date"),
						message=Config.get(name, "message"),
						substitute_message=Config.get(name, "substitute_message")
					)
				)
	return polls

def LoadTwitterAccount(user):
	configurationDict = LoadConfiguration(user)
	try:
		twitter = Twython(configurationDict["app_key"], configurationDict["app_secret"], configurationDict["oauth_token"], configurationDict["oauth_token_secret"])
	except:
		print("There was an issue with your configuration!")
	return twitter

def GenerateStatus(name, time, user, function, date=None, message="", substitute_message=None):
	twitter = LoadTwitterAccount(user)
	if(function.lower() == "countdown"):
		final_message=(message % RemainingTime(date))
	elif(function.lower() == "functional"):
		final_message=(message % eval(substitute_message))
	elif(function.lower() == "substitute"):
		final_message=(message % substitute_message)
	elif(function.lower() == "standard"):
		final_message=(message)
	else:
		exit(0)
		
	try:
		twitter.update_status(status=final_message)
	except:
		exit(1)
	
def RemainingTime(date):
	today=datetime.date.today()
	date_array=date.split("/")
	future_date=datetime.date(int(date_array[2]), int(date_array[0]), int(date_array[1]))
	date_delta = (future_date-today).days
	
	if(date_delta > 1):
		return("in %s days" % str(date_delta))
	elif(date_delta == 1):
		return("tomorrow")
	elif(date_delta == 0):
		return("today")
	else:
		exit(1)

polls=LoadPolls()

for name, poll in polls.iteritems():
	#print(name)
	pyCron.add_poll(name, poll)

if __name__ == "__main__":
	pyCron.run_Cron()
