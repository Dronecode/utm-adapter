# Meeting Minutes
This document captures the bi-weekly meeting notes for coordination purposes.

### June 22, 2023
We discussed the project scope of work and reviewed the proposal from @hrishiballal outlined in #2, particularly the "Core Modules" and "Services" required.

Configuration modules are portable text files (JSON proposed) containing metadata for USSP services, such as any user authentication and endpoint details, so that QGC knows where to fetch data for a given service and how to authorize a user to begin the workflow.

**Note: @hrishiballal will provide an example configuration file at the next meeting.

We discussed the need for QGC to understand when it's ONLINE or OFFLINE because its the law in some geographical regions that they NEED UTM authorization and to publish telemetry continuously.

Additionally, the operator needs feedback from the USSP service and should always know what's going on with the system.

The five services listed in the document are the REQUIRED services for an operation at the USSP/UTM level

TODO: help create a config file
TODO: distribute meeting minutes 

### June 8, 2023
Hey folks, welcome to the workgroup’s first meeting; we are kicking off with an overview of the project and a goal alignment meeting.

Goal Discussion: The team agrees the main goal for the project is to build an open-source configurable adapter for QGC that can submit telemetry to participating UTM providers:

1. The scope of the adapter is the four U-Space mandatory services: Net-RID, Strategic De-confliction / Flight Authorization, Traffic Information and Geozones
2. The optional service of Conformance monitoring is also included in scope.
3. Integration of weather service is a strech goal, the standard for weather has been released, need to review it after the initial work is complete.
4. We discussed changes to the QGCS User interface and how the work will be handled
5. Changes to Mavlink / Mavlink protocol is outside of scope of the project at this moment. 

Next Steps: We are putting together data requirements for the interfaces and discussing before the meeting. The data will be distributed before the meeting starts.
    - HB to start a PR detailing initial spec for review in the next meeting
