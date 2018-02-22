import DS from 'ember-data';

export default DS.Model.extend({
   ID: DS.attr('string'),
   Name: DS.attr('string'),
   Location: DS.attr('string'),
   user: DS.belongsTo('user')
});
