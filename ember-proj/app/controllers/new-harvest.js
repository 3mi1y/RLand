import Controller from '@ember/controller';

export default Controller.extend({
   actions: {
      newHarvest() {
         let harvest = this.get('store').createRecord('harvest', {
            amount: this.get('amount'),
            polyId: this.get('model').get('id'),
            units: this.get('units')
         })
         harvest.save().then(
            this.transitionToRoute('polygon-info', this.get('model').get('id'))
         )
      }
   }
});
