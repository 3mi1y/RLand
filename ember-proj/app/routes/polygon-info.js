import Route from '@ember/routing/route';
import RSVP from 'rsvp';

export default Route.extend({
   model(params) {
      return RSVP.hash({
        polygon: this.store.findRecord('polygon', params.polygon_id),
        tasks: this.get('store').findAll('task', { reload:true }).then((list) => {
           return list.filterBy('polyId', parseInt(params.polygon_id));
        }),
        notes: this.get('store').findAll('note', { reload:true }).then((list) => {
           return list.filterBy('polyId', parseInt(params.polygon_id));
        }),
        harvests: this.get('store').findAll('harvest', { reload:true }).then((list) => {
           return list.filterBy('polyId', parseInt(params.polygon_id));
        }),
      })
   }
});
