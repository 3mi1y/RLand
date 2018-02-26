import Ember from 'ember';

const google = window.google;

export default Ember.Service.extend({

  init() {
    this.set('geocoder', new google.maps.Geocoder());
  },

  createMap(element, location) {
    let map = new google.maps.Map(element, {
      scrollwheel: true,
      zoom: 20,
      tilt: 0,
      mapTypeId: google.maps.MapTypeId.HYBRID,
    });

    this.pinLocation(location, map);
    return map;
  },

  pinLocation(location, map) {
    this.get('geocoder').geocode({address: location}, (result, status) => {
      if (status === google.maps.GeocoderStatus.OK) {
        let geometry = result[0].geometry.location;
        let position = { lat: geometry.lat(), lng: geometry.lng() };
        map.setCenter(position);
      }
    });
  }

});
