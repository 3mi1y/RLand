import Route from '@ember/routing/route';

export default Route.extend({
  model() {
    this.get('store').push({
      data: [{
        id: 1,
        type: 'user',
        attributes: {
          email: 'user@portal.org',
          name: 'tempUser',
          password: 'tempUser',
          address: '123 Missoula Rd',
          polygons: []
        }
    }]
   })
  }
})
