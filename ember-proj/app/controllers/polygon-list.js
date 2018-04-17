import Controller from '@ember/controller';

export default Controller.extend({
   actions: {
     deletePolygon(polygon) {
       this.store.findRecord('polygon', polygon.get('id')).then((post) => {
          post.destroyRecord();
       })
     }
   }
});
