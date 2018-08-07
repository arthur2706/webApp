# webApp
Web App to calc hash of msg

## To build the app

### build and start

clone repo and then:
```console
~$ docker build -t webapp .
~$ docker swarm init
~$ sudo mkdir -p /Users/docker/redis/data
~$ sudo chmod -R 777 /Users/docker/redis/data
~$ docker stack deploy -c docker-compose.yml webappstack
```

/messages takes a message (a string) as a POST and returns the SHA256 hash digest
of that message (in hexadecimal format)

try:
```console
~$ curl --silent "http://localhost:80/messages" -X POST -H "Content-Type: application/json" -d '{"message": "foo"}'
{"digest":"2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae"}
```

/messages/<hash> is a GET request that returns the original message. A request to a
non-existent <hash> should return a 404 error.

try:
```console
~$ curl --silent "http://localhost:80/messages/2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae"
{"message":"foo"}
```

### kill
```console
~$ docker stack rm webappstack
```

## bottle necks ?
redis instance wont scale if getting hit by massive amounts of users. 
need more micro services deployed. 
