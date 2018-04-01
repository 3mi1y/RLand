import Controller from '@ember/controller';

export default Controller.extend({
   actions: {
      getPolygons() {
         this.get('store').peekAll('polygon').then(function(polygons) {
            // polygons.forEach(function(p) {
             //console.log(p.id);
         //});
       })
     },
     deletePolygon(polygon) {
       this.store.findRecord('polygon', polygon.get('id')).then((post) => {
          post.destroyRecord();
       })
     }
   }
});
