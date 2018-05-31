import configparser

config = configparser.ConfigParser()

config.read('config.ini')

discordtoken = config['SETTINGS']['discordtoken'].strip()
server = config['SETTINGS']['server'].strip()
apiURL = config['SETTINGS']['apiURL'].strip()
blockTargetTime = config['SETTINGS']['blockTargetTime'].strip()
coinCode = config['SETTINGS']['coinCode'].strip()