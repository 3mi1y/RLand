import Controller from '@ember/controller';

export default Controller.extend({
  actions: {
    change_password() {
      this.setProperties({
        "password-success": false,
        "password-mismatch": false,
        "password-error": false,
      });
      this.get('store').findRecord('user', '@CURRENT_USER', { reload: true }).then(user => {
        const newPass = this.get("new_pw");
        const verifyPass = this.get("verify_pw");
        if (newPass == verifyPass) {
          const oldPass = this.get("current_pw");
          user.set("password", newPass);
          user.set("oldPassword", oldPass);
          user.save().then(() => {
            this.set("password-success", true);
            return user.reload();
          }, () => {
            this.set("password-error", true);
            user.rollbackAttributes();
          });
          this.setProperties({
            "current_pw": null,
            "new_pw": null,
            "verify_pw": null,
          });
        } else {
          this.set("password-mismatch", true);
        }
      });
    },
    update_address() {
      this.setProperties({
        "address-success": false,
        "address-error": false,
      });
      this.get('store').findRecord('user', '@CURRENT_USER', { reload: true }).then(user => {
        const newAddress = this.get("street") + " " + this.get("city") + ", " + this.get("state") + " " + this.get("zip");
        user.set("address", newAddress);
        user.save().then(() => {
          this.set("address-success", true);
          return user.reload();
        }, () => {
          this.set("address-error", true);
        });
      });
    }
  }
});
