import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr('string'),
  email: DS.attr('string'),
  password: DS.attr('string'),
  address: DS.attr('string'),
  polygons: DS.hasMany('polygon')
});
