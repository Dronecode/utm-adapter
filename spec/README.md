### UTM Adapter Specification

This document details at a high level the requirements for the UTM adapter 
## Scope of work 

## Eco-system 
UTM services or U-space services as it is called in the EU are a set of digital services to enable safe integration of drones with manned aviation that are regulated and will be verified and certified in the EU. Automated verification of the ability to conform to UTM standards forms a part of the UTM Service provider (USSP) certification framework. 

### UTM Standards 
The [EU U-Space law](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32021R0664) and the associated [acceptable means of compliance (AMC) and guidance material (GM)](https://www.easa.europa.eu/en/document-library/acceptable-means-of-compliance-and-guidance-materials/amc-and-gm-implementing) has been published. 
- [Network Remote ID](https://www.astm.org/f3411-22a.html): Mentioned in the AMC/GM document as a acceptable way to comply to Net-RID. This standard specifies interfaces to ensure that 
- [EuroCAE ED269](https://eurocae.net/news/posts/2020/june/ed-269-minimum-operational-performance-standard-for-uas-geo-fencing/): Mentioned in the AMC/GM document as a acceptable way to share with Geozone information.
- [USSP Interoperability](https://www.astm.org/f3548-21.html): Sharing operational intents / flight authorization can be shared via this standard, the `interuss/dss` implements this standard. 

### Services with no / lack of standards
- Traffic information service: A service that shares air-traffic information via an API, normally this is hosted by a Air-Navigation Service provider (ANSP) or the standards allow for a special types of "Supplemental Data Service Providers"
- Common information services: A server that hosts and shares ED-269 Geozones and other information, currently there is no standard for it and this server will normally be expected to be hosted by an ANSP and / or an authority. 

### Opensource software 
There exists open-source software in the context of UTM 
- [interuss/dss](https://github.com/interuss/dss): Open source software the enables standards-compliant Discovery of UTM services and synchronization of data. 
- [interuss/monitoring](https://github.com/interuss/monitoring): A UTM services verification suite developed to test compliance against UTM standards
- [openskies-sh/flight-blender](https://github.com/openskies-sh/flight-blender): A reference implementation that implements in the open-source standards compliant UTM services passes the `interuss/monitoring` suite. It is used in the context of inter-operability testing by developers and enables third-party verification of UTM software. 

## A. Interface for Network RID / Telemetry

Goal: Allow the GCS to send live telemetry to the USSP via this interface so that the USSP can process the data and share it with the UTM network
Pre-requisites: 
- A plan is developed and shared with the USSP network and authorized by the USSP (see Flight Authorization service below) and telemetry is shared against that plan. 
- Telemetry data from the drone should be submitted via TCP / IP with REST interfaces
Reference: 
- Automated test for [ASTM network RID](https://github.com/interuss/monitoring/blob/main/monitoring/uss_qualifier/suites/astm/netrid/f3411_22a.yaml) exists



## B. Interface for Flight Authorization
Goal: Allow the GCS to send flight plan and other data and get the associated authorization 


## C. Interface for Geofence / Geozone

## D. Interface for Traffic Information

## E. Interface for Conformance Monitoring