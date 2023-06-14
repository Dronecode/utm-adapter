### UTM Adapter Specification

This document details at a high level the requirements for a UTM adapter that will be integrated in QGCS.
## Scope of work 

## Eco-system 
UTM services or U-space services as it is called in the EU are a set of digital services to enable safe integration of drones with manned aviation that are regulated and will be verified and certified in the EU. Automated verification of the ability to conform to UTM standards forms a part of the UTM Service provider (USSP) certification framework. 

The EU U-space law builds a regulatory framework for UTM, it is expected that other jurisdictions will have their own version of UTM regulations, while this work at this time (June 2023) is focused on the EU, it is not limited to it. It is expected that the codebase will change as other jurisdictions will build a regulatory / legal framework for integrating drones in the airspace and enabling "advanced" operations like BVLOS etc. 

### UTM Standards 
The [EU U-Space law](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32021R0664) and the associated [acceptable means of compliance (AMC) and guidance material (GM)](https://www.easa.europa.eu/en/document-library/acceptable-means-of-compliance-and-guidance-materials/amc-and-gm-implementing) has been published. 
- [Network Remote ID](https://www.astm.org/f3411-22a.html): Mentioned in the AMC/GM document as a acceptable way to comply to Net-RID. This standard specifies interfaces to ensure that 
- [EuroCAE ED-269](https://eurocae.net/news/posts/2020/june/ed-269-minimum-operational-performance-standard-for-uas-geo-fencing/): Mentioned in the AMC/GM document as a acceptable way to share with Geozone information.
- [USSP Interoperability](https://www.astm.org/f3548-21.html): Sharing operational intents / flight authorization can be shared via this standard, the `interuss/dss` implements this standard. 

### Services with no / lack of standards
- Traffic information service: A service that shares air-traffic information via an API, normally this is hosted by a Air-Navigation Service provider (ANSP) or the standards allow for a special types of "Supplemental Data Service Providers"
- Common information services: A server that hosts and shares ED-269 Geozones and other information, currently there is no standard for it and this server will normally be expected to be hosted by an ANSP and / or an authority. 

### Opensource software 
There exists open-source software in the context of UTM 
- [interuss/dss](https://github.com/interuss/dss): Open source software the enables standards-compliant Discovery of UTM services and synchronization of data. 
- [interuss/monitoring](https://github.com/interuss/monitoring): A UTM services verification suite developed to test compliance against UTM standards
- [openskies-sh/flight-blender](https://github.com/openskies-sh/flight-blender): A reference implementation that implements in the open-source standards compliant UTM services passes the `interuss/monitoring` suite. It is used in the context of inter-operability testing by developers and enables third-party verification of UTM software. 

## Underlying mechanism
A JSON based config file will need to be developed that allows the operator / entity / person using the GCS to configure details of a UTM endpoints. A REST based adapter that can submit data to USSP interfaces on the internet.

__Deliverables__:
- JSON specification that contains the details of an USSP implementation that the QGCS user-interface can read. 
- QGCS module / code that reads the JSON and interacts with the user-interface

## Notifications
Interaction with USSP and USSP network is a synchronous process and there needs to be a notification mechanism that tells the operator "prominently" what is going on in the UTM system.

## A. Interface for Flight Authorization
__Goal__: Allow the GCS to send flight plan to the USSP and get an associated status. 

__Pre-requisites__: 
- A flight plan is built in the QGCS user-interface and it is valid 
- A network connection exists between QGCS and USSP

__Reference__: 
- Example submission of a plan [as GeoJSON](https://github.com/openskies-sh/flight-blender/blob/master/api/flight-blender-1.0.0-resolved.yaml#L1402)
- Example states of an operation [Flight Blender](https://github.com/openskies-sh/flight-blender/blob/master/api/flight-blender-1.0.0-resolved.yaml#L1885)

## B. Interface for Network RID / Telemetry

__Goal__: Allow the GCS to send live telemetry (for a registered operation) to the USSP via this QGCS user-interace so that the USSP can process the data and share it with the UTM network. 
__Pre-requisites__: 
- A plan is built and shared to the USSP and authorized by the USSP (see Flight Authorization service below). 
- Telemetry data from the drone should be submitted via TCP / IP with REST interfaces to the USSP that can be configured
- Additional data e.g. operator location, drone serial number, operator registration number etc. 

__Reference__: 
- Automated test for [ASTM network RID](https://github.com/interuss/monitoring/blob/main/monitoring/uss_qualifier/suites/astm/netrid/f3411_22a.yaml) exists
- [Data format](https://github.com/uastech/standards/blob/dd4016b09fc8cb98f30c2a17b5a088fb2995ab54/remoteid/canonical.yaml#L1692) per ASTM Remote ID standard


## C. Interface for Geofence / Geozone
Goal: To build a way for QGCS to read Geozone / Geofence information and show the data in the user interface

## D. Interface for Traffic Information

## E. Interface for Conformance Monitoring