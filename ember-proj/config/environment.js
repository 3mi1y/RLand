'use strict';

module.exports = function(environment) {
  let ENV = {
    modulePrefix: 'ember-proj',
    environment,
    rootURL: '/',
    locationType: 'auto',
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true
      },
      EXTEND_PROTOTYPES: {
        // Prevent Ember Data from overriding Date.parse.
        Date: false
      }
    },

    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
    }
  };

  ENV.contentSecurityPolicy = {
    'default-src': "'none'",
    'script-src': "'self' 'unsafe-eval' *.googleapis.com maps.gstatic.com",
    'font-src': "'self' fonts.gstatic.com",
    'connect-src': "'self' maps.gstatic.com",
    'img-src': "'self' *.googleapis.com maps.gstatic.com csi.gstatic.com",
    'style-src': "'self' 'unsafe-inline fonts.googleapis.com maps.gstatic.com"
  };

  if (environment === 'development') {
    // ENV.GOOGLE_MAPS_API_KEY = "AIzaSyCLY83JWDZ0glsYBfk3mFPY8aD32AzuNdE";
    // ENV.googleMap = {
    //   libraries: ['drawing']
    // }
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true;
  }

  if (environment === 'test') {
    // Testem prefers this...
    ENV.locationType = 'none';

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = '#ember-testing';
    ENV.APP.autoboot = false;
    // ENV.GOOGLE_MAPS_API_KEY = "AIzaSyCLY83JWDZ0glsYBfk3mFPY8aD32AzuNdE";
    // ENV.googleMap = {
    //   libraries: ['drawing']
    // }
  }

  if (environment === 'production') {
    // ENV.GOOGLE_MAPS_API_KEY = "AIzaSyCLY83JWDZ0glsYBfk3mFPY8aD32AzuNdE";
    // ENV.googleMap = {
    //   libraries: ['drawing']
    // }
    // here you can enable a production-specific feature
  }

  return ENV;
};
