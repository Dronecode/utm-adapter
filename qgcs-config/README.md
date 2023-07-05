## QGCS Config file

This directory contains the configuration detail for UTM adapter in QGCS

## File structure
| Variable Key | Data Type | Description |
|--------------|--------------|:-----:|
| available_services | list | A list of services that are supported by the USSP  |

## Definitions 

The adapter containts specific terms as defined in the [interuss/monitoring](https://github.com/interuss/monitoring) test suite. The specific definitions and 

### Flight Authorization
The capabilities of [Flight Authorization](https://github.com/interuss/automated_testing_interfaces/blob/8c83e2735c762f6fee8d6ca62ee1c1c0d479512c/scd/v1/scd.yaml) match the ones defined in `interuss/monitoring`

- `FlightAuthorisationValidation`: USS supports EU flight authorisation parameter validation.
- `BasicStrategicConflictDetection`: USS supports strategic conflict detection for typical flights, including future planning (Accepted
operational intents), activation (Accepted operational intents), and closing (deleting the operational intent reference).
- `HighPriorityFlights`: USS supports flights at priority levels higher than typical flights.