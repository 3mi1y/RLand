import Controller from '@ember/controller';
import $ from 'jquery';

export default Controller.extend({
  authentication: Ember.inject.service('authentication'),
  //loggedIn: true,
  actions: {
     logout() {
        Ember.run(() => this.store.unloadAll())
        Ember.run(() => console.log(this.store.peekAll('polygon').get('length')))
        this.get('authentication').logout()
        $.get("api/logout").then(() => { console.log("Logged out on the server")})
        this.transitionToRoute('index')
     }
   }
});
