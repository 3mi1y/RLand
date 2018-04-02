import Route from '@ember/routing/route';
import RSVP from 'rsvp';

export default Route.extend({
    model(params) {
  	return this.get('store').query('note', { polyId: params.polygon_id})
/*
     return RSVP.hash({
       notes: this.get('store').findAll('note'),
       polygon: this.get('store').findRecord('polygon', params.polygon_id)
     })
*/ 
   }
});
