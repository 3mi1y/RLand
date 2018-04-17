import Controller from '@ember/controller';

export default Controller.extend({
   actions: {
      addTask() {
         console.log(this.get('model').get('id'))
         let task = this.get('store').createRecord('task', {
            name: this.get('name'),
            polyId: this.get('model').get('id'),
            description: this.get('description'),
            dueDate: this.get('dueDate'),
            priority: this.get('priority')
         })
         task.save().then(
            this.transitionToRoute('tasks', this.get('model').get('id'))
         )
      }
   }
});
