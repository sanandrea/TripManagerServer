module.exports = function(app) {
  //we want to register users without mail at the moment
  delete app.models.Customer.validations.email;

  //add admin role
  var Customer = app.models.Customer;
  var Role = app.models.Role;
  var RoleMapping = app.models.RoleMapping;

  //only the first time it runs
  Customer.find({},function(err, customers){
    if(err) return console.log(err);
    if (customers.length > 0) return;
    Customer.create({username: 'admin', password: 'admin'},
      function(err, instance) {
        if (err) return console.log(err);
        Role.upsert({
          name: 'admin'
        }, function(err, role) {
          if (err) throw err;
          console.log('created role ', role);

          // Make customer an admin
          role.principals.create({
            principalType: RoleMapping.USER,
            principalId: instance.id
          }, function(err, principal) {
            if (err) throw err;
            console.log(principal);
          });
        });
      });
  });
};
