import Route from '@ember/routing/route';
import $ from 'jquery';

export default Route.extend({
  actions: {
    login() {
      $.post("api/login", {
        email: this.get("username"),
        password: this.get("password")
      }).then(function () {
          this.transitionTo('polygon');
      });
    },

    register() {
      this.setProperties({
        registerFailed: false,
        isProcessing: false
      });

      $.post("api/signup", {
        email: this.get("email"),
        name: this.get("username"),
        password: this.get("password")
      }).then(function () {
        this.transitionTo('sign-in');
      });
    }
  }
});
