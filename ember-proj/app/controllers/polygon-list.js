import Controller from '@ember/controller';

export default Controller.extend({
   actions: {
      getPolygons() {
      this.get('store').findAll('polygon').then(function(polygons) {
          polygons.forEach(function(p) {
            console.log(p.id);
          });
      })
    }
   }
});
