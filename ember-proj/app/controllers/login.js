import Controller from '@ember/controller';
import $ from 'jquery'

export default Controller.extend({
  loginFailed: false,
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
      }).then(function () {
          this.set("isProcessing", false);
          user.save().then(() => {
              this.transitionToRoute('dashboard')},
            (response) => {
              $('#errors').text(response.errors[0].title);-
              $('#errors').show();
            })
        }.bind(this),

        function () {
          this.set("isProcessing", false);
          this.set("loginFailed", true);
        }.bind(this));
    }
  }
});
