import Controller from '@ember/controller';

export default Controller.extend({
  //todo: Add attributes to indicate potential errors and display on register page
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
        () => {
        console.log("error")
      })
    }
  }
});
