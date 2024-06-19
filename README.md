First test
Отдача статического документа напрямую через Nginx

Finished 1000 requests

Document Path:          /static/sample.html
Document Length:        271 bytes

Concurrency Level:      10
Time taken for tests:   0.218 seconds
Complete requests:      1000
Failed requests:        0
Non-2xx responses:      1000
Total transferred:      451000 bytes
HTML transferred:       271000 bytes
Requests per second:    4584.34 [#/sec] (mean)
Time per request:       2.181 [ms] (mean)
Time per request:       0.218 [ms] (mean, across all concurrent requests)
Transfer rate:          2019.08 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Total:          0    1   4.1      1     112

Percentage of the requests served within a certain time (ms)
 100%    112 (longest request)
-------------------------------------------------------

Second test
Отдача статики через Gunicorn

Document Path:          /static/sample.html
Document Length:        34 bytes

Concurrency Level:      10
Time taken for tests:   0.501 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      173000 bytes
HTML transferred:       34000 bytes
Requests per second:    1997.32 [#/sec] (mean)
Time per request:       5.007 [ms] (mean)
Time per request:       0.501 [ms] (mean, across all concurrent requests)
Transfer rate:          337.44 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Total:          1    4   4.6      3     137

Percentage of the requests served within a certain time (ms)
 100%    137 (longest request)

------------------------------------------

Third test
Отдача динамического документа напрямую через Gunicorn

Document Path:          /
Document Length:        34 bytes

Concurrency Level:      10
Time taken for tests:   0.409 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      173000 bytes
HTML transferred:       34000 bytes
Requests per second:    2446.81 [#/sec] (mean)
Time per request:       4.087 [ms] (mean)
Time per request:       0.409 [ms] (mean, across all concurrent requests)
Transfer rate:          413.38 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Total:          1    4   3.6      3      35

Percentage of the requests served within a certain time (ms)
 100%     35 (longest request)

----------------------------------------------
Fourth test
Отдача динамического документа через проксирование запроса с Nginx на Gunicorn +кэш

Document Path:          /
Document Length:        10671 bytes

Concurrency Level:      10
Time taken for tests:   0.210 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      10945000 bytes
HTML transferred:       10671000 bytes
Requests per second:    4769.38 [#/sec] (mean)
Time per request:       2.097 [ms] (mean)
Time per request:       0.210 [ms] (mean, across all concurrent requests)
Transfer rate:          50977.37 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Total:          0    1   3.4      1      97

Percentage of the requests served within a certain time (ms)
 100%     97 (longest request)

----------------------------------------------------
Fifth test
Отдача динамического документа через проксирование запроса с Nginx на Gunicorn +кэш

Document Path:          /
Document Length:        10671 bytes

Concurrency Level:      10
Time taken for tests:   0.231 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      10945000 bytes
HTML transferred:       10671000 bytes
Requests per second:    4334.31 [#/sec] (mean)
Time per request:       2.307 [ms] (mean)
Time per request:       0.231 [ms] (mean, across all concurrent requests)
Transfer rate:          46327.22 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Total:          0    1   3.9      1     109

Percentage of the requests served within a certain time (ms)
 100%    109 (longest request)
-------------------------------------------



-----------------------------------------------------------------------------------------------------------------------------------------------------------

[![Join the chat at https://t.me/joinchat/ABFVWBE0AhkyyhREoaboXQ](https://img.shields.io/badge/Telegram-Group-orange?style=flat&logo=telegram)](https://t.me/joinchat/ABFVWBE0AhkyyhREoaboXQ) &nbsp;&nbsp;[![Join the chat at https://discord.gg/tYgADKx](https://img.shields.io/discord/719186998686122046?style=flat&label=Discord&logo=discord)](https://discord.gg/tYgADKx)

Centrifugo is a scalable real-time messaging server in language-agnostic way. Centrifugo works in conjunction with application backend written in any programming language. It runs as separate service and keeps persistent Websocket or SockJS connections from application clients (from web browsers or other environments like iOS/Android apps). When you need to deliver an event to your clients in real-time you publish it to Centrifugo API and Centrifugo then broadcasts event to all connected clients interested in this event (i.e. clients subscribed on event channel). In other words – this is a user-facing PUB/SUB server.

For more information follow to [Centrifugo documentation site](https://centrifugal.github.io/centrifugo/).

![scheme](https://raw.githubusercontent.com/centrifugal/centrifugo/master/docs/content/images/scheme_sketch.png)

You can also find the following posts interesting:
* [Four years in Centrifuge](https://medium.com/@fzambia/four-years-in-centrifuge-ce7a94e8b1a8) – this is a story and motivation of Centrifugo
* [Building real-time messaging server in Go](https://medium.com/@fzambia/building-real-time-messaging-server-in-go-5661c0a45248) – this is a write-up about some Centrifugo internals and decisions

### How to install

See [installation instructions](https://centrifugal.github.io/centrifugo/server/install/) in Centrifugo documentation.

### Demo

Try our [demo instance](https://centrifugo2.herokuapp.com/) on Heroku (admin password is `password`, token_hmac_secret_key is `secret`, API key is `api_key`). Or deploy your own Centrifugo instance in one click:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/centrifugal/centrifugo)

### Highlights

* Centrifugo is fast and capable to scale to millions of simultaneous connections
* Simple integration with any application – works as separate service
* Simple server API (HTTP or GRPC)
* Client-side libraries for popular frontend environments
* JSON and binary Protobuf Websocket client protocol based on strict schema
* SockJS polyfill for web browsers without Websocket support
* User authentication with JWT or over connection request proxy to configured HTTP endpoint
* Proper connection management and expiration control
* Various types of channels: private, user-limited
* Various types of subscriptions: client-side or server-side
* Transform RPC calls over WebSocket/SockJS to configured HTTP endpoint call
* Presence information for channels (show all active clients in channel)
* History information for channels (last messages published into channel)
* Join/leave events for channels (client goes online/offline)
* Automatic recovery of missed messages between client reconnects over configured retention period
* Built-in administrative web panel
* Cross platform – works on Linux, MacOS and Windows
* Ready to deploy (Docker, RPM/DEB packages, automatic Let's Encrypt TLS certificates, Prometheus/Graphite monitoring)
* MIT license
