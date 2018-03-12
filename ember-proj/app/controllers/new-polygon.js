import Controller from '@ember/controller';
export default Controller.extend({
  Hierarchy: [
     { name: 'Garden', leaves: [
           { name: 'Raised Bed', leaves: [
              { name: 'Vegetable', leaves: [
                 { name: 'Root Vegetable', leaves: [
                    { name: 'Potato' }
                 ]}
              ]},
              { name: 'Fruit', leaves: [
                 { name: 'Tiny fruits', leaves: [
                   { name: 'Grapes' }
                 ]}
              ]},
           ]},
           { name: 'Potted Plant', leaves: [
              { name: 'Fruit', leaves: [
                 { name: 'somehting else here...', leaves: [
                    { name: 'Tomatoe' }
                 ]}
              ]},
              { name: 'Vine', leaves: [
                 { name: 'vine one', leaves: [
                   { name: 'some stuff' }
                 ]}
              ]},
           ]}
        ]
     },
     { name: 'Structure', leaves: [
           { name: 'tractor', leaves: [
              { name: 'tractor 1', leaves: [
                 { name: 'tractor 1 level 4', leaves: [
                    { name: 'tractor 1 level 5' }
                 ]}
              ]},
              { name: 'tractor 2', leaves: [
                 { name: 'tractor 2 level 4', leaves: [
                   { name: 'tractor 2 level 5' }
                 ]}
              ]},
           ]},
           { name: 'house', leaves: [
              { name: 'house 1', leaves: [
                 { name: 'house 1 level 4', leaves: [
                    { name: 'house 1 level 5' }
                 ]}
              ]},
              { name: 'house 2', leaves: [
                 { name: 'house 2 level 4', leaves: [
                   { name: 'house 2 level 5' }
                 ]}
              ]},
           ]}
        ]
     },


  ],
  levelOne: ['Garden', 'Structure'],
  levelTwo: ['*'],
  levelThree: ['*'],
  levelFour: ['*'],
  levelFive: ['*'],
  selectedOptionOne: '*default level 1',
  selectedOptionTwo: '*default level 2',
  selectedOptionThree: '*default level 3',
  selectedOptionFour: '*default level 4',
  selectedOptionFive: '*default level 5',
  actions: {
   createPolygon() {
      let polygon = this.get('store').createRecord('polygon', { 'name': this.get("name"), 'location': this.get("location")});
      polygon.save();
    },
    updateLevelTwo(selectedOption) {
      let myArr = this.Hierarchy.filter(item => {
         return item.name === selectedOption
      }).map(item => {
         return item.leaves
      })[0].map(item => {
        return item.name
      })
      this.set('selectedOptionOne', selectedOption)
      this.set('levelTwo', myArr)
      return myArr
    },
    updateLevelThree(selectedOption) {
       let levThree = this.Hierarchy.filter(item => {
          return item.name === this.selectedOptionOne
       }).map(item => {
          return item.leaves
       })[0].filter(item => {
          return item.name === selectedOption
       })[0].leaves.map(item => {
          return item.name
       })
       this.set('selectedOptionTwo', selectedOption)
       this.set('levelThree', levThree)
    },
    updateLevelFour(selectedOption) {
       let levFour = this.Hierarchy.filter(item => {
          return item.name === this.selectedOptionOne
       }).map(item => {
          return item.leaves
       })[0].filter(item => {
          return item.name === selectedOptionTwo
       })[0].leaves.filter(item => {
          return item.name === selectedOption
       }).leaves.map(item => {
          return item.name
       })
       this.set('selectedOptionThree', selectedOption)
       this.set('levelFour', levFour)
       console.log(this.selectedOptionThree)
       console.log(this.levelFour)
    }
  }
});
