package payment

import (
	"github.com/go-kit/kit/log"
	"github.com/go-kit/kit/metrics"
	"time"
)

// Middleware decorates a service.
type Middleware func(Service) Service

// LoggingMiddleware logs method calls, parameters, results, and elapsed time.
func LoggingMiddleware(logger log.Logger) Middleware {
	return func(next Service) Service {
		return loggingMiddleware{
			next:   next,
			logger: logger,
		}
	}
}

type loggingMiddleware struct {
	next   Service
	logger log.Logger
}

func (mw loggingMiddleware) Authorise(amount float32) (auth Authorisation, err error) {
	defer func(begin time.Time) {
		mw.logger.Log(
			"method", "Authorise",
			"result", auth.Authorised,
			"took", time.Since(begin),
		)
	}(time.Now())
	return mw.next.Authorise(amount)
}

func (mw loggingMiddleware) Health() (health []Health) {
	defer func(begin time.Time) {
		mw.logger.Log(
			"method", "Health",
			"result", len(health),
			"took", time.Since(begin),
		)
	}(time.Now())
	return mw.next.Health()
}

type instrumentingService struct {
	requestCount   metrics.Counter
	requestLatency metrics.Histogram
	Service
}

// NewInstrumentingService returns an instance of an instrumenting Service.
func NewInstrumentingService(requestCount metrics.Counter, requestLatency metrics.Histogram, s Service) Service {
	return &instrumentingService{
		requestCount:   requestCount,
		requestLatency: requestLatency,
		Service:        s,
	}
}

func (s *instrumentingService) Authorise(amount float32) (auth Authorisation, err error) {
	defer func(begin time.Time) {
		s.requestCount.With("method", "authorise").Add(1)
		s.requestLatency.With("method", "authorise").Observe(time.Since(begin).Seconds())
	}(time.Now())

	return s.Service.Authorise(amount)
}

func (s *instrumentingService) Health() []Health {
	defer func(begin time.Time) {
		s.requestCount.With("method", "health").Add(1)
		s.requestLatency.With("method", "health").Observe(time.Since(begin).Seconds())
	}(time.Now())

	return s.Service.Health()
}
