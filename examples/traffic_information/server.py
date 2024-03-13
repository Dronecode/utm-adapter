import argparse
import asyncio
import logging
import struct
from typing import Dict, Optional

from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived
from aioquic.quic.logger import QuicFileLogger
from aioquic.tls import SessionTicket
from aioquic.quic.logger import QuicFileLogger

logger = logging.getLogger("server")

# Define MAVLink message IDs
MAVLINK_MSG_ID_HEARTBEAT = 0

class MavlinkHeartbeat:
    def __init__(self, system_id: int, component_id: int):
        self.system_id = system_id
        self.component_id = component_id

    def pack(self) -> bytes:
        payload = struct.pack("<BBBBI", 0, 1, 2, 3, 4)  # Placeholer for ADSB data
        return struct.pack("<B", MAVLINK_MSG_ID_HEARTBEAT) + payload


class DnsServerProtocol(QuicConnectionProtocol):
    def quic_event_received(self, event: QuicEvent):
        if isinstance(event, StreamDataReceived):

            heartbeat = MavlinkHeartbeat(system_id=1, component_id=1)
            heartbeat_data = heartbeat.pack()
            logger.info("Send traffic info")
            # send answer
            self._quic.send_stream_data(event.stream_id, heartbeat_data, end_stream=True)


class SessionTicketStore:
    """
    Simple in-memory store for session tickets.
    """

    def __init__(self) -> None:
        self.tickets: Dict[bytes, SessionTicket] = {}

    def add(self, ticket: SessionTicket) -> None:
        self.tickets[ticket.ticket] = ticket

    def pop(self, label: bytes) -> Optional[SessionTicket]:
        return self.tickets.pop(label, None)


async def main(
    host: str,
    port: int,
    configuration: QuicConfiguration,
    session_ticket_store: SessionTicketStore,
    retry: bool,
) -> None:
    await serve(
        host,
        port,
        configuration=configuration,
        create_protocol=DnsServerProtocol,
        session_ticket_fetcher=session_ticket_store.pop,
        session_ticket_handler=session_ticket_store.add,
        retry=retry,
    )
    await asyncio.Future()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UTM SDSP traffic information over QUIC server")
    parser.add_argument(
        "--host",
        type=str,
        default="::",
        help="listen on the specified address (defaults to ::)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=853,
        help="listen on the specified port (defaults to 853)",
    )
    parser.add_argument(
        "-k",
        "--private-key",
        type=str,
        help="load the TLS private key from the specified file",
    )
    parser.add_argument(
        "-c",
        "--certificate",
        type=str,
        required=True,
        help="load the TLS certificate from the specified file",
    )
    parser.add_argument(
        "--retry",
        action="store_true",
        help="send a retry for new connections",
    )
    parser.add_argument(
        "-q",
        "--quic-log",
        type=str,
        help="log QUIC events to QLOG files in the specified directory",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase logging verbosity"
    )

    args = parser.parse_args()

    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        level=logging.DEBUG if args.verbose else logging.INFO,
    )

    # create QUIC logger
    if args.quic_log:
        quic_logger = QuicFileLogger(args.quic_log)

    configuration = QuicConfiguration(
        alpn_protocols=["doq"],
        is_client=False,
    )

    configuration.load_cert_chain(args.certificate, args.private_key)

    try:
        asyncio.run(
            main(
                host=args.host,
                port=args.port,
                configuration=configuration,
                session_ticket_store=SessionTicketStore(),
                retry=args.retry,
            )
        )
    except KeyboardInterrupt:
        pass
