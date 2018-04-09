import Controller from '@ember/controller';

export default Controller.extend({
   actions: {
      newHarvest() {
         console.log(this.get('model').get('id'))
         let harvest = this.get('store').createRecord('harvest', {
            amount: this.get('amount'),
            polyId: this.get('model').get('id'),
            units: this.get('units')
         })
         harvest.save()
         this.transitionToRoute('harvests', this.get('model').get('id'))
      }
   }
});
