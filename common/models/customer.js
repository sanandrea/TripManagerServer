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


  Customer.prototype.promote = function(cb){
    var userId = this.id;

    var RoleMapping = Customer.app.models.RoleMapping;
    var Role = Customer.app.models.Role;
    RoleMapping.find({where: {principalId: userId}}, function(err, roleMap) {
      if (err) throw err;
      if (roleMap.length === 1){
        //if role map exists it is a manager
        //promote to admin if not admin
        var roleMapInstance = roleMap[0];
        Role.find({where:{name: 'admin'}}, function(err,role){
          if(err) cb(err);
          var roleIns = role[0];
          roleMapInstance.updateAttribute('roleId',roleIns.id,function(err,ins){
            if(err) cb(err);
            cb(null,'ok');
          });
        });
      }else if (roleMap.length === 0){
        Role.find({where:{name: 'manager'}}, function(err,role){
          if (err) cb(err);
          if (role.length === 0){
            cb('manager role not yet defined');
            return;
          }

          var managerRole = role[0];
          managerRole.principals.create({
            principalType: RoleMapping.USER,
            principalId: userId
          }, function(err, principal) {
            if (err) cb(err);
            cb(null,'ok');
          });
        });
      }
    });
  };
  Customer.remoteMethod('promote',{
    isStatic:false,
    http:{path:'/promote',verb:'post'},
    returns: { arg: 'result', type: String }
  });
};
