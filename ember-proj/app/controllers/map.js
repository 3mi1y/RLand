import Controller from '@ember/controller';
import { inject } from '@ember/service';
import $ from 'jquery';

export default Controller.extend({
  polyTypeTree: inject(),
  Hierarchy: [],
  levelOne: ['*'],
  levelTwo: ['*'],
  levelThree: ['*'],
  levelFour: ['*'],
  levelFive: ['*'],
  showLevelTwo: false,
  showLevelThree: false,
  showLevelFour: false,
  showLevelFive: false,
  selectedOptionOne: 'default',
  selectedOptionTwo: '(must specify level one)',
  selectedOptionThree: '(must specify level two)',
  selectedOptionFour: '(must specify level three)',
  selectedOptionFive: '(must specify level four)',

  init() {
    this._super(...arguments);
    this.get('polyTypeTree').get_tree().then(tree => {
      this.set('Hierarchy', tree);
      this.set('levelOne', tree.map(x => x.name));
    });
  },

  // todo: modify: when active causes transaction is null error, need to modify for our polygons
  actions:
    {
      polygonSelected(polygon)
      {
        if (!polygon)
          return;

        let model = polygon.get('model');
        if (!model)
        {
          model = this.get('store').createRecord('polygon', {
            name: '',
            polytype: '',
            location: '',
            category: '',
            subcategory: '',
            tasks: [],
            startDate: '',
            endDate: '',
          });
          model.save();
          polygon.set('model', model);
        }
        this.set('selected', model);
      },

      filterByYear(year)
      {
        if (year == undefined)
          return this.get('store').findAll('polygon');
        else
          return this.get('store').query('polygon', { year: year });
      },

      createPolygon() {
        let polygon = this.get('selected');
        polygon.set('name', this.get("name"));
        polygon.set('polyType', this.actions.getPolygonType.call(this));
        polygon.set('startDate', this.get("startDate"));
        polygon.set('endDate', this.get("endDate"));
        polygon.save();
        $('.new-poly').hide();
        $('.poly-list').show();
      },

      updateLevelTwo(selectedOption) {
        let myArr = this.Hierarchy.filter(item => {
          return item.name === selectedOption
        }).map(item => {
          return item.leaves
        })[0].map(item => {
          return item.name
        });
        //console.log(myArr)
        this.set('selectedOptionOne', selectedOption);
	this.set('selectedOptionTwo', '');
	this.set('selectedOptionThree', '');
	this.set('selectedOptionFour', '');
	this.set('selectedOptionFive', '');
        this.set('levelTwo', myArr);
	this.set('showLevelTwo', true);
	this.set('showLevelThree', false);
	this.set('showLevelFour', false);
	this.set('showLevelFive', false);
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
        });
	this.set('selectedOptionTwo', selectedOption);
	this.set('selectedOptionThree', '');
	this.set('selectedOptionFour', '');
	this.set('selectedOptionFive', '');
        this.set('levelThree', levThree);
	this.set('showLevelThree', true);
	this.set('showLevelFour', false);
	this.set('showLevelFive', false);
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
        });

	this.set('selectedOptionThree', selectedOption);
	this.set('selectedOptionFour', '');
	this.set('selectedOptionFive', '');
        this.set('levelFour', levFour);
	this.set('showLevelFour', true);
	this.set('showLevelFive', false);
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
        });

	this.set('selectedOptionFour', selectedOption);
	this.set('selectedOptionFive', '');
        this.set('levelFive', levFive);
	this.set('showLevelFive', true);
      },

      setLevelFiveSelection(selectedOption) {
        this.set('selectedOptionFive', selectedOption)
      },

      getPolygonType() {
        const polygonTypeArray = [];
        polygonTypeArray.push(this.get('selectedOptionOne'));
        polygonTypeArray.push(this.get('selectedOptionTwo'));
        polygonTypeArray.push(this.get('selectedOptionThree'));
        polygonTypeArray.push(this.get('selectedOptionFour'));
        polygonTypeArray.push(this.get('selectedOptionFive'));
        return polygonTypeArray
      },

      deletePolygon(polygon) {
        this.get('store').findRecord('polygon', polygon.get('id'), {backgroundReload: false}).then((polygon) => {
          polygon.destroyRecord();
        })
      }
    }
});
