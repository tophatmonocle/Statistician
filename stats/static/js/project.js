$(document).ready(function () {
    var StatsRouter = Backbone.Router.extend({
        routes: {
            "*path": "doSomething"
        },
        doSomething: function (path) {
            $('.main-menu>li').removeClass('active');
            $('.main-menu>li[data-tab='+path+']').addClass('active');
            $('#content>div').hide();
            $('[data-content='+path+']').show();
        }
    });
    window.app = new StatsRouter();
    Backbone.history.start({
        pushState: true,
        root: window.project
    });
    window.instruments = new Stats.collections.Instruments();

    var from = new Date();
    from.setDate(from.getDate() - 5);
    var to = new Date();
    $('#date_range').text(moment(from).format('YYYY/MM/DD') + ' - ' + moment(to).format('YYYY/MM/DD'));

    instruments.fetch({
        data: {project: window.project},
    }).then(function () {
        instruments.each(function (instrument) {
            v = new Stats.views.Instrument({
                model: instrument,
                field: 'max'
            });
            instrument.getData({
                from: from,
                to: to,
            });

            $('#instruments').append(v.el);
            v.render();

        });
    });

    $('.main-menu a').on('click', function (e) {
        e.preventDefault();
        var route = $(e.target).closest('li').attr('data-tab');
        window.app.navigate(route, {trigger: true});
    });
});