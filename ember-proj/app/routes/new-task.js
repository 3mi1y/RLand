import Route from '@ember/routing/route';

export default Route.extend({
   model(params) {
     return this.store.findRecord('polygon', params.polygon_id)
   },
   setupController: function(controller, model) {
      controller.set('params', this.get('params'))
      this._super(controller, model);
   }
});
