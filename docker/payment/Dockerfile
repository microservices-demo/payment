FROM golang:1.6

RUN mkdir /app
COPY . /go/src/github.com/microservices-demo/payment/

RUN go get -v github.com/gorilla/mux github.com/go-kit/kit/log github.com/go-kit/kit/endpoint github.com/go-kit/kit/transport/http github.com/go-kit/kit/metrics/prometheus github.com/prometheus/client_golang/prometheus

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o /app/main github.com/microservices-demo/payment/cmd/paymentsvc

CMD ["/app/main", "-port=80"]

EXPOSE 80
