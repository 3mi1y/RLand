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
    let setPolyModel = (polyObject) => this.setPolyModel(polyObject);

    google.maps.event.addListener(this.get('map'), 'click', () => this.clearSelected());
    google.maps.event.addListener(drawing, 'overlaycomplete', function (e) {
      drawing.setDrawingMode(null);
      e.overlay.setEditable(false);
      console.log(e.overlay);
      setSelected(e.overlay);
      addPolygonListener(e.overlay);
      setPolyModel(e);
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
    });

    let parent = this;
    google.maps.event.addDomListener(document, 'keyup', function (e) {
      let code = e.which;
      if (code === 46)
      {
        let selected = getSelected();
        parent.get('controllers.map').send('deletepolygon', selected.model);
        //deletePolygon(selected.model);
        clearSelected();
      }
    });
  },

  addPolygon(location, model)
  {
    if(location) {
      location = JSON.parse(location);
      let map = this.get('map');
      let shape = location.shape;
      let polygon = null;
      if (shape == google.maps.drawing.OverlayType.CIRCLE) {
        let center = location.center;
        let radius = location.radius;
        polygon = new google.maps.Circle({
          clickable: true,
          center: center,
          radius: radius,
          map: map
        });
      }
      else if (shape == google.maps.drawing.OverlayType.RECTANGLE) {
        let neBounds = location.neBounds;
        let swBounds = location.swBounds;
        polygon = new google.maps.Rectangle({
          clickable: true,
          map: map,
          bounds: {
            north: neBounds.lat,
            south: swBounds.lat,
            east: neBounds.lng,
            west: swBounds.lng
          }
        });
      }
      else {
        let path = location.path;
        console.log(path);
        polygon = new google.maps.Polygon({
          clickable: true,
          map: map,
          path: path
        });
      }
      this.addPolygonListener(polygon);
    }
    // let rectangle = new google.maps.Rectangle({
    //   map: this.get('map'),
    //   bounds: shape,
    //   clickable: true,
    // });
    //
    // rectangle.set('model', model);
    // this.addPolygonListener(rectangle);
    // this.on_map_polygons.push(rectangle);
  },

  clearAllPolygons()
  {
    this.on_map_polygons.forEach((polygon) => polygon.setMap(null));
    this.on_map_polygons = new Array();
    this.clearSelected();
  },

  setPolyModel(e)
  {
    let polygon = e.overlay;
    if (e.type == google.maps.drawing.OverlayType.CIRCLE) {
      polygon.model.set('location', JSON.stringify({
        shape: e.type,
        center: polygon.getCenter(),
        radius: polygon.getRadius()
      }));
      console.log(polygon.model.get('location'));
    }
    else if (e.type == google.maps.drawing.OverlayType.RECTANGLE) {
      let bounds = polygon.getBounds();
      polygon.model.set('location', JSON.stringify({
        shape: e.type,
        neBounds: bounds.getNorthEast(),
        swBounds: bounds.getSouthWest()}));
      console.log(polygon.model.get('location'));
    }
    else {
      polygon.model.set('location', JSON.stringify({shape: e.type, path: polygon.getPath().getArray()}));
      console.log(polygon.model.get('location'));
    }
  }
});
