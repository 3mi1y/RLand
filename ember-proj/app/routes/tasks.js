import Route from '@ember/routing/route';

export default Route.extend({
   model(params) {
      return this.get('store').findAll('task').then((list) => {
         return list.filterBy('polyId', parseInt(params.polygon_id));
      })
   }
});
