import Controller from '@ember/controller';

export default Controller.extend({
   actions: {
      addTask() {
         let task = this.get('store').createRecord('task', {
            name: this.get('name'),
            description: this.get('description'),
            dueDate: this.get('dueDate'),
            priority: this.get('priority')
         })
         task.save()
      }
   }
});
