import Controller from '@ember/controller';

export default Controller.extend({
  actions: {
    login() {
      $.post("/login", {
        username: this.get("username"),
        password: this.get("password")
      }).then(function() {
        document.location('welcome')
      }, function() {
        this.set("loginFailed", true)
      }).bind(this)
    }
  }
});
