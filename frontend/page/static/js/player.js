var TV23 = {
    kdp: null
};

function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) == variable) {
            return decodeURIComponent(pair[1]);
        }
    }
    return null;
}

$(function () {
    "use strict";
    kWidget.addReadyCallback(function (playerId) {

        TV23.kdp = document.getElementById(playerId);

        // Jump to start location:
        var start = getQueryVariable('start');
        if (start && /^\d+$/.test(start)) {
            TV23.kdp.kBind('playerUpdatePlayhead.start', function () {
                TV23.kdp.sendNotification('doSeek', start);
                TV23.kdp.kUnbind('.start')
            });
        }
    });


    //function HHMMSStoSeconds(HH, MM, SS) {
    //    return HH * 3600 + MM * 60 + SS;
    //}

    function hmmss(seconds) {
        var ss = seconds % 60;
        ss = "" + (ss < 10 ? "0" : "") + ss;
        if (seconds / 3600 < 1) {
            return "" + Math.floor(seconds / 60) + ":" + ss;
        }
        var mm = Math.floor(seconds / 60);
        mm = "" + (mm < 10 ? "0" : "") + mm;
        return "" + Math.floor(seconds / 3600) + ":" + mm + ":" + ss;
    }

    var interval;

    $("#add-snippet").click(function () {
        $("#add-snippet").hide();
        $("#mark-snippet").show();
        interval = setInterval(function () {
            updateMarker($("#start"));
        }, 100);
    });

    $("#save-start").click(function () {
        clearInterval(interval);
        var currentTime = TV23.kdp.evaluate("{video.player.currentTime}");
        $("#start").val(currentTime.toFixed(0));
        $("#save-start").hide();
        interval = setInterval(function () {
            updateMarker($("#end"));
        }, 100);
        $("#timer_end_span").show();
        return false;
    });

    $("#save-end").click(function () {
        clearInterval(interval);
        var currentTime = TV23.kdp.evaluate("{video.player.currentTime}");
        $("#start").hide();
        $("#timer_end_span").hide();
        $("#snipEd_start_display")[0].innerHTML = $("#start span").text();
        $("#snipEd_end_display")[0].innerHTML = $("#end span").text();
        $("#snippet_editor").show();
        return false;
    });

    $("#snipEd_save").click(function () {
        $("#snippet_editor").hide();
        $("#start").val(0);
        $("#start").show();
        $("#id_start_time").val($("#start input").val());
        $("#id_end_time").val($("#end input").val());
        $("#save-start").show();
    });


    $('#snippet-form').ajaxForm({
        beforeSerialize: function () {
            var tags = $("#id_tags_select").val();
            $("#id_tags").val(tags ? tags.join(",") : '');
        },
        clearForm: true,
        success: function (data) {
            $("#snippets").append(data);
            $("#snippet-form").get(0).reset();
            $("#id_tags_select").val(null).trigger('change');
            $("#add-snippet").show();
            $("#mark-snippet").hide();
            $("#snippet_editor").hide();
        }
    });

    function updateMarker(el) {
        var currentTime = TV23.kdp.evaluate("{video.player.currentTime}");
        var v = currentTime.toFixed(0);
        el.find("input").val(v);
        el.find("span").text(hmmss(v));
    }


    $("body").on("click", ".jumpTo", function () {
        TV23.kdp.sendNotification("doSeek", $(this).data("start"));
    });

    $("body").on("mouseover", ".moving-thumb", function () {
        var el = $(this);
        var original = el.css('background-position');
        var start = parseInt(original);
        var end = parseInt(el.data('end-offset'));
        var x = start;

        var h = setInterval(function () {
            x -= 100;
            if (x <= end) {
                // restart loop...
                x = start;
            }
            el.css('background-position', x + 'px');
        }, 300);
        el.one('mouseout', function () {
            clearInterval(h);
            el.css('background-position', start);
        })
    });

    var tags_url = $("#id_tags_select").data('tags-url');
    $.get(tags_url, function (data) {
        $("#id_tags_select").select2({
            dir: 'rtl',
            language: "he",
            tags: true,
            data: data,
            tokenSeparators: [',']
        });
    });


});