import configparser
from api import Api

config = configparser.ConfigParser()
config.read('config.ini')
herolabs_email = config['DEFAULT']['EMAIL']
herolabs_password = config['DEFAULT']['PASSWORD']

apiObj = Api(herolabs_email, herolabs_password)

login = apiObj._retrieve_token()
user_details = apiObj._user_details()
