import argparse
import asyncio
import logging
import pickle
import ssl
import struct
from typing import Optional, cast

from aioquic.asyncio.client import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived
from aioquic.quic.logger import QuicFileLogger
from pymavlink import mavutil

logger = logging.getLogger("client")
MAVLINK_MSG_ID_HEARTBEAT = 0

class utm_traffic_info(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._heartbeat_waiter: Optional[asyncio.Future[bytes]] = None
        self.last_system_time = float("-inf")
        self.should_exit = False  # Flag to indicate whether to exit

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

    async def receive_trafficinfo(self) -> bytes:
        waiter = self._loop.create_future()
        self._heartbeat_waiter = waiter
        return await asyncio.shield(waiter)

    async def send_start_message(self) -> None:
        payload = struct.pack("<BBBBI", 0, 0, 0, 0, 0)  # Additional fields for heartbeat
        struct.pack("<B", MAVLINK_MSG_ID_HEARTBEAT) + payload
        stream_id = self._quic.get_next_available_stream_id()
        self._quic.send_stream_data(stream_id, payload, end_stream=True)
        self.transmit()

    def quic_event_received(self, event: QuicEvent) -> None:
        if self._heartbeat_waiter is not None:
            if isinstance(event, StreamDataReceived):
                msg = event.data.decode()
                print("Received data:", msg, end="\n")
                self.parse(msg)
                waiter = self._heartbeat_waiter
                self._heartbeat_waiter = None
                waiter.set_result(msg)

                if self.should_exit:
                    self._quic.close()
                    asyncio.get_event_loop().stop()

def save_session_ticket(ticket):
    logger.info("New session ticket received")
    if args.session_ticket:
        with open(args.session_ticket, "wb") as fp:
            pickle.dump(ticket, fp)

async def main(
    configuration: QuicConfiguration,
    host: str,
    port: int,
) -> None:
    logger.debug(f"Connecting to {host}:{port}")
    async with connect(
        host,
        port,
        configuration=configuration,
        session_ticket_handler=save_session_ticket,
        create_protocol=utm_traffic_info,
    ) as client:
        client = cast(utm_traffic_info, client)
        logger.debug("Sending traffic info start msg")
        await client.send_start_message()
        answer = await client.receive_trafficinfo()
        logger.info("Received traffic info msg\n%s" % answer)

        try:
            while not client.should_exit:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("Ctrl+C detected. Initiating graceful exit.")
            client.should_exit = True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UTMSDSP traffic information over QUIC client")
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="The remote peer's host name or IP address",
    )
    parser.add_argument(
        "--port", type=int, default=853, help="The remote peer's port number"
    )
    parser.add_argument(
        "-k",
        "--insecure",
        action="store_true",
        help="do not validate server certificate",
    )
    parser.add_argument(
        "--ca-certs", type=str, help="load CA certificates from the specified file"
    )
    parser.add_argument(
        "-q",
        "--quic-log",
        type=str,
        help="log QUIC events to QLOG files in the specified directory",
    )
    parser.add_argument(
        "-l",
        "--secrets-log",
        type=str,
        help="log secrets to a file, for use with Wireshark",
    )
    parser.add_argument(
        "-s",
        "--session-ticket",
        type=str,
        help="read and write session ticket from the specified file",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase logging verbosity"
    )

    args = parser.parse_args()

    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        level=logging.DEBUG if args.verbose else logging.INFO,
    )

    configuration = QuicConfiguration(alpn_protocols=["doq"], is_client=True)
    if args.ca_certs:
        configuration.load_verify_locations(args.ca_certs)
    if args.insecure:
        configuration.verify_mode = ssl.CERT_NONE
    if args.quic_log:
        configuration.quic_logger = QuicFileLogger(args.quic_log)
    if args.secrets_log:
        configuration.secrets_log_file = open(args.secrets_log, "a")
    if args.session_ticket:
        try:
            with open(args.session_ticket, "rb") as fp:
                configuration.session_ticket = pickle.load(fp)
        except FileNotFoundError:
            logger.debug(f"Unable to read {args.session_ticket}")
            pass
    else:
        logger.debug("No session ticket defined...")

    asyncio.run(
        main(
            configuration=configuration,
            host=args.host,
            port=args.port,
        )
    )

