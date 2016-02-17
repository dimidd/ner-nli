$(function () {
    "use strict";

    $('a[data-entity]').hover(function () {
        var e = $(this);
        e.off('hover');
        $.get(e.attr('href') + 'tooltip/', function (html) {
            e.tooltip({title: html, html:'true', placement: 'bottom'}).tooltip('show');
        });
    });
});
