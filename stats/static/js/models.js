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
        dataUrl: '/api/v1/metric_data/',
        bucketUrl: '/api/v1/metric_data/buckets/',
        initialize: function () {
            // update things every minute
            this.timer = setInterval(function () {
                this.getLatest();
                this.getData();
            }.bind(this), 60*1000);

        },
        defaults: {
            aggregations: [],
            annotations: [],
            buckets: [],
            latest: null,
            width: 180,
            domain: 86400,
            offset: 0,
            units: null
        },
        getLatest: function (options, cb, context) {
            var data = {    
                order_by: '-timestamp',
                limit: 1,
                metric: this.get('metric')
            }

            return $.ajax({
                url: this.dataUrl,
                dataType: 'json',
                type: 'GET',
                data: data,
                context: this,
                success: function (data, statux, xhr) {
                    if (data.objects && data.objects.length == 1) {
                        this.set({latest: data.objects[0]});
                        if (_.isFunction(cb)) {
                            cb.call(context);
                        }
                    }
                }
            });
        },
        getData: function (options, cb, context) {
            var data, from, to;
            if (options && options.from) {
                from = options.from;
            } else {
                from = new Date();
                from.setSeconds(from.getSeconds() - this.get('domain'));
            }
            if (options && options.to) {
                to =options.to;
            } else {
                to = new Date();
                to.setSeconds(to.getSeconds() - this.get('offset'));
            }
            data = {
                from: from.toISOString(),
                to: to.toISOString(),
                width: this.get('width'),
                aggregations: JSON.stringify(this.get('aggregations')),
                annotations: JSON.stringify(this.get('annotations')),
                metric: this.get('metric')
            };

            return $.ajax({
                url: this.bucketUrl,
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