import Service from '@ember/service';
import $ from 'jquery';

export default Service.extend({
  get_tree() {
    var promise = this.get('_tree_promise');
    if (!promise) {
      promise = $.get("/api/polygon_type_tree").then(data => {
        if (data.data) {
          return data.data;
        } else {
          throw new Error("Invalid format for tree data");
        }
      }).catch(err => {
        console.log("Error loading tree", err);
        this.set('_tree_promise', null);
      });

      this.set('_tree_promise', promise);
    }
    return promise;
  }
});
