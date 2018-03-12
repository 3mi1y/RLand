import { module, test } from 'qunit';
import { setupTest } from 'ember-qunit';

module('transform:poly-type', 'Unit | Transform | poly type', function(hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test('it exists', function(assert) {
    let transform = this.owner.lookup('transform:poly-type');
    assert.ok(transform);
  });
});
