import Service from '@ember/service';
import { camelize } from '@ember/string';
import EmberObject from '@ember/object';
import Ember from 'ember';
import MapUtil from '../utils/google-maps';

const google = window.google;

export default Service.extend({
  store: Ember.inject.service(),

  selected: null,
  on_map_polygons: new Array(),

  init() {
    if (!this.get('cachedMaps')) {
      this.set('cachedMaps', EmberObject.create());
    }
    if (!this.get('mapUtil')) {
      this.set('mapUtil', MapUtil.create());
    }
    if (!this.get('selected'))
    {
      this.set('selected', null);
    }
  },

  getMapElement(location) {
    let camelizedLocation = location.camelize();
    let element = this.get(`cachedMaps.${camelizedLocation}`);
    if (!element) {
      element = this.createMapElement();
      let map = this.get('mapUtil').createMap(element, location);

      this.set(`cachedMaps.${camelizedLocation}`, element);
      this.set('map', map);

      this.initDrawingManager();
    }
    return element;
  },

  createMapElement() {
    let element = document.createElement('div');
    element.className = 'map';
    return element;
  },

  clearSelected()
  {
    let previous = this.get('selected');
    if (previous)
    {
      previous.setEditable(false);
      previous.setDraggable(false);
    }
    this.set('selected', null);
  },

  setSelectedShape(shape)
  {
    this.clearSelected();
    shape.setEditable(true);
    shape.setDraggable(true);
    this.set('selected', shape);
  },

  initDrawingManager()
  {
    let drawing = new google.maps.drawing.DrawingManager({
      drawingControlOptions: {
        position: google.maps.ControlPosition.TOP_CENTER,
        drawingModes: ['circle','polygon','rectangle']
      },
      polygonOptions: {
        draggable: true,
        editable: true,
        clickable: true
      },
      rectangleOptions: {
        draggable: true,
        editable: true,
        clickable: true
      },
      circleOptions: {
        draggable: true,
        editable: true,
        clickable: true
      },

    });

    let setSelected = (shape) => this.setSelectedShape(shape);
    let addPolygonListener = (overlay) => this.addPolygonListener(overlay);
    let parent = this;

    google.maps.event.addListener(this.get('map'), 'click', () => this.clearSelected());
    google.maps.event.addListener(drawing, 'overlaycomplete', function (e) {
      drawing.setDrawingMode(null);
      e.overlay.setEditable(false);
      setSelected(e.overlay);
      addPolygonListener(e.overlay);
      if (e.type == google.maps.drawing.OverlayType.CIRCLE) {
        console.log("omg its a circle");
      }
      else if (e.type == google.maps.drawing.OverlayType.RECTANGLE) {
        console.log(e.overlay.getBounds());
        console.log("omg its a rectangle");
      }
      else {
        console.log("omg its a polygon");
        parent.get('selected').model.set('location', JSON.stringify({path: e.overlay.getPath().getArray()}));
        console.log(parent.get('selected').model.get('location'));
      }
    });

    drawing.setMap(this.get('map'));
  },

  addPolygonListener(overlay)
  {
    var setSelected = (shape) => this.setSelectedShape(shape);
    var getSelected = () => this.get('selected');
    var clearSelected = () => this.clearSelected();
    google.maps.event.addListener(overlay, 'click', function () {
      setSelected(this);
      console.log(this.getPath().getArray());
    });

    parent = this;
    google.maps.event.addDomListener(document, 'keyup', function (e) {
      let code = e.which;
      if (code === 46)
      {
        let selected = getSelected();
        parent.get('controllers.map').send('deletepolygon', selected.model);
        deletePolygon(selected.model);
        clearSelected();
      }
    });
  },

  addPolygon(type, shape, model)
  {
    let rectangle = new google.maps.Rectangle({
      map: this.get('map'),
      bounds: shape,
      clickable: true,
    });

    rectangle.set('model', model);
    this.addPolygonListener(rectangle);
    this.on_map_polygons.push(rectangle);
  },

  clearAllPolygons()
  {
    this.on_map_polygons.forEach((polygon) => polygon.setMap(null));
    this.on_map_polygons = new Array();
    this.clearSelected();
  }
});
