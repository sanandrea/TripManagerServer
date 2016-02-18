//we want to register users without mail at the moment
module.exports = function(app) {
  delete app.models.Customer.validations.email;
};
