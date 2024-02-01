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

logger = logging.getLogger("client")
MAVLINK_MSG_ID_HEARTBEAT = 0

class MavlinkClientProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._heartbeat_waiter: Optional[asyncio.Future[bytes]] = None

    async def receive_heartbeat(self) -> bytes:
        payload = struct.pack("<BBBBI", 0, 0, 0, 0, 0)  # Additional fields for heartbeat
        struct.pack("<B", MAVLINK_MSG_ID_HEARTBEAT) + payload
        stream_id = self._quic.get_next_available_stream_id()
        self._quic.send_stream_data(stream_id, payload, end_stream=True)
        waiter = self._loop.create_future()
        self._heartbeat_waiter = waiter
        self.transmit()
        return await asyncio.shield(waiter)


    def quic_event_received(self, event: QuicEvent) -> None:
        if self._heartbeat_waiter is not None:
            if isinstance(event, StreamDataReceived):
                # Parse MAVLink message
                length = struct.unpack("!B", bytes(event.data[:1]))[0]
                mavlink_message = event.data[1:1 + length]

                # Return MAVLink message
                waiter = self._heartbeat_waiter
                self._heartbeat_waiter = None
                waiter.set_result(mavlink_message)



def save_session_ticket(ticket):
    """
    Callback which is invoked by the TLS engine when a new session ticket
    is received.
    """
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
        create_protocol=MavlinkClientProtocol,
    ) as client:
        client = cast(MavlinkClientProtocol, client)
        logger.debug("Sending traffic info start msg")
        answer = await client.receive_heartbeat()
        logger.info("Received traffic info msg\n%s" % answer)


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
