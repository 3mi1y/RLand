import Controller from '@ember/controller';
export default Controller.extend({
  Hierarchy: [
     { name: 'Structure/Equiptment/Other', leaves: [
           { name: 'Structure', leaves: [
              { name: 'House', leaves: [
                 { name: '*', leaves: [
                    { name: '*' }
                 ]}
              ]},
              { name: 'Barn (as is)', leaves: [
                 { name: '*', leaves: [
                   { name: '*' }
                 ]}
              ]},
              { name: 'Barn (with nested entities)', leaves: [
                 { name: '*', leaves: [
                   { name: '*' }
                 ]}
              ]},
              { name: 'Garage (as is)', leaves: [
                 { name: '*', leaves: [
                   { name: '*' }
                 ]}
              ]}
           ]},
           { name: 'Equiptment', leaves: [
              { name: 'Vehicle', leaves: [
                 { name: '*', leaves: [
                    { name: '*' }
                 ]}
              ]},
              { name: 'Tractor', leaves: [
                 { name: '*', leaves: [
                   { name: '*' }
                 ]}
              ]},
           ]}
        ]
     },
     { name: 'Plant', leaves: [
           { name: 'Beds (raised beds)', leaves: [
              { name: 'Vegetable &amp Fruit Garden (single crop)', leaves: [
                 { name: 'all possible veggie/fruit options', leaves: [
                    { name: 'veggie/fruit species' }
                 ]}
              ]},
              { name: 'Vegetable &amp Fruit Garden (multiple nested crops)', leaves: [
                 { name: 'all possible fruit/vegie options', leaves: [
                    { name: 'species' }
                 ]}
              ]},
              { name: 'Ornamental Garden (single crop)', leaves: [
                 { name: 'all possible ornamental options', leaves: [
                    { name: 'ornamental plants specific species names' }
                 ]}
              ]},
           ]},
           { name: 'Garden Patch/Area (NOT raised beds)', leaves: [
              { name: 'Vegetable & Fruit Garden (single crop)', leaves: [
                 { name: 'all possible veggie/fruit options', leaves: [
                    { name: 'veggie/fruit species' }
                 ]}
              ]},
              { name: 'Vegetable & Fruit Garden (multiple nested crops)', leaves: [
                 { name: 'all possible fruit/vegie options', leaves: [
                    { name: 'species' }
                 ]}
              ]},
              { name: 'Ornamental Garden (single crop)', leaves: [
                 { name: 'all possible ornamental options', leaves: [
                    { name: 'ornamental plants specific species names' }
                 ]}
              ]},

           ]}
        ]
     },


  ],
  levelOne: ['Plant', 'Structure/Equiptment/Other'],
  levelTwo: ['*'],
  levelThree: ['*'],
  levelFour: ['*'],
  levelFive: ['*'],
  selectedOptionOne: 'default',
  selectedOptionTwo: '(must specify level one)',
  selectedOptionThree: '(must specify level two)',
  selectedOptionFour: '(must specify level three)',
  selectedOptionFive: '(must specify level four)',
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
      //console.log(myArr)
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
          return item.name === this.selectedOptionTwo
       })[0].leaves.filter(item => {
          return item.name === selectedOption
       })[0].leaves.map(item => {
          return item.name
       })

       this.set('selectedOptionThree', selectedOption)
       this.set('levelFour', levFour)
    },
    updateLevelFive(selectedOption) {
       let levFive = this.Hierarchy.filter(item => {
          return item.name === this.selectedOptionOne
       }).map(item => {
          return item.leaves
       })[0].filter(item => {
          return item.name === this.selectedOptionTwo
       })[0].leaves.filter(item => {
          return item.name === this.selectedOptionThree
       })[0].leaves.filter(item => {
          return item.name === selectedOption
       })[0].leaves.map(item => {
          return item.name
       })

       this.set('levelFive', levFive)
       this.set('selectedOptionFour', selectedOption)
    },
    setLevelFiveSelection(selectedOption) {
       this.set('selectedOptionFive', selectedOption)
    },
    getPolygonType() {
       const polygonTypeArray = []
       polygonTypeArray.push(this.selectedOptionOne)
       polygonTypeArray.push(this.selectedOptionTwo)
       polygonTypeArray.push(this.selectedOptionThree)
       polygonTypeArray.push(this.selectedOptionFour)
       polygonTypeArray.push(this.selectedOptionFive)
       return polygonTypeArray
    }
  }
});
