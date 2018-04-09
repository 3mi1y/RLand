import Controller from '@ember/controller';

export default Controller.extend({
   actions: {
      deleteTask(task) {
         this.store.findRecord('task', task.get('id')).then((post) => {
          post.destroyRecord();
       })
      },
      deleteNote(note) {
         this.store.findRecord('note', note.get('id')).then((post) => {
            post.destroyRecord()
         })
      }
   }
});
