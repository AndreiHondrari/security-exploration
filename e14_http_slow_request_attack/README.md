# Slow HTTP Request attack

## Pre-requisite steps

- start the `01_server.py` HTTP server

## Steps

- start `03_slow_client.py` (it will take a few seconds to run)
- while `03_slow_client.py` is still running, run quickly `02_normal_client.py`

## Observations

- the normal client will run only after the slow client is finished sending all
  the bytes
- the server will rotate between open sockets until one has data available, and
  will lock onto that socket until it finished serving it
- the normal client will be served very late, right after the slow client
  finished the last byte

## Probable outcomes

- if the slow client were to hang indefinitely, the server would be blocked on
  that specific request for ever, potentially halting the ability of a server
