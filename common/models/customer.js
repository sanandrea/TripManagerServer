module.exports = function(Customer) {
  var loopback = require('loopback');
  Customer.listTrips = function(cb) {
    //get request context
    var reqCtx = loopback.getCurrentContext();
    // Get the current access token
    var userId = reqCtx.get('accessToken').userId;

    var Trip = Customer.app.models.Customer;
    Trip.find({where:{'customerId':userId}}, cb);
  };
  Customer.remoteMethod('listTrips', {
    returns: {arg: 'trips', type: 'array'},
    http: {path:'/list-trips', verb: 'get'}
  });
};
