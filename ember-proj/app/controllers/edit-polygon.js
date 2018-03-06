import Controller from '@ember/controller';

export default Controller.extend({
   actions: {
      submitChangedPolygon (id) {
         let location = this.get('location')
         let name = this.get('name')
         this.store.findRecord('polygon', id).then((changedPolygon) => {
            changedPolygon.set('name', name)
            changedPolygon.set('location', location)
            changedPolygon.save()
         }).then(
            this.transitionToRoute('polygon-list')
         )
      }
   }
});
