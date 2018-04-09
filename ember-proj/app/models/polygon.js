import DS from 'ember-data';

export default DS.Model.extend({
   name: DS.attr('string'),
   polyType: DS.attr('poly-type'),
   location: DS.attr('string'),
   user: DS.belongsTo('user'),
   tasks: DS.hasMany('task'),
   notes: DS.hasMany('note'),
   startDate: DS.attr('string'),
   endDate: DS.attr('string'),
});
