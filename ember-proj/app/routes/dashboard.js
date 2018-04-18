import Route from '@ember/routing/route';
import RSVP from 'rsvp';

export default Route.extend({
  model(params) {
      return RSVP.hash({
         users: this.store.peekAll('user'),
         tasks: this.store.findAll('task')
      })
  }
});
