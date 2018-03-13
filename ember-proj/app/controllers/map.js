import Controller from '@ember/controller';

export default Controller.extend({
  // todo: modify: when active causes transaction is null error, need to modify for our polygons
  // actions:
  //   {
  //     polygonSelected(polygon)
  //     {
  //       if (!polygon)
  //         return;
  //
  //       let model = polygon.get('model');
  //       if (!model)
  //       {
  //         model = this.get('store').createRecord('polygon', {
  //           category: '',
  //           subcategory: ''
  //         });
  //         model.save();
  //         polygon.set('model', model);
  //       }
  //
  //       this.set('selected', model);
  //     },

      // filterByYear(year)
      // {
      //   if (year == undefined)
      //     return this.get('store').findAll('polygon');
      //   else
      //     return this.get('store').query('polygon', { year: year });
      // }
    // }
});
