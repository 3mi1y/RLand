
import EmberObject from '@ember/object';

const google = window.google;

export default EmberObject.extend({

  init() {
    this.set('geocoder', new google.maps.Geocoder());
  },

  createMap(element, location) {
    let map = new google.maps.Map(element, {
      scrollwheel: false,
      zoom: 20
    });
    this.pinLocation(location, map);
  },

  pinLocation(location, map) {
    this.get('geocoder').geocode({address: location}, (result, status) => {
      let geometry = result[0].geometry.location;
      let position = {lat: geometry.lat(), lng: geometry.lng()};
      map.setCenter(position);
      new google.maps.Marker({position, map, title: location});
    })
  }
})
