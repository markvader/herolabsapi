import configparser
from api import Api

config = configparser.ConfigParser()
config.read('config.ini')
herolabs_email = config['DEFAULT']['EMAIL']
herolabs_password = config['DEFAULT']['PASSWORD']

apiObj = Api(herolabs_email, herolabs_password)

login = apiObj._retrieve_token()
user_details = apiObj._user_details()
# sonics = apiObj._retrieve_sonics()
# signals = apiObj._retrieve_signals()
# incidents = apiObj._retrieve_incidents()
# telemetry = apiObj._sonic_telemetry()
# properties = apiObj._retrieve_properties()
# property_notification_settings = apiObj._property_notification_settings()
# property_settings = apiObj._property_settings()
# valve_control = apiObj._sonic_valve("close")
# valve_control = apiObj._sonic_valve("open")
# update_user_details = apiObj._update_user_details({'last_name': 'testLastName', 'language': 'en'})
# refresh_token = apiObj._refresh_token()
# invalidate_token = apiObj._invalidate_token()
