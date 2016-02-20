module.exports = function(Trip) {
  var loopback = require('loopback');

  //Operation hook to save user relation
  Trip.observe('before save', function relationHook(ctx, next) {
    //get request context
    var reqCtx = loopback.getCurrentContext();
    // Get the current access token
    var userId = reqCtx.get('accessToken').userId;

    if (ctx.instance) {
      var Customer = Trip.app.models.Customer;
      Customer.findById(userId, function (err, customer){
        if(err) {
          console.log(err);
          next();
        }
        //console.log(customer);
        ctx.instance.customer(customer);
        //console.log(ctx.instance);
        next();
      });
    }else{
      next();
    }

  });
};
