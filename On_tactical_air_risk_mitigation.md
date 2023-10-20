# On tactical air risk mitigation

Author(s): Kai Lothar John <https://github.com/jokalode>

© 2023 by Kai Lothar John. ALL RIGHTS RESERVED.

The following is a short treatise on tactical air risk mitigation, and
how to use traffic information for that purpose. It is based on
regulations of the European Union (EU) and publications of the
European Union Aviation Safety Agency (EASA), as referenced in the
text.

[EU 2019/945]: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32019R0945
[EU 2019/947]: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32019R0947
[EU 2021/664]: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32021R0664
[Easy Access Rules]: https://www.easa.europa.eu/en/document-library/easy-access-rules/easy-access-rules-unmanned-aircraft-systems-regulations-eu

## TL;DR - The very short version

Remote pilots, or autonomous UAS control systems, are responsible for
assessing traffic information, and deciding upon taking evasive
action, or not.

Aircraft operators are responsible for broadcasting position reports.

UTM service providers are responsible for picking up those position
reports, and for dispatching relevant information to concerned parties
without undue delay, while preserving the integrity of the
information.

## The short version

### On the origin of traffic information

In the context of air traffic management, traffic information is
either generated onboard an aircraft, or in a radar station. In the
former case, the aircraft estimates its own time, position, altitude,
speed, etc. derived from onboard sensors. In the latter case, the
radar station estimates its own time, and the target's position and
altitude.

### On responsibilites

UAS operators are responsible for the (flight) safety of their
operations. They shall develop operational procedures adapted to the
type of their operations and the risks involved.

References:

- [EU 2019/947] UAS.OPEN.050 (1)
- [EU 2019/947] UAS.SPEC.050 (1) (a)
- [EU 2019/947] UAS.LUC.020 (1)

Upon receiving traffic information services (sic!), UAS operators shall take
relevant action to avoid any collision hazard.

References:

- [EU 2021/664] Art. 11 No. 4

During a flight in the "Specific" category, in the case of autonomous
operations, UAS operators shall ensure that during all phases of the
operation, responsibilities and tasks that would normally be allocated
to remote pilots are properly allocated otherwise.

References:

- [EU 2019/947] UAS.SPEC.050 (1) (b)

During a flight in the "Open" category, remote pilots shall keep their
aircraft in sight and maintain a thorough visual scan of the airspace
surrounding their aircraft in order to avoid any risk of collision
with any other aircraft. The remote pilot shall discontinue the flight
if the operation poses a risk to other aircraft, people, animals,
environment or property.

References:

- [EU 2019/947] UAS.OPEN.060 (2)(b)

During a flight in the "Specific" category, remote pilots, or
autonomous control systems, shall avoid any risk of collision with any
other aircraft and discontinue their flights when continuing it may
pose a risk to other aircraft, people, animals, environment or
property.

References:

- [EU 2019/947] UAS.SPEC.060 (3)(b)

### On the detect and avoid procedure

During a flight in the "Specific" category, in a designated UTM
airspace, remote pilots, or autonomous control systems, shall maintain
situational awareness as follows.

They should

- detect other aircraft in the vicinity of their own aircraft;
- decide if the other aircraft are at risk;
- command their own aircraft to take evasive action;
- execute evasive action;
- observe effectiveness of evasive action.

References:

- [Easy Access Rules] D.5.3

In a dedicated UTM airspace, detecting other aircraft is achieved by
subscribing to a traffic information service.

The effectiveness of the detect and avoid procedure is determined
primarily by the timeliness of the traffic information. The more the
traffic information is behind the actual situation, the more extreme
evasive actions must be taken, up to and beyond the point that the
(remote) pilots run out of options.

When deciding whether to take evasive action, remote pilots, or
autonomous control systems, must be able to assess the age of the
traffic information they receive.

This imposes real-time constraints on the information paths from aircraft and ground control stations.

This imposes clock integrity and synchronization constraints between aircraft and ground control stations.

This imposes a maximum latency between aircraft and ground control stations.

### Notes and recommendations

**[Recommendation]** Aircraft should report the clock used to estimate
own-time (GPS, Galileo, etc.) for receivers to determine their clock
skew.

**[Recommendation]** Aircraft, traffic information publishers and
subscribers should use the same reference clock.

**[Recommendation]** Aircraft should report position in WGS84 coordinates.

**[Recommendation]** UTM service providers should keep position report
processing to the bare minimum: receive, identify concerned
subscribers, dispatch.

**[Recommendation]** UTM service providers should be able to determine
a ballpark estimate of the distance between any two aircraft with
very, very, very low latency. The estimate shall be such that the
actual distance may be greater than the estimate, but not less.

**[Recommendation]** Ground control stations should be able to
compensate for position error due to latency; for example by applying
a Kalman filter.

**[Recommendation]** The network layer should respect real-time
properties.

**[Note]** Using TCP may introduce unwanted latency, see [Nagle's algorithm](https://en.wikipedia.org/wiki/Nagle%27s_algorithm#Interactions_with_real-time_systems).

**[Note]** Using UDP may suffer packet loss in congested networks.

**[Recommendation]** Aircraft should not report own-speed as Δp/Δt.

**[Recommendation]** Aircraft should not report own-course as `atan2(Δx,Δy)`.
