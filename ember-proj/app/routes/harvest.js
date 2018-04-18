import Route from '@ember/routing/route';

export default Route.extend({
    model(params) {
      return this.store.findRecord('harvest', params.harvest_id)
   }
});
