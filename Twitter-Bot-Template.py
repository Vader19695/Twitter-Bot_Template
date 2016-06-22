from twython import Twython
import datetime, argparse

# Global
function_mappings = {
        "date_now": datetime.datetime.today().strftime("%A %B %d, %Y at %I:%M %p")
}

def main():
	# Load configuration
	configurationArray=GetConfiguration()	
	
	# Load parameters
	args=parseargs()
	
	# Define twitter
	twitter = Twython(configurationArray[0], configurationArray[1], configurationArray[2], configurationArray[3])

	# Retrive the status
	statusDisplay = GetStatus(vars(args))
	
	# Update status
	try:
		twitter.update_status(status=statusDisplay)
		Log("", statusDisplay, configurationArray[4])
	except Exception as e:
		Log("error", str(e), configurationArray[-1])

def GetStatus(args):
	if(args["function"].lower() == "countdown"):
		return str(args["message"]) % RemainingTime(args["date"])
	elif(args["function"].lower() == "standard"):
		return args["message"]
	elif(args["function"].lower() == "substitute"):
		return args["message"].split("\'")[1] % function_mappings[args["message"].split("\'")[-1].split("%")[-1].strip(" ")]
	else:
		print("Invalid Function!")
		exit(1)
			
def RemainingTime(date):
	return date

def parseargs():
	parser = argparse.ArgumentParser(prog="Twitter Bot")
	parser.add_argument("-f", "--function", help="Please enter the type of bot you wish to use. E.g.(Coutdown, Standard, Substitute)", required=True)
	parser.add_argument("-d", "--date", help="Please enter your date in the form: MM/DD/YYYY")
	parser.add_argument("-m", "--message", help="Please enter the message you wish to send.")
	args = parser.parse_args()

	return args

# Load the configuration from the config file
def GetConfiguration():
	# Local Variables
	config = []
	
	fr = open("config", "r")
	for line in fr.readlines():
		if "=" in line:
			config.append(line.split("=")[1].strip(" ").rstrip())

	return config
	

def Log(log_type, message, path):
	logger = open(path, "a")
	logger.write("[%s] %s: %s\n" % (function_mappings["date_now"], log_type.upper(), message))
	logger.close()
	
main()
