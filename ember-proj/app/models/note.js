import DS from 'ember-data';

export default DS.Model.extend({
   polyId: DS.attr('number'),
   date: DS.attr('string', {
      defaultValue() { return new Date(); }
   }),
   title: DS.attr('string'),
   content: DS.attr('string')
});
