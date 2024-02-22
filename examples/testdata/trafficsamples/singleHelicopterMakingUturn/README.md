# Traffic file format description

The traffic file `traffic.bin` contains shy of two minutes of a recorded track of an actual  helicopter.

The file format is binary serialized MAVLINK v2 that can be parsed with `mavlink_frame_char(uint8_t, uint8_t, mavlink_message_t*, mavlink_status_t*)`.

The file contains a sequence of `mavlink_message` with alternating payloads of `SYSTEM_TIME` and `ADSB_VEHICLE` as follows.

```
+--------------------------------+
| mavlink message (system time)  |
+--------------------------------+
| mavlink message (ADSB vehicle) |
+--------------------------------+
| mavlink message (system time)  |
+--------------------------------+
| mavlink message (ADSB vehicle) |
+--------------------------------+
| ...                            |
```

## Notes on `mavlink_system_time_t` messages

- All `mavlink_system_time_t` messages have a `time_unix_usec` value relative to the beginning of the file:
  - The first `mavlink_system_time_t` message has a `time_unix_usec` value of `0`;
  - the second `mavlink_system_time_t` message has a `time_unix_usec` value of  `604_000`; and so on, until 
  - the last `mavlink_system_time_t` message has a `time_unix_usec` value of `117_200_000`.
- The original data source did only provide Millisecond precision for `time_unix_usec`.
- The original data source did not provide `time_boot_ms`.

## Notes on `mavlink_adsb_vehicle_t` messages

- The values of the `ver_velocity` fields are inconsistent with the `altitude` information. 

  This may be an issue with the original data source.
