import Ember from 'ember';

export default Ember.Route.extend({
  model(){
    return $.get('/server/give_me_time');
  }
});
