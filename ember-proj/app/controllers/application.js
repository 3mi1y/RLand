import Controller from '@ember/controller';

export default Controller.extend({
  authentication: Ember.inject.service('authentication'),
  //loggedIn: true,
  actions: {
     logout() {
       // console.log("From authentication service", this.get('authentication).isLoggedIn)
        this.store.unloadAll()
        this.get('authentication').logout()
        this.transitionToRoute('index')
     }
   }
});
