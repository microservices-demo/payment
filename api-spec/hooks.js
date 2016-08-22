const hooks = require('hooks');

// Setup database connection before Dredd starts testing
hooks.beforeAll((transactions, done) => {
    done();
});

// Close database connection after Dredd finishes testing
hooks.afterAll((transactions, done) => {
    done();   
});

hooks.beforeEach((transaction, done) => {
    done();
});

hooks.before("/paymentAuth > POST", function(transaction, done) {
    transaction.request.headers['Content-Type'] = 'application/json';
    transaction.request.body = JSON.stringify({
	"amount": 10.00
    });
    done();
});
