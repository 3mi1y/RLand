import DS from 'ember-data';

export default DS.Model.extend({
   name: DS.attr('string'),
   type: DS.attr('poly-type'),
   location: DS.attr('string'),
   user: DS.belongsTo('user'),
   tasks: DS.hasMany('task'),
   startDate: DS.attr('date'),
   endDate: DS.attr('date'),
});
