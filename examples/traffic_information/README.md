## Traffic Information client and server

A simple implementation of the traffic information server that uses QUIC and Mavlink messages. 

Client: `python3 client.py --ca-certs certs/pycacert.pem --port 8053`

Server: `python3 server.py --certificate certs/ssl_cert.pem --private-key certs/ssl_key.pem --port 8053 -input-file ../testdata/trafficsamples/singleHelicopterMakingUturn/traffic`

