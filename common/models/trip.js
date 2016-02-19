module.exports = function(Trip) {
  //Operation hook to save user relation
  Trip.beforeRemote('create', function relationHook(ctx, instance, next) {
    console.log(typeof instance);
    instance.customer(ctx.req.accessToken.userId);
    next();
  });
};
