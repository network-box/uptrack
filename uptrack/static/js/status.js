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
                $(this).click({pkgid: pkgid, value: true},
                              mark_downstream_clicked);
            } else if (action === "nodownstream") {
                $(this).click({pkgid: pkgid, value: false},
                              mark_downstream_clicked);
            } else if (action === "renamed") {
                var pkgname = $(this).attr("data-pkgname");
                var upstream_pkgname = $(this).attr("data-upstream-pkgname");

                $(this).click({pkgid: pkgid, pkgname: pkgname,
                               upstream_pkgname: upstream_pkgname},
                              mark_renamed_clicked);
            } else {
                console.log("ERROR: Can't handle '" + action + "' action");
            }
        });
    });
}

var mark_downstream_clicked = function(e) {
    var pkgid = e.data.pkgid;
    var value = e.data.value;

    var url = "/packages/" + pkgid + "/markdownstream";

    $("#popover_button_" + pkgid).popover("hide");

    $.get(url, $.param({value: value}), function(data) {
        var notif = $("#alert_placeholder");

        if (data.error !== undefined) {
            var msg = data.error;
            var level = "error";
        } else {
            var msg = data.msg;
            var level = "success";
        }

        notify(msg, level);
    }, 'json');

    return false;
}

var mark_renamed_clicked = function(e) {
    var pkgid = e.data.pkgid;
    var pkgname = e.data.pkgname;
    var upstream_pkgname = e.data.upstream_pkgname;

    if (upstream_pkgname === undefined) {
        upstream_pkgname = "";
    }

    $("#popover_button_" + pkgid).popover("hide");

    $("#uptrack_rename_package_modal").modal({backdrop: true, keyboard: true,
                                              show: true});

    $("#uptrack_rename_package_modal").on("shown.bs.modal", function() {
        $("#uptrack_rename_package_upstream_pkgname").val(upstream_pkgname);
        $("#uptrack_rename_package_current_name").text(pkgname);

        $("#uptrack_rename_package_submit").off("click");
        $("#uptrack_rename_package_submit").click(function() {
            var url = "/packages/" + pkgid + "/markrenamed";

            var upstream_pkgname = $("#uptrack_rename_package_upstream_pkgname").val();
            var options = {upstream_pkgname: upstream_pkgname};

            $.get(url, $.param(options), function(data) {
                $("#uptrack_rename_package_modal").modal("hide");

                if (data.error !== undefined) {
                    var msg = data.error;
                    var level = "error";
                } else {
                    var msg = data.msg;
                    var level = "success";
                }

                notify(msg, level);
            }, 'json');
        });
    });

    return false;
}
