# herolabsapi - TO DO list

## Main task remaining
- Tests
- Example Code (separate some from readme, getting too long)
- Tidy up readme and other documentation

## functions for remaining endpoints
sonics_wifi endpoints currently returning zero results (but valid return)
- get /ape/v1/sonics_wifi
- get /ape/v1/sonics_wifi/{id}
- put /ape/v1/sonics_wifi/{id}

no documentation on what fields can be updated via API
- put /ape/v1/properties/{property_id}/notifications
- put /ape/v1/properties/{property_id}/settings

## later:
When api_token expiry date added to api by hero labs developers, incorporate its use into library


## DONE
Check commit log for full progress, lots more than just these
- create and use function for common headers
- set token expiry
- initiate checks for token being present, check if token valid, if not request one, if expiring soon, renew it.
- functions - timestamps returned in telemetry and signals json response, converted to datetime
(do I want to do this in the library or leave it to Home assistant etc.)
- handle session object properly
- rewrite for asynchronous code (may need to use aiohttp rather than requests)
- capturing full log of incidents, let user chose to displaying all/open/last incidents etc.
- add logging to library
- fix markdown in readme (formatting for / in table doesn't display in PYPI, need to encode it?)
- re-write readme
- appropriate handling for users with multiple sonics, signals or properties, at the minute only first devices returned are utilised
- Refactor code (reduce duplication of lines calling request library)
- Separate functions to different files if appropriate, authentication & user functions, device interactions (sonics & signals), incidents
