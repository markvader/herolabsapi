"""Define package constants."""
# Hero Labs API endpoints
# key api resource endpoints
BASE_RESOURCE: str = "https://api.hero-labs.com"
AUTH_RESOURCE: str = "user-service/auth/sign_in"
USER_RESOURCE: str = "user-service/customer_app/users/"  # +USER_ID
REFRESH_TOKEN_RESOURCE: str = "user-service/auth/refresh_token"
SIGN_OUT_RESOURCE: str = "user-service/auth/sign_out"
# user resource endpoints
UPDATE_USER_RESOURCE: str = "customer_app/users/"  # +USER_ID
RESET_PASSWORD_RESOURCE: str = "iot-core-public/passwords/reset_password"
# property resource endpoints
LIST_PROPERTIES_RESOURCE: str = "ape/v1/properties/"
FETCH_NOTIFICATION_SETTINGS_RESOURCE: str = "ape/v1/properties/"  # +PROPERTY_ID+"/notifications"
FETCH_PROPERTY_SETTINGS_RESOURCE: str = "ape/v1/properties/"  # +PROPERTY_ID+"/settings"
# signals resource endpoints
LIST_SIGNALS_RESOURCE: str = "ape/v1/signals"
# sonics resource endpoints
LIST_SONICS_RESOURCE: str = "ape/v1/sonics/"
LIST_SONICS_WIFI_RESOURCE: str = "ape/v1/sonics_wifi"
LIST_TELEMETRY_RESOURCE: str = "ape/v1/sonics/"  # +SONIC_ID+"/telemetry"
SONIC_VALVE_RESOURCE: str = "ape/v1/sonics/"  # +SONIC_ID+"/valve"
# incidents resource endpoints
LIST_INCIDENTS_RESOURCE: str = "ape/v1/incidents"
