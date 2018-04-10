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
        // TODO: this duplicates register.js
        const street = this.get("street");
        const city = this.get("city");
        const state = this.get("state");
        const zip = this.get("zip");

        let address = "";
        if (street) { address += street + " "; }
        if (city) { address += city; }
        if (state) { address += ", " + state; }
        if (zip) { address += " " + zip; }

        user.set("address", address);
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
