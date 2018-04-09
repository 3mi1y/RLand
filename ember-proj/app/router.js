import EmberRouter from '@ember/routing/router';
import config from './config/environment';

const Router = EmberRouter.extend({
  location: config.locationType,
  rootURL: config.rootURL
});

Router.map(function() {
  this.route('map');
  this.route('profile');
  this.route('login');
  this.route('task', { path: '/task/:task_id' });
  this.route('dashboard');
  this.route('polygon-list');
  this.route('new-polygon');
  this.route('edit-polygon', { path: '/edit-polygon/:polygon_id' });
  this.route('polygon-info', { path: '/polygon-info/:polygon_id' });
  this.route('register');
  this.route('social');
  this.route('charts');
  this.route('new-task', { path: '/new-task/:polygon_id' });
  this.route('new-harvest', { path: '/new-harvest/:polygon_id' });
  this.route('new-note', { path: '/new-note/:polygon_id' });
  this.route('all-tasks');
  this.route('notes', { path: '/notes/:polygon_id' });
  this.route('harvests', { path: '/harvests/:polygon_id' });
  this.route('tasks', { path: '/tasks/:polygon_id' });
  this.route('task-info', { path: '/task-info/:task_id '});
});

export default Router;
