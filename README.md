# Tractors

A full-stack monorepo for a tractor supply machine-learning API.

## Requirements

* Python 3.13
* Docker

## How to Run

### Server

`docker build -t server .`

`docker run -d --name servercontainer -p 80:80 server`
