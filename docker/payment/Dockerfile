FROM golang:1.14.2

RUN mkdir /app
COPY . /go/src/github.com/microservices-demo/payment/

RUN cd /go/src/github.com/microservices-demo/payment/ && go mod vendor

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o /app/main github.com/microservices-demo/payment/cmd/paymentsvc

CMD ["/app/main", "-port=80"]

#EXPOSE 80
