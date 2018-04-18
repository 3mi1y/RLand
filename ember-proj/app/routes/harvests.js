import Route from '@ember/routing/route';

export default Route.extend({
   model(params) {
      //return this.get('store').query('harvest', { polyId: params.polygon_id})
      return this.get('store').findAll('harvest', { reload:true }).then((list) => {
           return list.filterBy('polyId', parseInt(params.polygon_id));
      })
   }
});
