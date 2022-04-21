import configparser
from api import Api

config = configparser.ConfigParser()
config.read('config.ini')
herolabs_email = config['DEFAULT']['EMAIL']
herolabs_password = config['DEFAULT']['PASSWORD']

apiObj = Api(herolabs_email, herolabs_password)

# functions below should all work independently of each other, uncomment one or more of them

# User Details Function
# user_details = apiObj._user_details()

# Signal Device Function
# signals = apiObj._retrieve_signals()

# Sonic Device Functions
# sonics = apiObj._retrieve_sonics()
telemetry = apiObj._sonic_telemetry()
# valve_control = apiObj._sonic_valve("close")
# valve_control = apiObj._sonic_valve("open")
# incidents = apiObj._retrieve_incidents()

# property functions
# properties = apiObj._retrieve_properties()
# property_notification_settings = apiObj._property_notification_settings()
# property_settings = apiObj._property_settings()

# admin functions
# update_user_details = apiObj._update_user_details({'last_name': 'testLastName', 'language': 'en'})
# invalidate_token = apiObj._invalidate_token()
# reset_password_request = apiObj._reset_password_request("useremail@emailprovider.com")


# called within other functions and not directly
# _retrieve_token()
# _check_token()
# _refresh_token()
