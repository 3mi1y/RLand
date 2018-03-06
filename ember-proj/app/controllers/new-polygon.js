import Controller from '@ember/controller';

export default Controller.extend({
  actions: {
   createPolygon() {
      let polygon = this.get('store').createRecord('polygon', { 'name': this.get("name"), 'location': this.get("location")});
      polygon.save();
    },
  }
});
