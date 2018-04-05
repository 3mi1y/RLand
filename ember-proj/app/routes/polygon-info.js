import Route from '@ember/routing/route';
import RSVP from 'rsvp';

export default Route.extend({
   model(params) {
    // return this.store.findRecord('polygon', params.polygon_id)
      return RSVP.hash({
        polygon: this.store.findRecord('polygon', params.polygon_id),
        tasks: this.store.query('task', { polyId: params.polygon_id }),
        notes: this.store.query('note', { polyId: params.polygon_id})
      })
   }
});
