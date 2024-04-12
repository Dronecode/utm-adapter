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
        msgid = message.get_msgId()
        if msgid == mavutil.mavlink.MAVLINK_MSG_ID_SYSTEM_TIME:
            unix_time_usec = message.time_unix_usec
            self.last_system_time = unix_time_usec * 1E-6
        elif msgid == mavutil.mavlink.MAVLINK_MSG_ID_ADSB_VEHICLE:
            fields = ["time: {:.3f}".format(self.last_system_time)]
            icao_address = message.get_field("ICAO_address")
            fields.append("#{:06X}".format(icao_address))
            flags = message.get_field("flags")
            fields.append("flags: {:08b}".format(flags))
            if flags & mavutil.mavlink.ADSB_FLAGS_VALID_COORDS:
                lat = message.get_field("lat")
                lon = message.get_field("lon")
                fields.append("lat: {:.6f}".format(lat * 1E-7))
                fields.append("lon: {:.6f}".format(lon * 1E-7))
            if flags & mavutil.mavlink.ADSB_FLAGS_VALID_ALTITUDE:
                alt = message.get_field("altitude")
                fields.append("alt: {:.1f}".format(alt * 1E-3 / 0.3048))
            if flags & mavutil.mavlink.ADSB_FLAGS_VALID_HEADING:
                crs = message.get_field("heading")
                fields.append("crs: {:.0f}".format(crs * 1E-2))
            if flags & mavutil.mavlink.ADSB_FLAGS_VALID_VELOCITY:
                spd = message.get_field("hor_velocity")
                fields.append("spd: {:.1f}".format(spd * 36 / 1852))
            if flags & mavutil.mavlink.ADSB_FLAGS_VALID_CALLSIGN:
                call_sign = message.get_field("callsign")
                fields.append("c/s: {}".format(call_sign))
            if flags & mavutil.mavlink.ADSB_FLAGS_VERTICAL_VELOCITY_VALID:
                rcd = message.get_field("ver_velocity")
                fields.append("rcd: {:.3f}".format(rcd * 6 / 3.048))
            print(fields)

def main():
    parser = argparse.ArgumentParser(description='utm-adapter traffic info strean file')
    parser.add_argument('inputFile', type=str, help='Input file')
    args = parser.parse_args()

    traffic_info = utm_traffic_info()

    try:
        mlog = mavutil.mavlink_connection(args.inputFile)
    except Exception as e:
        raise Error(f'Error opening {args.inputFile}: {e}')

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

