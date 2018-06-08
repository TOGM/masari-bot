import configparser

config = configparser.ConfigParser()

config.read('config.ini')

discordtoken = config['SETTINGS']['discordtoken'].strip()
server = config['SETTINGS']['server'].strip()
welcomeChannel = config['SETTINGS']['welcomeChannel'].strip()
exchangeChannel = config['SETTINGS']['exchangeChannel'].strip()
marketChannel = config['SETTINGS']['marketChannel'].strip()
networkChannel = config['SETTINGS']['networkChannel'].strip()
apiURL = config['SETTINGS']['apiURL'].strip()
blockTargetTime = config['SETTINGS']['blockTargetTime'].strip()
coinCode = config['SETTINGS']['coinCode'].strip()