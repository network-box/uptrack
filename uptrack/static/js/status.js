var make_popover = function() {
    var pkgid = $(this).attr("data-pkg");
    return $("#popover_content_" + pkgid).html();
}

var make_popovers = function(popover_class) {
    $(popover_class).popover({animation: true, container: "body", html: true,
                              placement: "bottom", title: "Actions",
                              content: make_popover});

    $(popover_class).on("shown.bs.popover", function() {
        $(".popover-content").find("li").each(function() {
            var pkgid = $(this).attr("data-pkgid");
            var action = $(this).attr("data-action");

            if (action === "downstream") {
                $(this).click({pkgid: pkgid}, mark_downstream_clicked);
            } else if (action === "nodownstream") {
                $(this).click({pkgid: pkgid}, unmark_downstream_clicked);
            } else {
                console.log("ERROR: Can't handle '" + action + "' action");
            }
        });
    });
}

var mark_downstream_clicked = function(e) {
    var pkgid = e.data.pkgid;
    var url = "/packages/" + pkgid + "/markdownstream";

    $("#popover_button_" + pkgid).popover("hide");

    $.get(url, {}, function(data) {
        var notif = $("#alert_placeholder");

        if (data.error !== undefined) {
            $(notif).html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span>' + data.error + '</span></div>');
        } else {
            $(notif).html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span>' + data.msg + '</span></div>');
        }
    }, 'json');

    return false;
}

var unmark_downstream_clicked = function(e) {
    var pkgid = e.data.pkgid;
    var url = "/packages/" + pkgid + "/unmarkdownstream";

    $("#popover_button_" + pkgid).popover("hide");

    $.get(url, {}, function(data) {
        var notif = $("#alert_placeholder");

        if (data.error !== undefined) {
            $(notif).html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span>' + data.error + '</span></div>');
        } else {
            $(notif).html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span>' + data.msg + '</span></div>');
        }
    }, 'json');

    return false;
}
