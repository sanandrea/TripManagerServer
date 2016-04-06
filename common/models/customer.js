// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
// 
//
//  Copyright © 2016 Andi Palo
//  This file is part of project: Simple Loopback Server
//
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

  Customer.observe('before delete', function checkIsAdmin(ctx, next) {
    //admin can delete admin
    //manager can delete manager
    //manager cannot delete admin
    var reqCtx = loopback.getCurrentContext();
    var userId = reqCtx.get('accessToken').userId;
    var RoleMapping = Customer.app.models.RoleMapping;

    //find the Customer doing the call
    RoleMapping.find({where: {principalId: userId}, include:'role'}, function(err, roleMap) {
      if (err) next(err);
      if (roleMap.length === 1) {
        var roleMapDeleter = roleMap[0].toJSON();

        //find the Customer to delete
        RoleMapping.find({where: {principalId: ctx.where.id}, include:'role'}, function(err, roleMap) {
          if (err) next(err);
          if (roleMap.length === 1) {
            var roleMapToDelete = roleMap[0].toJSON();
            if(roleMapToDelete.role.name == 'manager'){
              //It is a manager so proceed
              next();
            }else if (roleMapToDelete.role.name === roleMapDeleter.role.name){
              //admin can delete admin
              next();
            }else{
              var err = new Error("Customer has no permissions to delete this Customer");
              err.statusCode = 403;
              next(err);
            }
          }else{
            //the Customer to delete is regular one so, PROCEED
            next();
          }
        });
      }else{
        var err = new Error("Customer is not an Admin or Manager, cannot delete");
        err.statusCode = 403;
        next(err);
      }
    });
  });
};
