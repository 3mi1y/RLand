import Controller from '@ember/controller';

export default Controller.extend({
  actions: {
    change_password() {
      console.log(this.get("current_pw"), this.get("password"));
    },
    update_address() {
      this.get('store').findRecord('user', '@CURRENT_USER').then(user => {
        const newAddress = this.get("street") + " " + this.get("city") + ", " + this.get("state") + " " + this.get("zip");
        user.set("address", newAddress);
        user.save();
      });
    }
  }
});
