# Introduction
This document captures the bi-weekly meeting notes. 

### June 8, 2023
**Meeting Minutes**
Hey folks, welcome to the workgroup’s first meeting; we are kicking off with an overview of the project and a goal alignment meeting.

Goal Discussion: The team agrees the main goal for the project is to build an open-source configurable adapter for QGC that can submit telemetry to participating UTM providers.    
    - The scope of the adapter is the four U-Space mandatory services: Net-RID, Strategic De-confliction / Flight Authorization, Traffic Information and Geozones
    - The optional service of Conformance monitoring is also included in scope. 
    - Integration of weather service is a strech goal, the standard for weather has been released, need to review it after the initial work is complete.
    - We discussed changes to the QGCS User interface and how the work will be handled.
    - Changes to Mavlink / Mavlink protocol is outside of scope of the project at this moment. 

Next Steps: We are putting together data requirements for the interfaces and discussing before the meeting. The data will be distributed before the meeting starts.
    - HB to start a PR detailing initial spec for review in the next meeting
