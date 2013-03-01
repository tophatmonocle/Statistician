/*global Backbone, window, _, $*/
(function () {
    "use strict";
    this.models.Metric = Backbone.Model.extend({
        urlRoot: '/api/v1/metrics/',
    });

    this.models.Event = Backbone.Model.extend({
        urlRoot: '/api/v1/events/',
    });

    this.models.Instrument = Backbone.Model.extend({
        urlRoot: '/api/v1/instruments/',
        defaults: {
            aggregations: [],
            annotations: [],
            buckets: [],
        },
        getData: function (options, cb, context) {
            var url, data;
            url = '/api/v1/metric_data/buckets/';
            data = {
                from: options.from.toISOString(),
                to: options.to.toISOString(),
                width: options.width,
                aggregations: JSON.stringify(this.get('aggregations')),
                annotations: JSON.stringify(this.get('annotations')),
                metric: this.get('metric')
            };

            return $.ajax({
                url: url,
                dataType: 'json',
                type: 'GET',
                data: data,
                context: this,
                success: function (data, statux, xhr) {
                    this.merge(data.buckets);
                    if (_.isFunction(cb)) {
                        cb.call(context);
                    }
                }
            });
        },
        merge: function (new_buckets) {
            if (new_buckets.length == 0) { return; }
            var buckets = this.get('buckets');
            var from = new_buckets[0].timestamp;
            var to = new_buckets[new_buckets.length-1].timestamp;
            var old = buckets.length;
            // remove all the data that's overridden by this merge
            buckets = _.filter(buckets, function (bucket) {
                return bucket.timestamp < from || bucket.timestamp > to;
            });

            buckets.push.apply(buckets, new_buckets);
            var sorted_buckets = _.sortBy(buckets, function (bucket) {
                return bucket.timestamp;
            });
            this.set({buckets: sorted_buckets});
            this.trigger('change:buckets');
        }
    });
}.call(window.Stats));