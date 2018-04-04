import Route from '@ember/routing/route';

export default Route.extend({
   model(params) {
     console.log(params.task_id)
     return this.store.findRecord('task', params.task_id)
   }
});
