import Controller from '@ember/controller';

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
      user.save()
    }
  }
});
