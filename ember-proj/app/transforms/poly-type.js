import DS from 'ember-data';

// TODO: choose serialization format and do verification
// currently this just assumes both sides of the data are an array

export default DS.Transform.extend({
  deserialize(serialized) {
    if (!serialized) {
      return null;
    }
    return serialized;
  },

  serialize(deserialized) {
    if (!deserialized) {
      return null;
    }
    return deserialized;
  }
});
