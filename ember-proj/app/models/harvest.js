import DS from 'ember-data';

export default DS.Model.extend({
    date: DS.attr('string', { defaultValue() { return new Date(); } }),
    amount: DS.attr('number'),
    units: DS.attr('string'),
    polyId: DS.attr('number')
});
