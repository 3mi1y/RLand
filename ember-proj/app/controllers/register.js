import Controller from '@ember/controller';
import $ from 'jquery';

export default Controller.extend({
  actions: {
    register() {
      const street = this.get("street");
      const city = this.get("city");
      const state = this.get("state");
      const zip = this.get("zip");

      let address = "";
      if (street) { address += street + " "; }
      if (city) { address += city; }
      if (state) { address += ", " + state; }
      if (zip) { address += " " + zip; }

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
