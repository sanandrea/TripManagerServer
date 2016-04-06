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
    Customer.create({username: 'admin', password: 'test'},
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
        Role.upsert({name:'manager'}, function(err, role){
          if (err) throw err;
        });
      });
  });
};
