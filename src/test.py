import configparser
from api import Api

config = configparser.ConfigParser()
config.read('config.ini')
herolabs_email = config['DEFAULT']['EMAIL']
herolabs_password = config['DEFAULT']['PASSWORD']
demo_incident_id = config['DEMO_DATA']['INCIDENT_ID_SAMPLE']
demo_signal_id = config['DEMO_DATA']['SIGNAL_ID_SAMPLE']
demo_sonic_id = config['DEMO_DATA']['SONIC_ID_SAMPLE']
demo_property_id = config['DEMO_DATA']['PROPERTY_ID_SAMPLE']

apiObj = Api(herolabs_email, herolabs_password)

# functions below should all work independently of each other, uncomment one or more of them

# User Details Function
# user_details = apiObj._user_details()

# Signal Device Function
# signals = apiObj._retrieve_signals()
# signal_by_id = apiObj._retrieve_signal_by_id(demo_signal_id)
# signals_by_property_id = apiObj._signals_by_property_id(demo_property_id)


# Sonic Device Functions
# sonics = apiObj._retrieve_sonics()
# sonic_by_id = apiObj._retrieve_sonic_by_id(demo_sonic_id)
# sonics_by_signal_id = apiObj._sonics_by_signal_id(demo_signal_id)
# sonics_wifi = apiObj._retrieve_sonics_wifi(demo_property_id)

# telemetry = apiObj._sonic_telemetry()
# valve_control = apiObj._sonic_valve("close")
# valve_control = apiObj._sonic_valve("open")

# incidents = apiObj._retrieve_incidents()
# incident_by_id = apiObj._retrieve_incident_by_id(demo_incident_id)
# incidents_by_property_id = apiObj._incidents_by_property_id(demo_property_id)

# property functions
# properties = apiObj._retrieve_properties()
# property_by_id = apiObj._retrieve_property_by_id(demo_property_id)
# property_notification_settings = apiObj._property_notification_settings()
# property_notification_settings_by_id = apiObj._property_notification_settings_by_property_id(demo_property_id)
# property_settings = apiObj._property_settings()
# property_settings_by_id = apiObj._property_settings_by_property_id(demo_property_id)

# admin functions
# update_user_details = apiObj._update_user_details({'last_name': 'testLastName', 'language': 'en'})
# invalidate_token = apiObj._invalidate_token()
# reset_password_request = apiObj._reset_password_request("useremail@emailprovider.com")

# called within other functions and not directly
# _retrieve_token()
# _check_token()
# _refresh_token()

# Incident Actions
# dismiss_incident_by_id = apiObj._action_incident(demo_incident_id, "dismiss")
# reopen_incident_by_id = apiObj._action_incident(demo_incident_id, "reopen")

# update_property_by_id = apiObj._update_property(demo_property_id, json = {'city': "NewDemoCityNameValue",
#                                                                           'name': "NewDemoPropertyNameValue"})
# update_signal_by_id = apiObj._update_signal(demo_signal_id, "NewSignalName")
# update_sonic_by_id = apiObj._update_sonic(demo_sonic_id, "NewSonicName")
