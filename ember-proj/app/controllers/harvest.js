import Controller from '@ember/controller';

export default Controller.extend({
   actions: {
      deleteHarvest(harvest) {
         this.store.findRecord('harvest', harvest.get('id')).then((harvest) => {
            harvest.destroyRecord().then(
               this.transitionToRoute('confirmation')
            )
         })
      }
   }
});
