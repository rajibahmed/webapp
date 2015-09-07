import DS from 'ember-data';

export default DS.Model.extend({
    name: DS.attr('string'),
    age: DS.attr('number'),
    location: DS.attr('string'),
    ip: DS.attr('string')
});
