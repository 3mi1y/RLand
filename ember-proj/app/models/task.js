import DS from 'ember-data';

export default DS.Model.extend({
   name: DS.attr('string'),
   description: DS.attr('string'),
   priority: DS.attr('number'),
   polyId: DS.attr('number'),
   dueDate: DS.attr('string'),
   completed: DS.attr('boolean'),
   polygon: DS.belongsTo('polygon')
});
