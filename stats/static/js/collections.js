/*global Backbone, window, _, $*/
(function () {
    "use strict";

    this.collections.Metrics = Backbone.Collection.extend({
        urlRoot: '/api/v1/metrics/',
        model: this.models.Metric
    });

    this.collections.Instruments = Backbone.Collection.extend({
        urlRoot: '/api/v1/instruments/',
        model: this.models.Instrument
    });

    this.collections.Events = Backbone.Collection.extend({
        urlRoot: '/api/v1/events/',
        model: this.models.Event
    });
}.call(window.Stats));