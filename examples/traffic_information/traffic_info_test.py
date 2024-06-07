import argparse
import datetime
from pymavlink import mavutil

class Error(Exception):
    def __init__(self, message):
        self.message = message

utc_date_formatter = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

class utm_traffic_info:
    def __init__(self):
        self.last_system_time = float("-inf")

    def parse(self, message):
        try:
            if isinstance(message, mavutil.mavlink.MAVLink_adsb_vehicle_message):
                self.parse_adsb_vehicle_message(message)
            elif isinstance(message, mavutil.mavlink.MAVLink_system_time_message):
                self.parse_system_time_message(message)
            else:
                print("Received unknown message type:", type(message))
        except Exception as e:
            print(f"Error while parsing message: {e}")

    def parse_adsb_vehicle_message(self, message):
        print("ADSB_VEHICLE:")
        print(f"ICAO_address: {message.ICAO_address}")
        print(f"lat: {message.lat}")
        print(f"lon: {message.lon}")
        print(f"altitude_type: {message.altitude_type}")
        print(f"altitude: {message.altitude}")
        print(f"heading: {message.heading}")
        print(f"hor_velocity: {message.hor_velocity}")
        print(f"ver_velocity: {message.ver_velocity}")
        print(f"callsign: {message.callsign}")
        print(f"emitter_type: {message.emitter_type}")
        print(f"tslc: {message.tslc}")
        print(f"flags: {message.flags}")
        print(f"squawk: {message.squawk}")
        print()

    def parse_system_time_message(self, message):
        print("SYSTEM_TIME:")
        print(f"time_unix_usec: {message.time_unix_usec}")
        print(f"time_boot_ms: {message.time_boot_ms}")
        self.last_system_time = message.time_unix_usec * 1E-6
        print()

def main():
    parser = argparse.ArgumentParser(description='utm-adapter traffic info stream file')
    parser.add_argument('inputFile', type=str, help='Input file')
    args = parser.parse_args()

    traffic_info = utm_traffic_info()

    try:
        mlog = mavutil.mavlink_connection(args.inputFile, notimestamps=True)
    except Exception as e:
        print(f'Error: {e}')
        exit()

    while True:
        try:
            msg = mlog.recv_msg()
            if msg is None:
                break
            traffic_info.parse(msg)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

