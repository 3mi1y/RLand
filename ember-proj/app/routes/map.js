import Route from '@ember/routing/route';
import RSVP from 'rsvp';

export default Route.extend({
  model() {
    return RSVP.hash({
      polygons: this.get('store').findAll('polygon'),
      address: this.get('store').findRecord('user', '@CURRENT_USER').then(user => user.get('address')),
    });
  },
});
