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
