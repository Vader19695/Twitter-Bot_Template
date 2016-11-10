from twython import Twython
import datetime, argparse

# Global variables
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
	statusDisplay = GenerateStatus(vars(args), configurationArray)
	
	# Update status
	try:
		twitter.update_status(status=statusDisplay)
		Log("", statusDisplay, configurationArray[4])
	except Exception as e:
		Log("error", str(e), configurationArray[-1])

# Function will generate the twitter status
# Depends on the function selection
def GenerateStatus(args, configurationArray):
	
	
	# If function is countdown
	# Determine how long until specified date
	# Substitute into entered message
	if(args["function"].lower() == "countdown"):
		try:
			return str(args["message"]) % RemainingTime(args["date"], configurationArray)
		except Exception as e:
			Log("error", str(e), configurationArray[-1])
	
	# If function is standard
	# Return status as entered message
	elif(args["function"].lower() == "standard"):
		try:
			return args["message"]
		except Exception as e:
			Log("error", str(e), configurationArray[-1])
			
	# If function is substitute
	# Substitute specified function into entered message
	elif(args["function"].lower() == "substitute"):
		try:
			message_split = args["message"].split(" % ")
			if(message_split[-1].strip(" ") not in function_mappings):
				return message_split[0][1:-1] % message_split[-1].strip(" ")
			return message_split[0][1:-1] % function_mappings[message_split[-1].strip(" ")]
		except Exception as e:
			Log("error", str(e), configurationArray[-1])
	else:
		print("Invalid Function!")
		exit(1)
			
# Determine how long until specified date
def RemainingTime(date, configurationArray):
	# Local Variables
	today = datetime.date.today()
	date_array = date.split("/")
	future_date = datetime.date(int(date_array[2]), int(date_array[0]), int(date_array[1]))
	date_delta = (future_date-today).days
	
	if(date_delta > 1):
		return("in %s days!" % str(date_delta))
	elif(date_delta == 1):
		return("tomorrow!")
	elif(date_delta == 0):
		return("today!")
	elif(date_delta < 0):
		Log("error", "The date specified has already passed.", configurationArray[3])
		exit(0)

def parseargs():
	parser = argparse.ArgumentParser(prog="Twitter Bot")
	parser.add_argument("-f", "--function", help="Please enter the type of bot you wish to use. E.g.(Coutdown, Standard, Substitute)", required=True)
	parser.add_argument("-d", "--date", help="Please enter your date in the form: MM/DD/YYYY")
	parser.add_argument("-m", "--message", help="Please enter the message you wish to send.", required=True)
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
	
# Function will log based on log_type, the logging message and the specified path
def Log(log_type, message, path):
	logger = open(path, "a")
	logger.write("[%s] %s: %s\n" % (function_mappings["date_now"], log_type.upper(), message))
	logger.close()
	
if __name__ == "__main__": main()
