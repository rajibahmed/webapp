import Ember from 'ember';

export default Ember.Controller.extend({

  /*
  * 1) First step you need to do is inject the websocket service into your object. You
  * can inject the service into component, controllers, object, mixins, routes, and views.
  */
  socketService: Ember.inject.service('websockets'),

  init: function() {
    this._super.apply(this, arguments);

    /*
    * 2) The next step you need to do is to create your actual websocket. Calling socketFor
    * will retrieve a cached websocket if one exists or in this case it
    * will create a new one for us.
    */
    var socket = this.get('socketService').socketFor('ws://localhost:7000/');

    /*
    * 3) The final step is to define your event handlers. All event handlers
    * are added via the `on` method and take 3 arguments: event name, callback
    * function, and the context in which to invoke the callback. All 3 arguments
    * are required.
    */
    socket.on('open', this.myOpenHandler, this);
    socket.on('message', this.myMessageHandler, this);
    socket.on('close', function(event) {
      // anonymous functions work as well
    }, this);
  },

  myOpenHandler: function(event) {
    console.log('On open event has been called: ' + event);
  },

  myMessageHandler: function(event) {
    console.log('Message: ' + event.data);
  },

  actions: {
    sendButtonPressed: function() {
      /*
      * If you need to retrieve your websocket from another function or method you can simply
      * get the cached version at no penalty
      */
      var socket = this.get('socketService').socketFor('ws://localhost:7000/');
      socket.send('Hello Websocket World');
    }
  }
});
