package payment

import (
	"net/http"
	"os"

	"github.com/go-kit/kit/log"
	"golang.org/x/net/context"

	kitprometheus "github.com/go-kit/kit/metrics/prometheus"
	stdopentracing "github.com/opentracing/opentracing-go"
	stdprometheus "github.com/prometheus/client_golang/prometheus"
)

func WireUp(ctx context.Context, declineAmount float32, tracer stdopentracing.Tracer) (http.Handler, log.Logger) {
	// Log domain.
	var logger log.Logger
	{
		logger = log.NewLogfmtLogger(os.Stderr)
		logger = log.NewContext(logger).With("ts", log.DefaultTimestampUTC)
		logger = log.NewContext(logger).With("caller", log.DefaultCaller)
	}

	fieldKeys := []string{"method"}
	// Service domain.
	var service Service
	{
		service = NewAuthorisationService(declineAmount)
		service = LoggingMiddleware(logger)(service)
		service = NewInstrumentingService(
			kitprometheus.NewCounterFrom(
				stdprometheus.CounterOpts{
					Namespace: "http",
					Subsystem: "requests",
					Name:      "total",
					Help:      "Number of requests received.",
				},
				fieldKeys),
			kitprometheus.NewSummaryFrom(stdprometheus.SummaryOpts{
				Namespace: "http",
				Subsystem: "request",
				Name:      "duration_microseconds_sum",
				Help:      "Total duration of requests in microseconds.",
			}, fieldKeys),
			service,
		)
	}

	// Endpoint domain.
	endpoints := MakeEndpoints(service, tracer)

	handler := MakeHTTPHandler(ctx, endpoints, logger, tracer)
	return handler, logger
}
