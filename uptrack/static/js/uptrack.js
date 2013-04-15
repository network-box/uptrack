update_form = function(elem) {
    if (elem === undefined) {
        /* Make a 'new' form */
        $("legend").text(function(i, val) {
            return val.replace('Edit ', 'New ');
        });
        $("input[type=hidden]").each(function(i, input) {
            if ($(input).attr('name') === 'id') {
                $(input).val('');
            }
        });
        $("input[type=text]").each(function(i, input) {
            $(input).val('');
        });
    } else {
        /* Make an 'edit' form */
        $("legend").text(function(i, val) {
            return val.replace('New ', 'Edit ');
        });
        $("input[type=hidden]").each(function(i, input) {
            if ($(input).attr("name") === "id") {
                $(input).val($.trim($(elem).attr('data-id')));
            }
        });
        $("input[type=text]").each(function(i, input) {
            var name = $(input).attr("name");
            if (name === "name") {
                $(input).val($.trim($(elem).text()));
            } else {
                $(input).val($.trim($(elem).attr("data-"+name)));
            }
        });
    }
}

listitem_clicked = function(elem) {
    /* Set the style */
    $(".uptrack_listitem.uptrack_selected").removeClass("uptrack_selected");
    $(elem).addClass("uptrack_selected");

    /* Enable the 'delete' button */
    $("#uptrack_listcontrols > ul > li.last").removeClass("disabled");

    /* Update the form */
    update_form(elem);
}

save_item = function(item, form) {
    var list = $('#uptrack_list');
    var controls = $('#uptrack_listcontrols')[0];

    var set_attributes = function(elem, obj) {
        $.each(obj, function(k, v) {
            if (k === "id") {
                return;
            } else if (k === "name") {
                elem.text(v);
            } else {
                elem.attr('data-'+k, v);
            }
        });
    }

    var edited = false;

    $(list).find('li').each(function(i, li) {
        if ($(li).attr('data-id') === item.id.toString()) {
            /* Modify the existing item */
            set_attributes($(li), item);
            edited = true;
        }
    });

    if (!edited) {
        /* Add the new item */
        var ul = $(list).find('ul');
        if (!ul.length) {
            /* This is the first one */
            ul = $('<ul/>');
            $(list).html(ul);
            $(list).removeClass("uptrack_disabled");
        } else {
            ul = ul[0];
        }

        var li = $('<li/>', {'class': 'uptrack_listitem',
                             'data-id': item.id.toString()});
        set_attributes($(li), item);
        $(li).click(function() {
            listitem_clicked($(li));
        });

        $(ul).append(li);
        $(li).click();
    }
}

remove_item = function(item) {
    var selected = $(".uptrack_listitem.uptrack_selected");
    if ($(selected).attr("data-id") === $(item).attr("data-id")) {
        /* The user didn't select another entry during the request */
        update_form();
    }

    $(item).remove();

    if (!$(".uptrack_listitem").length) {
        /* We just removed the last one */
        $("#uptrack_list").addClass("uptrack_disabled")
                          .text("No releases configured.");
    }
}

prepare_lists = function() {
    $(".uptrack_listitem").each(function(i, item) {
        $(item).click(function() {
            listitem_clicked($(item));
        });
    });

    $("#uptrack_listadd").click(function() {
        $(".uptrack_listitem.uptrack_selected").removeClass('uptrack_selected');
        update_form();
    });

    $("#uptrack_listremove").click(function() {
        $(this).addClass('disabled');
        var item = $(".uptrack_listitem.uptrack_selected");

        $.get($(this).attr("data-action"), {'id': $(item).attr("data-id")},
            function(data) {
                remove_item(item);
            }.bind(this), 'json');

        return false;
    });
}

ajaxify_forms = function() {
    $('form.ajax').each(function(i, form) {
        $(form).submit(function() {
            $(this).find('button[type=submit]').attr('disabled', 'disabled');

            $.post($(this).attr('action'), $(this).serialize(),
                function(data) {
                    save_item(data[$(this).attr('data-param')], $(this));

                    $(this).find('button[type=submit]').removeAttr('disabled');
                }.bind(this), 'json');

            return false;
        });
    });
}

$(document).ready(function() {
    ajaxify_forms();
    prepare_lists();
});
