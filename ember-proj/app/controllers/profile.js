import Controller from '@ember/controller';

export default Controller.extend({
  actions: {
    change_password() {
      this.get('store').findRecord('user', '@CURRENT_USER').then(user => {
        const newPass = this.get("password");
	const oldPass = this.get("current_pw");
        user.set("password", newPass);
	user.set("oldPassword", oldPass);
	// TODO: handle errors, redirect on success, etc.
        user.save();
      });
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
