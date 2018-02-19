import Controller from '@ember/controller';

export default Controller.extend({
   actions: {
      createPolygon() {
         console.log('You are tring to post a polygon');
         $.post('http://localhost:8000/api/polygons/', {
            ID: this.get("ID"),
            Location: this.get("Location"),
            Name: this.get("Name")
         }).then(reponse => {
            console.log('something happened')
            console.log(response)
         })
      },
      createPolygonAdapter() {
         const polygon = this.store.createRecord('polygon', { 'ID': this.get("ID"), 'Name': this.get("Name"), 'Location': this.get("Location")})
         polygon.save();
      },
      getPolygonsAdapter() {
         console.log(this.get('store').findAll('polygon'));
         return this.get('store').findAll('polygon');
      },
      getPolygons() {
         $.get("http://localhost:8000/api/polygons/", {
        }).then((response) => {
           console.log('I hate this')
           console.log(response)
        })
     }
   }
});
