import Controller from '@ember/controller';
import $ from 'jquery';

export default Controller.extend({
  actions: {
    register() {
      const address = this.get("street") + " " + this.get("city") + ", " + this.get("state") + " " + this.get("zip");

      const user = this.get('store').createRecord('user', {
        name: this.get("name"),
        email: this.get("email"),
        password: this.get("password"),
        address: address,
        polygons: []
      });
      user.save().then(() => {
          this.get('store').unloadAll();
          this.transitionToRoute('login')
        },
        (response) => {
          $('#errors').text(response.errors[0].title);
          $('#errors').show();
      })
    }
  }
});
