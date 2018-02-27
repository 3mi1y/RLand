import Component from '@ember/component';
import { inject as service } from '@ember/service';

export default Component.extend({
  maps: service(),
  classNames: "rland-map",

  init()
  {
    this._super(...arguments);
    // this.get('maps').addObserver('selected', this, 'polygon_selected');
  },

  didInsertElement() {
    this._super(...arguments);
    let location = this.get('location');
    let mapElement = this.get('maps').getMapElement(location);
    this.$('.map-container').append(mapElement);
  }
});
