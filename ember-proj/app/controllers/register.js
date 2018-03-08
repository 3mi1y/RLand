import Controller from '@ember/controller';
import $ from 'jquery';

export default Controller.extend({
  actions: {
    register() {
      const user = this.get('store').createRecord('user', {
        name: this.get("name"),
        email: this.get("email"),
        password: this.get("password"),
        address: this.get("address"),
        polygons: []
      });
      user.save().then(() => {
        this.transitionToRoute('login')},
        (response) => {
          $('#errors').text(response.errors[0].title)
          $('#errors').show()
      })
    }
  }
});
