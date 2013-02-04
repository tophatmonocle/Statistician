/*global Backbone, _, Rickshaw, window, $*/
/*nomen=false*/
(function () {
    'use strict';
    this.views.Bucket = Backbone.View.extend({
        default_transform: {
            x: function (x) { return x; },
            y: function (y) { return y; }
        },
        initialize: function () {
            this.options.filters = _.extend({}, this.options.filters);
            this.options.transform = _.extend(_.clone(this.default_transform), this.options.transform);
            this.listenTo(this.model, 'change:data', this.render, this);
            this.mapped_data = [];
        },
        map_data: function () {
            return {
                data: _.map(this.model.get('data').buckets, function (bucket, timestamp) {
                    var x, y;
                    x = new Date(timestamp).getTime() / 1000;
                    y = bucket[this.options.field];
                    return {
                        x: this.options.transform.x(x),
                        y: this.options.transform.y(y)
                    };
                }, this),
                color: '#c05020',
                name: this.options.name
            };
        },
        render: function () {
            this.$el.html('');
            if (this.model.get('data') === null) {
                this.render_loading();
            } else {
                this.render_data();
            }
        },
        render_loading: function () {
            this.$el.css({width: this.options.width, height: this.options.height});
            this.$el.addClass('loading_graph');
        },
        build_graph: function () {
            var y_ticks, hoverDetail, xAxis, yAxis, data, max;
            if (this.graph) {
                delete this.graph;
            }
            data = this.map_data();
            max = _.max(data.data, function (datum) { return datum.y });
            this.graph = new Rickshaw.Graph({
                element: this.el,
                renderer: 'area',
                stroke: true,
                strokeWidth: 1,
                height: this.options.height,
                width: this.options.width,
                interpolation: 'linear',
                series: [data],
                max: max.y * 1.2
            });

            xAxis = new Rickshaw.Graph.Axis.Time({
                graph: this.graph
            });

            xAxis.render();

            yAxis = new Rickshaw.Graph.Axis.Y({
                graph: this.graph,
                tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
                pixelsPerTick: 30
            });

            yAxis.render();

            hoverDetail = new Rickshaw.Graph.HoverDetail({
                graph: this.graph,
                formatter: function (series, x, y) {
                    var date = '<span class="date">' + new Date(x * 1000).toUTCString() + '</span>',
                        swatch = '<span class="detail_swatch" style="background-color: ' + series.color + '"></span>',
                        content = swatch + series.name + ': ' + parseInt(y, 10) + '<br>' + date;
                    return content;
                }
            });
        },
        render_data: function () {
            this.$el.removeClass('loading_graph');
            this.build_graph();
            this.graph.render();
        }
    });

    this.views.PeriodPicker = Backbone.View.extend({
        className: 'period_picker d',
        events: {
            'click a': 'select'
        },
        select: function (e) {
            var period, from, to, width;

            period = e.target.className;
            this.$el.removeClass().addClass('period_picker').addClass(period);
            e.preventDefault();

            to = new Date();
            from = new Date();
            switch (period) {
            case 'h':
                from.setHours(to.getHours() - 1);
                break;
            case 'd':
                from.setDate(to.getDate() - 1);
                break;
            case 'w':
                from.setDate(to.getDate() - 7);
                break;
            }
            width = Math.floor((to - from) / 24 / 1000);
            this.model.update({
                from: from,
                to: to,
                width: width,
                data: null
            });
        },
        render: function () {
            this.$el.addClass(this.options.selected);
            this.$el.html($('#period-picker').html());
        }
    });

    this.views.ExceptionSummary = Backbone.View.extend({
        className: 'exceptionSummary',
        tagName: 'li',
        render: function () {
            this.$el.html(_.template($('#exception-summary').html(), this.model.attributes));
        }
    });

    this.views.GraphFilter = Backbone.View.extend({
        tagName: 'form',
        className: 'form-inline',
        events: {
            'submit': 'submit'
        },
        submit: function (e) {
            var url, from, to;
            url = this.$('input[name="url"]').val();
            from = new Date();
            to = new Date();
            from.setHours(to.getHours() - 1);
            this.model.set({
                from: from,
                to: to,
                filters: {
                    url: url
                }
            });
            this.model.fetch();
            e.preventDefault();
            return false;
        },
        render: function () {
            this.$el.html(($('#graph-filter').html()))
        }
    });
}.call(window.Statistician));
