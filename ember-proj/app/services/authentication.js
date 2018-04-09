import Service from '@ember/service';

export default Service.extend({
   isLoggedIn: false,
   init() {
      this._super(...arguments);
      this.set('isLoggedIn', false);
      $.get("/api/users/@CURRENT_USER").then((data) => {
	if (data.data) {
          this.set('isLoggedIn', true);
        }
      });
   },
   login() {
      this.set('isLoggedIn', true);
   },
   logout() {
      this.set('isLoggedIn', false);
   },
   getStatus() {
      return this.isLoggedIn;
   }
});
