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
    let location = this.get('location').toString().trim();
    if (!location) {
      // no location set, so pick a default
      location = "Montana";
      // TODO: the location is set to Montana, but the map is zoomed in too far
    }
    let map = this.get('maps');
    let mapElement = map.getMapElement(location);
    this.$('.map-container').append(mapElement);

    //todo: Modify for our polygon models, as is causes transaction is null error
    // let polygons = this.get('polygons')();
    // polygons.then((results) => results.forEach((model) => {
    //   map.addPolygon(model.get('type'), model.get('shape'), model);
    // }, this));
  },

  polygon_selected(sender/*, key, value, rev*/)
  {
    let selected = sender.get('selected');
    this.send('polygonSelected', selected);

    if (selected) {
      $('.poly-list').hide();
      $('.new-poly').show();
    }
    else {
      $('.poly-list').show();
      $('.new-poly').hide();
    }
  },

  actions: {
    polygonSelected(polygon)
    {
      //todo: initiates request to save polygon, currently causes error
      this.get('polygonSelected')(polygon);
    },
    // select_year(year)
    // {
    //   let maps = this.get('maps');
    //   maps.clearAllPolygons();
    //   let polygons = this.get('polygons')(year);
    //   polygons.then((results) => results.forEach((model) => {
    //     maps.addPolygon(model.get('type'), model.get('shape'), model);
    //   }, this));
    // }
  }
});
