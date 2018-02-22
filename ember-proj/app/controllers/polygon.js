import Controller from '@ember/controller';
import $ from 'jquery';
import DS from 'ember-data';

export default Controller.extend({
  actions: {
    createPolygon() {
      let polygon = this.get('store').createRecord('polygon', { 'name': this.get("name"), 'location': this.get("location")});
      polygon.save();
    },

    getPolygons() {
      this.get('store').findAll('polygon').then(function(polygons) {
          polygons.forEach(function(p) {
            console.log(p.id);
          });
      })
    }
  }

         // console.log('You are tring to post a polygon');
         // $.post('http://localhost:8000/api/polygons/', {
         //    ID: this.get("ID"),
         //    Location: this.get("Location"),
         //    Name: this.get("Name")
         // }).then(reponse => {
         //    console.log('something happened')
         //    console.log(response)
         // })
     //  },
     //  createPolygonAdapter() {
     //     const polygon = this.store.createRecord('polygon', { 'ID': this.get("ID"), 'Name': this.get("Name"), 'Location': this.get("Location")})
     //     polygon.save();
     //  },
     //  getPolygons() {
     //     $.get("http://localhost:8000/api/polygons/", {
     //    }).then((response) => {
     //       console.log('I hate this')
     //       console.log(response)
     //    })
     //}

});
