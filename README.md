# QGCS UTM Adapter Project
## Goal
The goal of this work is to develop a UTM focused working group within Dronecode membership and build an open / configurable adapter for QGCS to enable it to exchange relevant data a UTM system. The adapter would be configurable so that the operator can specify what UTM system it wants to use. The UTM system in turn must implement those APIs to exchange data with QGCS. 
## Scope

![Screenshot](images/net-rid.jpg)

Figure: Image depicting the scope of ASTM Network RID standard, the part in Red: the way operators submit data to the UTM system is not standardized and we hope to build an API specification and a configurable implementation for that as well as other relevant data (flight authorizations, geozones, conformance alerts etc.). 

## Deliverables

1. OpenAPI document specifying the adapter + relevant documentation of configuring adapter 
2. API to be implemented at the UTM Service Provider side
3. Implement Adapter + configuration file in QGCS that enables exchange of data with different UTM services
4. Integration of this adapter in QGCS builds + test infrastructure
 
## Timeline
- Start date: 31 May 2023 -  30 November 2023 (6 months)
- Evaluation phase: December + January 2023 / re-work
