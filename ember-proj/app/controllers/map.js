import Controller from '@ember/controller';
import DS from "ember-data";

export default Controller.extend({
  Hierarchy: 
[{"name": "Structure/Equipment/Other", "leaves": [{"name": "Structure", "leaves": [{"name": "House", "leaves": []}, {"name": "Barn", "leaves": []}, {"name": "Garage", "leaves": []}, {"name": "Shed/Storage/Outbuilding", "leaves": []}, {"name": "Warehouse", "leaves": []}, {"name": "Fence", "leaves": [{"name": "Wood Fence", "leaves": []}, {"name": "Barbed Wire Fence", "leaves": []}, {"name": "Chain-link Fence", "leaves": []}]}, {"name": "Firewood Storage", "leaves": []}, {"name": "Other Structure", "leaves": []}]}, {"name": "Equipment", "leaves": [{"name": "Vehicle", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Tractor", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Farm Equipment", "leaves": []}, {"name": "Pipe/Irrigation", "leaves": []}, {"name": "Other Equipment", "leaves": []}]}, {"name": "Other Category", "leaves": []}]}, {"name": "Plant", "leaves": [{"name": "Beds (raised beds)", "leaves": [{"name": "Vegetable & Fruit Garden", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Ornamental Garden", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Cover Crop and/or Pollinator Habitat", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Other Crops", "leaves": [{"name": "Weeds", "leaves": []}, {"name": "Fallow", "leaves": []}, {"name": "Other Other Crops", "leaves": []}]}]}, {"name": "Garden Patch/Area (NOT raised beds)", "leaves": [{"name": "Vegetable & Fruit Garden", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Ornamental Garden", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Cover Crop and/or Pollinator Habitat", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Other Crops", "leaves": [{"name": "Weeds", "leaves": []}, {"name": "Fallow", "leaves": []}, {"name": "Other Other Crops", "leaves": []}]}]}, {"name": "Tunnels/Hoops", "leaves": [{"name": "Vegetable & Fruit Garden", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Ornamental Garden", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Cover Crop and/or Pollinator Habitat", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Other Crops", "leaves": [{"name": "Weeds", "leaves": []}, {"name": "Fallow", "leaves": []}, {"name": "Other Other Crops", "leaves": []}]}]}, {"name": "Greenhouse", "leaves": [{"name": "Vegetable & Fruit Garden", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Ornamental Garden", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Cover Crop and/or Pollinator Habitat", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Other Crops", "leaves": [{"name": "Weeds", "leaves": []}, {"name": "Fallow", "leaves": []}, {"name": "Other Other Crops", "leaves": []}]}]}, {"name": "Hydroponics", "leaves": [{"name": "Vegetable & Fruit Garden", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Ornamental Garden", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Cover Crop and/or Pollinator Habitat", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Other Crops", "leaves": [{"name": "Weeds", "leaves": []}, {"name": "Fallow", "leaves": []}, {"name": "Other Other Crops", "leaves": []}]}]}, {"name": "Row Crops", "leaves": [{"name": "Vegetable & Fruit Garden", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Ornamental Garden", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Cover Crop and/or Pollinator Habitat", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Other Crops", "leaves": [{"name": "Weeds", "leaves": []}, {"name": "Fallow", "leaves": []}, {"name": "Other Other Crops", "leaves": []}]}]}, {"name": "Major Mono-Crops Field", "leaves": []}, {"name": "Open area (Lawn/Meadow/Field)", "leaves": [{"name": "Lawn", "leaves": [{"name": "Native Grass", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Non-native Grass", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Mixed native and non-native", "leaves": []}, {"name": "Weeds", "leaves": []}, {"name": "Fallow (not in use; inactive)", "leaves": []}, {"name": "Other Lawn/Meadow/Field", "leaves": []}]}, {"name": "Meadow", "leaves": [{"name": "Native Grass", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Non-native Grass", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Mixed native and non-native Grasses", "leaves": []}, {"name": "Flowers", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Mixed Grasses and flowers", "leaves": []}, {"name": "Weeds", "leaves": []}, {"name": "Fallow (not in use; inactive)", "leaves": []}, {"name": "Other Lawn/Meadow/Field", "leaves": []}]}, {"name": "Field", "leaves": [{"name": "Native Grass", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Non-native Grass", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Mixed native and non-native", "leaves": []}, {"name": "Flowers", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Mixed Grasses and flowers", "leaves": []}, {"name": "Weeds", "leaves": []}, {"name": "Fallow (not in use; inactive)", "leaves": []}, {"name": "Other Lawn/Meadow/Field", "leaves": []}]}]}, {"name": "Forest/Woods", "leaves": [{"name": "Mixed Conifer/Deciduous", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Mixed Conifers", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Mixed Deciduous", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Single Species Conifers", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Single Species Deciduous", "leaves": [{"name": "...", "leaves": []}]}]}, {"name": "Individual Tree", "leaves": [{"name": "Fruit Tree", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Nut Tree", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Other Deciduous Trees", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Other Conifers", "leaves": [{"name": "...", "leaves": []}]}]}, {"name": "Orchard", "leaves": [{"name": "Mono Fruit Orchard", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Mono Nut Orchard", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Mixed Fruit Orchard", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Mixed Nut Orchard", "leaves": [{"name": "...", "leaves": []}]}]}]}, {"name": "Animal", "leaves": [{"name": "Poultry/Egg layers", "leaves": [{"name": "Chickens", "leaves": [{"name": "Egg Laying Chicken Hens", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Meat Chickens", "leaves": [{"name": "...", "leaves": []}]}]}, {"name": "Turkeys", "leaves": []}, {"name": "Pheasants", "leaves": []}, {"name": "Quail", "leaves": []}, {"name": "Other Poultry", "leaves": []}]}, {"name": "Individual Bee Hive", "leaves": [{"name": "Single Honey Bee Hive", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Single Pollinatory Hive", "leaves": [{"name": "...", "leaves": []}]}]}, {"name": "Apiary", "leaves": [{"name": "Honey Bee Hives", "leaves": [{"name": "...", "leaves": []}]}, {"name": "Pollinator Bee Hives", "leaves": [{"name": "...", "leaves": []}]}]}, {"name": "Cattle/Beef", "leaves": []}, {"name": "Dairy", "leaves": []}, {"name": "Hogs/Pork", "leaves": []}, {"name": "Sheep/Lamb/Mutton", "leaves": []}, {"name": "Aquaculture(fish)", "leaves": []}, {"name": "Horses", "leaves": []}, {"name": "Grazing/Pasture", "leaves": []}, {"name": "Feed", "leaves": []}, {"name": "Feed lot", "leaves": []}]}, {"name": "Water", "leaves": [{"name": "Well/Pump", "leaves": [{"name": "Well", "leaves": []}, {"name": "Well with pump", "leaves": []}, {"name": "Well - artesian (under pressure)", "leaves": []}]}, {"name": "Pond/Lake", "leaves": []}, {"name": "Stream/River", "leaves": []}, {"name": "Riparian Area", "leaves": []}, {"name": "Water transport", "leaves": [{"name": "Pipe line", "leaves": []}, {"name": "Irrigation", "leaves": [{"name": "Spray", "leaves": []}, {"name": "Drip", "leaves": []}]}, {"name": "Ditches", "leaves": [{"name": "Feeder Ditch", "leaves": []}, {"name": "Drainage Ditch", "leaves": []}, {"name": "Diversion Ditch", "leaves": []}, {"name": "Protection Ditch", "leaves": []}]}, {"name": "Aqueduct", "leaves": []}, {"name": "Siphons", "leaves": []}, {"name": "Canals", "leaves": [{"name": "Feeder Canals", "leaves": []}, {"name": "Drainage Canals", "leaves": []}, {"name": "Diversion Canals", "leaves": []}, {"name": "Protection Canals", "leaves": []}]}]}]}],
  levelOne: ['Structure/Equipment/Other', 'Plant', 'Animal', 'Water'],
  levelTwo: ['*'],
  levelThree: ['*'],
  levelFour: ['*'],
  levelFive: ['*'],
  selectedOptionOne: 'default',
  selectedOptionTwo: '(must specify level one)',
  selectedOptionThree: '(must specify level two)',
  selectedOptionFour: '(must specify level three)',
  selectedOptionFive: '(must specify level four)',

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
        polygon.set('location', this.get("location"));
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
        this.set('levelTwo', myArr);
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
        this.set('levelThree', levThree);
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
        this.set('levelFour', levFour);
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

        this.set('levelFive', levFive);
        this.set('selectedOptionFour', selectedOption);
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
        //console.log(polygonTypeArray)
        return polygonTypeArray
      },

      deletePolygon(polygon) {
        this.store.findRecord('polygon', polygon.get('id')).then((post) => {
          post.destroyRecord();
        })
      }
    }
});
