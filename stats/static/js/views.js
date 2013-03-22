/*global Backbone, _, Rickshaw, window, $*/
/*nomen=false*/
(function () {
    'use strict';
    this.views.Instrument = Backbone.View.extend({
        className: "widget span6 instrument",
        initialize: function () {
            this.listenTo(this.model, 'change:buckets', this.set_data, this);
            this.listenTo(this.model, 'change:latest', this.set_latest, this);
            this.template = _.template($('#instrument_template').html());
        },
        set_latest: function () {
            var value = this.model.get('latest').value;
            this.$('.latest').text(Humanize.intcomma(value) + ' ' + this.model.get('units'));
        },
        map_data: function () {
            var buckets = this.model.get('buckets');
            return _.map(buckets, function (bucket) {
                var x, y;
                x = new Date(bucket.timestamp).getTime();
                y = {};
                _.each(bucket, function (value, key) {
                    if (key !== 'timestamp') {
                        y[key] = value;
                    }
                });
                return {
                    x: x,
                    y: y
                };
            }.bind(this));
        },
        set_data: function () {
            var data = this.map_data();
            if (data.length == 0) { return; }
            this.$('.loading').hide();
            this.$('.graph').show();
            this.has_data = true;

            var vis = d3.select(this.el);

            var xMin = _.min(data, function (datum) { return datum.x }).x,
                xMax = _.max(data, function (datum) { return datum.x }).x;

            var yMin, yMax;

            if (this.model.get('stack')) {
                var sums = _.map(data, function (datum) {
                    return _.reduce(datum.y, function (memo, num) { return memo + num; }, 0);
                });
                yMin = _.min(sums);
                yMax = _.max(sums);
            } else {
                var maxes = _.map(data, function (datum) {
                    return _.max(datum.y);
                });
                yMin = _.min(maxes);
                yMax = _.max(maxes);
            }

            var buffer = (yMax - yMin) * 0.1
            yMin = Math.max(0, yMin - buffer);
            yMax += buffer;

            this.x.domain([xMin, xMax]);
            this.y.domain([yMin, yMax]);
            this.x2.domain(this.x.domain());
            this.y2.domain(this.y.domain());

            _.each(this.model.get('readings'), function (reading) {
                vis.selectAll('path[reading="'+reading.name+'"]')
                    .data([data])
                    .attr("clip-path", "url(#clip)")
                    .attr("d", this.detailAreas[reading.name]);
            }.bind(this));

            vis.selectAll('path.miniplot')
                .data([data])
                .attr("clip-path", "url(#clip)")
                .attr("d", this.area2);

            this.yAxis.scale(this.y);
            this.focus.select('.y.axis')
                .call(this.yAxis);

            this.xAxis.scale(this.x);
            this.focus.select('.x.axis')
                .call(this.xAxis);

            this.xAxis2.scale(this.x2);
            this.context.select('.x.axis')
                .call(this.xAxis2);

            this.brush.x(this.x2);
            this.zoomView();
        },
        render: function () {
            this.$el.append(this.template(this.model));

            this.x = d3.time.scale(),
            this.x2 = d3.time.scale(),
            this.y = d3.scale.linear(),
            this.y2 = d3.scale.linear();

            this.xAxis = d3.svg.axis(),
            this.xAxis2 = d3.svg.axis(),
            this.yAxis = d3.svg.axis();

            this.brush = d3.svg.brush()
                .on("brush", this.zoomView.bind(this))
                .on('brushend', this.refineData.bind(this));

            this.detailAreas = {}

            this.svg = d3.select(this.$('.graph')[0]).append("svg")
            this.focus = this.svg.append("g");
            this.context = this.svg.append("g")

            _.each(this.model.get('readings'), function (reading, index) {
                this.detailAreas[reading.name] = d3.svg.area()
                    .interpolate("monotone")
                    .x(function(d) {
                        return this.x(d.x);
                    }.bind(this))
                    .y0(function (d) {
                        if (this.model.get('stack')) {
                            var values = _.first(_.values(d.y), index);
                            var sum = _.reduce(values, function (memo, num) { return memo + num; }, 0);
                            return sum;
                        } else {
                            return 0
                        }
                    })
                    .y1(function(d) {
                        if (this.model.get('stack')) {
                            var values = _.first(_.values(d.y), index + 1);
                            var sum = _.reduce(values, function (memo, num) { return memo + num; }, 0);
                            return this.y(sum);
                        } else {
                            var values = _.values(d.y);
                            return this.y(d.y[reading.name]);
                        }
                    }.bind(this));

                this.focus.append("path")
                    .attr("clip-path", "url(#clip)")
                    .attr('class', 'plot')
                    .attr('reading', reading.name)
                    .attr('style', 'stroke:'+reading.stroke+'; fill:'+reading.fill+';');
            }.bind(this));

            this.area2 = d3.svg.area()
                .interpolate("monotone")
                .x(function(d) {
                    return this.x2(d.x);
                }.bind(this))
                .y1(function(d) {
                    var values = _.values(d.y);
                    return this.y2(_.first(values));
                }.bind(this));


            this.svg.append("defs").append("clipPath")
                .attr("id", "clip")
                .append("rect");

            this.focus.append("g")
                .attr("class", "x axis")
            this.focus.append("g")
                .attr("class", "y axis")
                .call(this.yAxis);
            this.context.append("path")
                .attr('class', 'miniplot');
            this.context.append("g")
                .attr("class", "x axis")
            this.context.append("g")
                .attr("class", "x brush")

            $(window).on('resize', this.resizeChart.bind(this));
            this.resizeChart();
        },
        resizeChart: function () {
            var svg = this.$('svg');
            svg.hide();

            var margin = {top: 10, right: 10, bottom: 80, left: 60},
                margin2 = {top: 210, right: 10, bottom: 20, left: 60},
                width = this.$el.width() - margin.left - margin.right,
                height = 270 - margin.top - margin.bottom,
                height2 = 270 - margin2.top - margin2.bottom;

            this.x.range([0, width]);
            this.x2.range([0, width]);
            this.y.range([height, 0]);
            this.y2.range([height2, 0]);

            this.xAxis.scale(this.x).orient("bottom"),
            this.xAxis2.scale(this.x2).orient("bottom"),
            this.yAxis.scale(this.y).orient("left");

            var svgW = width + margin.left + margin.right,
                svgH = height + margin.top + margin.bottom;

            this.svg
                .attr("width", svgW)
                .attr("height", svgH)
              .select("#clip rect")
                .attr("width", width)
                .attr("height", height);

            this.brush.x(this.x2)
            this.svg.select('.brush')
                .call(this.brush)
                .selectAll("rect")
                .attr("y", -6)
                .attr("height", height2 + 7);

            _.each(this.model.get('readings'), function (reading) {
                this.detailAreas[reading.name]
                    .y0(height);
            }.bind(this));

            this.area2
                .y0(height2);

            this.focus
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
              .select('g')
                .attr("transform", "translate(0," + height + ")")
                .call(this.xAxis);

            if (this.has_data) {
                _.each(this.model.get('readings'), function (reading) {
                    this.focus.select("path[reading='"+reading.name+"']")
                        .attr("d", this.detailAreas[reading.name]);
                }.bind(this));
                this.focus.select(".x.axis").call(this.xAxis);
                this.context.select("path").attr("d", this.area2);
                this.context.select(".x.axis").call(this.xAxis2);
            }

            this.context
                .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")")
              .select('g')
                .attr("transform", "translate(0," + height2 + ")")
                .call(this.xAxis2);

            svg.show();
        },
        zoomView: function () {
            this.x.domain(this.brush.empty() ? this.x2.domain() : this.brush.extent());
            _.each(this.model.get('readings'), function (reading) {
                this.focus.select("path[reading='"+reading.name+"']")
                    .attr("d", this.detailAreas[reading.name]);
            }.bind(this));
            this.focus.select(".x.axis").call(this.xAxis);
        },
        refineData: function() {
            var extent = this.brush.extent(), from, to;
            if (!this.brush.empty()) {
                from = extent[0];
                to = extent[1];
                this.model.getData({
                    from: from,
                    to: to
                })
            }
        }
    });

    this.views.Event = Backbone.View.extend({
        className: 'timeslot',
        icon: function () {
            switch (this.model.get('type')) {
            default:
                return "fa-icon-calendar"
            }
        },
        render: function () {
            this.$el.append(_.template($('#event_template').html(), this.model));
            var icon = this.icon(this);
            this.$('.icon').append('<i class="' + this.icon() + '"></i>');
            if (this.options.alt) {
                this.$el.addClass('alt');
            }
        }
    });
}.call(window.Stats));
