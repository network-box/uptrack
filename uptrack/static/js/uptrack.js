var equalize_column_heights = function(row_selector, column_selector) {
    $(row_selector).each(function(index, row) {
        tallest_height = 0;

        $(row).find(column_selector).each(function(index, block) {
            current_height = $(block).height();
            if (current_height >= tallest_height) {
                tallest_height = current_height;
            }
        });

        $(row).find(column_selector).height(tallest_height);
    });
}

var notify = function(msg, level) {
    if (level === undefined) {
        level = "info";
    }
    level = "alert-" + level;

    var notif_elem = $("#notify_placeholder");
    var notif = '<div class="alert ' + level + ' fade in"><a class="close" data-dismiss="alert">×</a><span>' + msg + '</span></div>';
    $(notif_elem).html(notif);
}
