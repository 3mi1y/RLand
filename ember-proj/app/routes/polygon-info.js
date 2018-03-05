import Route from '@ember/routing/route';

export default Route.extend({
   model(params) {
     //console.log(this.store.recordIsLoaded('polygon', params.poalygon_id))
     return this.store.findRecord('polygon', 1)
   }
});
