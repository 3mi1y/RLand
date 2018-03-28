import Service from '@ember/service';
import $ from 'jquery';

export default Service.extend({
  get_tree() {
    var promise = this.get('_tree_promise');
    if (!promise) {
      promise = $.get("/api/polygon_type_tree").then(data => {
        return data.data;
      }, () => {
        console.log("Error loading tree");
      });

      this.set('_tree_promise', promise);
    }
    return promise;
  }
});
