| Method | Name         | Error                                                                               | Occurrences |
|--------|--------------|-------------------------------------------------------------------------------------|-------------|
| POST   | /users       | HTTPError('500 Server Error: Internal Server Error for url: /users')                | 26605       |
| GET    | /reviews     | ConnectionResetError(54, 'Connection reset by peer')                                 | 1196        |
| POST   | /users       | ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x....>, 'Connection to localhost timed out. (connect timeout=None)') | 2168        |
| GET    | /reviews     | ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x....>, 'Connection to localhost timed out. (connect timeout=None)') | 1657        |
| GET    | /reviews     | RemoteDisconnected('Remote end closed connection without response')                | 151         |
| POST   | /users       | HTTPError('403 Client Error: Forbidden for url: /users')                            | 123         |
| GET    | /businesses  | ConnectionResetError(54, 'Connection reset by peer')                                 | 874         |
| GET    | /businesses  | RemoteDisconnected('Remote end closed connection without response')                 | 115         |
| GET    | /health      | ConnectionResetError(54, 'Connection reset by peer')                                 | 8728        |
| GET    | /health      | RemoteDisconnected('Remote end closed connection without response')                 | 140         |
| GET    | /businesses  | ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x....>, 'Connection to localhost timed out. (connect timeout=None)') | 746         |
| GET    | /health      | ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x....>, 'Connection to localhost timed out. (connect timeout=None)') | 3326        |
| POST   | /users       | ConnectionResetError(54, 'Connection reset by peer')                                 | 3858        |
| POST   | /users       | RemoteDisconnected('Remote end closed connection without response')                 | 117         |
