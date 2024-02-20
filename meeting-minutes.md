# Meeting Minutes
This document captures the bi-weekly meeting notes for coordination purposes.

### February 15 2024
In the meeting on HB and KLJ were present and we discussed the QUIC / traffic information endpoint. We discussed that the end point should have options for ASTERIX or Mavlink messages to share traffic information and USSPs can then choose the best strategy of sharing the data. 

### February 1 2024
First draft of the PR into QGCS is merged. A major part of the adapter code is in, we will have to enable and test and going forward it will be easier. Govind has a PR open in QGCS re test framework and examples. HB to add a readme and add / review the PRs. For traffic information service request and the server will give a information on how to connect to the QUIC service. Kai to provide sample air-traffic data file and Govind to update the example code in the PR. 

### January 4 2024
In the meeting we discussed the progress in the QGCS PR and resolving some of Beat's comments. We also discussed provisioning a OpenUTM instance / reference implementation to test with the endpoints. We also discussed a proof-of-concept implementation of traffic data via Mavlink Datagrams over QUIC. 

### December 21, 2023
In the meeting we discussed the two open PRs and also the next steps re the "Mavlink on QUIC" implementation. Kai agreed to build a prototype of traffic information service and a way for QGCS to query it. We also discussed the need for QGCS to build tracks / trajectories based on traffic information. We will meet next on the 4th January. 

### November 23, 2023
In the meeting we discussed different protocols for the traffic information service. The discussion was around if SRTP etc. are a good fit for traffic information where accuracy and timeliness is important. HTTP3 is not a good method for traffic information / QUIC is a better. SRTP/ WebRTC etc. are primarily media streaming and they do buffering in case of poor connectivity etc. , so they are not good fit. These have to be extended by custom code / development e.g. via profiles and payload to extend the payloads to make it suitable for air-traffic information. 
Discussion on QUIC: QUIC is secure by default (incorporates TLS v1.3), manned traffic information can be disseminated via RTCA-DO-260 and EuroCAE ED-102. Asterix (binary) variable length header, BEAST. 
- TODO Map Mavlink to QUIC datagrams
    - GCS should implement the receiving end 
    - USSP should implement the sending end 
- The basic query mechanism will be something like show me flights in x mile radius 
- Can mavlink be used with QUIC or is it linked to the UDP transport? To investigate 
    - If not it should be MQTT over QUIC or AMQP over QUIC.


### October 26, 2023
We discussed the traffic information service and the fact that there is a "real-time" aspect to the service so the discussion focused on how to best select the protocol for publishing Traffic Information data. We discussed the best way to make the contributions to QGCS and the conversations in-person at the PX4 Summit. Some actions: 
- @hrishiballal will create a criteria for selection in the repository
- Kai will refactor the current [PR](https://github.com/Dronecode/utm-adapter/pull/13/files) to be added to the [spec](https://github.com/Dronecode/utm-adapter/tree/main/spec) Traffic Information interface
- All members will review real-time protocols / technologies that can be used to share real-time safety information 


### September 27, 2023
We reviewed the operator API and the mechanism for notification: the USSP has the responsibility to notify the operators so a pull request cycle is not the best way to develop the API. We discussed the roadmap where the current focus is on Network RID and Strategic Deconfliction and then tackle traffic management service. We discussed that RID / SCD are primarily REST based but there needs to be a new mechanism to define the Traffic information service given its realtime nature. We will revisit it in the next meeting.

### September 15, 2023
We reviewed the API and discussed the air-traffic endpoint and mandatory / optional fields. @hrishiballal to add optional fields once a PR is submitted with a list of them, we discussed a tentative list. 
@hrishiballal to add new endpoints for Network RID display application so that QGCS can act as one. 

### August 3, 2023
Team, today we reviewed @hrishiballal [proposed services](https://github.com/Dronecode/utm-adapater/pull/7) for Flight Authorization and Network Remote ID. Thanks to everyone who joined the call and gave feedback on the call.

* [Service Proposal](https://github.com/Dronecode/utm-adapater/pull/7)
* **TODO:** To all members of the WG, please review the Pull Request and leave feedback directly on GitHub. We are looking for scrutiny in every field and service.
* **TODO:**: @mrpollo will reach out to the MAVLink team to discuss how to integrate a mission authorization identifier into the mission micro-service 

### July 6, 2023
In today's meeting, we discussed @hrishiballal proposal for a QGC configuration file. At this stage the file specifies how QGC can read the capabilities of a UTM provider and successfully use their services; the proposal also includes a API that a participating USSP can implement to be compatible with QGCS Adapter. Currently the WG is focusing on two services: Flight Authorization and Network Remote ID and define the groundwork needed to make them work, with the idea of adding the rest of the required services once things stabilize and are standardized. The two primary services are Flight Authorization and Network Remote ID.

**NOTE**: the group considers out of scope how QGC knows of the product.json files; we expect to resolve this in future discussions; some ideas are having previous knowledge at build-time or having a way to load at runtime.

**TODO**: The proposal is a first draft, and we are looking for feedback from everyone; please submit a review of the pull request by July 13th to allow for a discussion before our next meeting https://github.com/Dronecode/utm-adapater/pull/5

**Next Meeting**: At our next meeting (July 20th), we will have presentations from UTM providers with demos of their current implementations.

### June 22, 2023
We discussed the project scope of work and reviewed the proposal from @hrishiballal outlined in #2, particularly the "Core Modules" and "Services" required.

Configuration modules are portable text files (JSON proposed) containing metadata for USSP services, such as any user authentication and endpoint details, so that QGC knows where to fetch data for a given service and how to authorize a user to begin the workflow.

**Note: @hrishiballal will provide an example configuration file at the next meeting.

We discussed the need for QGC to understand when it's ONLINE or OFFLINE because its the law in some geographical regions that they NEED UTM authorization and to publish telemetry continuously.

Additionally, the operator needs feedback from the USSP service and should always know what's going on with the system.

The five services listed in the document are the REQUIRED services for an operation at the USSP/UTM level (per the EU U-Space regulation).

TODO: help create a config file
TODO: distribute meeting minutes 

### June 8, 2023
Hey folks, welcome to the workgroup’s first meeting; we are kicking off with an overview of the project and a goal alignment meeting.

Goal Discussion: The team agrees the main goal for the project is to build an open-source configurable adapter for QGC that can submit telemetry to participating UTM providers:

1. The scope of the adapter is the four U-Space mandatory services: Net-RID, Strategic De-confliction / Flight Authorization, Traffic Information and Geozones
2. The optional service of Conformance monitoring is also included in scope.
3. Integration of weather service is a stretch goal, the standard for weather has been released, need to review it after the initial work is complete.
4. We discussed changes to the QGCS User interface and how the work will be handled
5. Changes to Mavlink / Mavlink protocol is outside of scope of the project at this moment. 

Next Steps: We are putting together data requirements for the interfaces and discussing before the meeting. The data will be distributed before the meeting starts.
    - HB to start a PR detailing initial spec for review in the next meeting
