[![Build Status](https://travis-ci.org/microservices-demo/payment.svg?branch=master)](https://travis-ci.org/microservices-demo/payment) [![Coverage Status](https://coveralls.io/repos/github/microservices-demo/payment/badge.svg?branch=master)](https://coveralls.io/github/microservices-demo/payment?branch=master)

# Payment
A microservices-demo service that provides payment services.
This build is built, tested and released by travis.

## Build

#### Go tools
In order to build the project locally you need to make sure that the repository directory is located in the correct
$GOPATH directory: $GOPATH/src/github.com/microservices-demo/payment/. Once that is in place you can build by running:

```
cd $GOPATH/src/github.com/microservices-demo/payment/cmd/paymentsvc/
go build -o payment
```

The result is a binary named `payment`, in the current directory.

#### Docker 
`GROUP=weaveworksdemos COMMIT=test ./scripts/build.sh`

## Test
`./test/test.sh < python testing file >`. For example: `./test/test.sh unit.py`

## Run 

#### Go native

If you followed to Go build instructions, you should have a "payment" binary in $GOPATH/src/github.com/microservices-demo/payment/cmd/paymentsvc/.
To run it use:
```
./payment
ts=2016-12-14T11:48:58Z caller=main.go:29 transport=HTTP port=8080
```

#### Docker

If you used Docker to build the payment project, the result should be a Docker image called `weaveworksdemos/payment`.
To run it use:
```
docker run --rm -p 8082:80 --name payment weaveworksdemos/payment
ts=2016-12-14T12:06:50Z caller=main.go:29 transport=HTTP port=80
```

You can now access the service via http://localhost:8082

## Use

To use the service start by doing a GET request to the health endpoint:

```
curl http://localhost:8082/health
{"health":[{"service":"payment","status":"OK","time":"2016-12-14 12:22:04.716316395 +0000 UTC"}]}
```

You can also authorise a payment by POSTing to the paymentAuth endpoint:

```
curl -H "Content-Type: application/json" -X POST -d'{"Amount":40}'  http://localhost:8082/paymentAuth
{"authorised":true}
```

## Push
`GROUP=weaveworksdemos COMMIT=test ./scripts/push.sh`
