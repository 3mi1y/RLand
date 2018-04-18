import Controller from '@ember/controller';

export default Controller.extend({
    actions: {
      deleteNote(note) {
         this.store.findRecord('note', note.get('id')).then((note) => {
          note.destroyRecord().then(
             this.transitionToRoute('confirmation')
          );
       })
      }
   }
});
