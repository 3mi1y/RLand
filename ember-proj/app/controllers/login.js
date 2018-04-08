import Controller from '@ember/controller';
import $ from 'jquery'

export default Controller.extend({
  authentication: Ember.inject.service('authentication'),
  //loginFailed: false,
  isProcessing: false,

  actions: {

    login() {
      this.setProperties({
        loginFailed: false,
        isProcessing: false
      });

      $.post("api/login", {
        email: this.get("email"),
        password: this.get("password")
      }).then(() => {
        // login reported success
        this.set("isProcessing", false);

        this.get('store').findRecord('user', this.get('email')).then(() => {
          // got user
          this.get('authentication').login();
          this.transitionToRoute('map')
        }, (response) => {
          // failed to get user
          $('#errors').text(response.errors[0].title);
          $('#errors').show();
        });
      }, () => {
        // login reported failure
        this.set("isProcessing", false);
        this.set("loginFailed", true);
      });
    },

    register() {
      this.transitionToRoute('register');
    }
  }
});
