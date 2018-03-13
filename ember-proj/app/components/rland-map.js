import Ember from 'ember';

export default Ember.Component.extend({
  maps: Ember.inject.service(),
  classNames: "rland-map",

  init()
  {
    this._super(...arguments);
    this.get('maps').addObserver('selected', this, 'polygon_selected');
  },

  didInsertElement()
  {
    this._super(...arguments);
    let location = this.get('location');
    let map = this.get('maps');
    let mapElement = map.getMapElement(location);
    this.$('.map-container').append(mapElement);

  //   let polygons = this.get('polygons')();
  //   polygons.then((results) => results.forEach((model) => {
  //     map.addPolygon(model.get('type'), model.get('shape'), model);
  //   }, this));
  // },
  //
  // polygon_selected(sender/*, key, value, rev*/)
  // {
  //   let selected = sender.get('selected');
  //   this.send('polygonSelected', selected);
  //
  //   if (selected)
  //     this.$('.polygon-info').velocity({translateX: "-400px"}, {duration: 'fast'});
  //   else
  //     this.$('.polygon-info').velocity({translateX: "0px"}, {duration: 'fast'});
  // },
  //
  // actions: {
  //   polygonSelected(polygon)
  //   {
  //     this.get('polygonSelected')(polygon);
  //   },
  //
  //   select_year(year)
  //   {
  //     let maps = this.get('maps');
  //     maps.clearAllPolygons();
  //     let polygons = this.get('polygons')(year);
  //     polygons.then((results) => results.forEach((model) => {
  //       maps.addPolygon(model.get('type'), model.get('shape'), model);
  //     }, this));
  //   }
  }
});
// import Component from '@ember/component';
// import { inject as service } from '@ember/service';
//
// export default Component.extend({
//   maps: service(),
//   classNames: "rland-map",
//
//   init()
//   {
//     this._super(...arguments);
//     // this.get('maps').addObserver('selected', this, 'polygon_selected');
//   },
//
//   didInsertElement() {
//     this._super(...arguments);
//     let location = this.get('location');
//     let mapElement = this.get('maps').getMapElement(location);
//     this.$('.map-container').append(mapElement);
//   }
// });
