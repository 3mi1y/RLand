import Controller from '@ember/controller';

export default Controller.extend({
   actions: {
      submitChangedPolygon (id) {
         let loc = this.get('location');
         let name = this.get('name');
         let startDate = this.get('startDate');
         let endDate = this.get('endDate');

         this.store.findRecord('polygon', id).then((changedPolygon) => {
	    if (name) { changedPolygon.set('name', name); }
	    if (loc) { changedPolygon.set('location', loc); }
	    if (startDate) { changedPolygon.set('startDate', startDate); }
	    if (endDate) { changedPolygon.set('endDate', endDate); }
            changedPolygon.save();
         }).then(
            this.transitionToRoute('polygon-list')
         )
      }
   }
});
