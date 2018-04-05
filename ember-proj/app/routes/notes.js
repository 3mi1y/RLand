import Route from '@ember/routing/route';
import RSVP from 'rsvp';

export default Route.extend({
    model(params) {
  	return this.get('store').findAll('note').then((list) => {
           return list.filterBy('polyId', parseInt(params.polygon_id));
        })
    }
});