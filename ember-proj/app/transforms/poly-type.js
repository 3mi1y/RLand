import DS from 'ember-data';

// TODO: choose serialization format and do verification
// currently this just assumes both sides of the data are an array
export default DS.Transform.extend({
  deserialize(serialized) {
    return serialized;
  },

  serialize(deserialized) {
    return deserialized;
  }
});
