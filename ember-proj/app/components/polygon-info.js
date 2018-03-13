import Ember from 'ember';

export default Ember.Component.extend({
  classNames: ['polygon-info', 'z-depth-1', 'row'],

  selected: null,

  categories: Ember.computed('content.[]', function () {
    return [
      'Structure',
      'Plant',
      'Animal',
      'Equipment',
      'Water',
      'Other'
    ];
  }),

  subcategories: Ember.computed('content.[]', 'selected.category', function () {
    let subcategories = {
      'Structure': [
        'House', 'Garage', 'Shed/Storage/Outbuilding', 'Greenhouse', 'Warehouse', 'Fence'
      ],
      'Plant': [
        'Field', 'Bed', 'Tunnels/Hoops', 'Greenhouse', 'Hydroponics', 'Major Crops', 'Vegetable/Fruit Garden', 'Fruit/Nut Trees', 'Tree', 'Lawn', 'Forest', 'Ornamental Garden', 'Timber'
      ],
      'Animal': [
        'Cattle/Beef', 'Dairy', 'Hogs/Pork', 'Poultry/Eggs', 'Sheep, Lamb, Mutton', 'Aquaculture(fish)', 'Apiary', 'Horses'
      ],
      'Equipment': [
        'Vehicle', 'Tractor', 'Pipe/irragation line'
      ],
      'Water': [
        'Well/pump', 'pond/lake', 'Stream/River', 'Pipe/irrigation line'
      ],
      'Other': [],
    };

    let selected = this.get('selected');
    if (!selected)
      return null;

    return subcategories[this.get('selected').get('category')];
  }),

  didRender() {
    this._super(...arguments);
    this.$('.md-select select').material_select(); // Needed for force md-select to update
    this.$('.datepicker').pickadate();
  }

});
