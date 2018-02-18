import Controller from '@ember/controller';
import $ from 'jquery'

export default Controller.extend({
  loginFailed: false,
  isProcessing: false,
  registerFailed: false,
  isRegistered: true,

  actions: {

    login() {
      this.setProperties({
        loginFailed: false,
        isProcessing: false
      });

      $.post("http://localhost:8000/api/login", {
        email: this.get("username"),
        password: this.get("password")
      }).then(function () {
          this.set("isProcessing", false);
          document.location = '/';
        }.bind(this),

        function () {
          console.log(arguments);
          this.set("isProcessing", false);
          this.set("loginFailed", true);
        }.bind(this));
    },

    register() {
      this.setProperties({
        registerFailed: false,
        isProcessing: false
      });

      $.post("http://localhost:8000/api/signup", {
        email: this.get("email"),
        name: this.get("username"),
        password: this.get("password")
      }).then(function () {
          this.set("isProcessing", false);
          document.location = '/sign-in';
        }.bind(this),

        function () {
          console.log(arguments);
          this.set("isProcessing", false);
          this.set("registerFailed", true);
        }.bind(this));
    }
  }
});
