# Hero Labs API endpoints
BASE_RESOURCE: str = "https://api.hero-labs.com"
AUTH_RESOURCE: str = f"{BASE_RESOURCE}/user-service/auth/sign_in"
USER_RESOURCE: str = f"{BASE_RESOURCE}/user-service/customer_app/users/"  # +USER_ID
REFRESH_TOKEN_RESOURCE: str = f"{BASE_RESOURCE}/user-service/auth/refresh_token"
SIGN_OUT_RESOURCE: str = f"{BASE_RESOURCE}/user-service/auth/sign_out"
UPDATE_USER_RESOURCE: str = f"{BASE_RESOURCE}/customer_app/users/"  # +USER_ID
RESET_PASSWORD_RESOURCE: str = f"{BASE_RESOURCE}/iot-core-public/passwords/reset_password"
LIST_PROPERTIES_RESOURCE: str = f"{BASE_RESOURCE}/ape/v1/properties"
FETCH_NOTIFICATION_SETTINGS_RESOURCE: str = f"{BASE_RESOURCE}/ape/v1/properties/"  # +PROPERTY_ID+"/notifications"
FETCH_PROPERTY_SETTINGS_RESOURCE: str = f"{BASE_RESOURCE}/ape/v1/properties/"  # +PROPERTY_ID+"/settings"
LIST_SIGNALS_RESOURCE: str = f"{BASE_RESOURCE}/ape/v1/signals"
LIST_SONICS_RESOURCE: str = f"{BASE_RESOURCE}/ape/v1/sonics"
LIST_SONICS_WIFI_RESOURCE: str = f"{BASE_RESOURCE}/ape/v1/sonics_wifi"
LIST_INCIDENTS_RESOURCE: str = f"{BASE_RESOURCE}/ape/v1/incidents"
LIST_TELEMETRY_RESOURCE: str = f"{BASE_RESOURCE}/ape/v1/sonics/"  # +SONIC_ID+"/telemetry"
SONIC_VALVE_RESOURCE: str = f"{BASE_RESOURCE}/ape/v1/sonics/"  # +SONIC_ID+"/valve"

DEFAULT_TIMEOUT: int = 10
DEFAULT_HEADER_CONTENT_TYPE: str = "application/json;charset=UTF-8"
