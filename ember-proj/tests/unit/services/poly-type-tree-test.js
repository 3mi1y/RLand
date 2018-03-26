import { module, test } from 'qunit';
import { setupTest } from 'ember-qunit';

module('Unit | Service | poly-type-tree', function(hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test('it exists', function(assert) {
    let service = this.owner.lookup('service:poly-type-tree');
    assert.ok(service);
  });
});

