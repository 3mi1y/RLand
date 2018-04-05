import Controller from '@ember/controller';

export default Controller.extend({
   actions: {
      newNote() {
            let note = this.get('store').createRecord('note', {
               title: this.get('title'),
               polyId: this.get('model').get('id'),
               content: this.get('notecontent')
            })
            note.save()
            this.transitionToRoute('notes', this.get('model').get('id')) 
         }
   }
});