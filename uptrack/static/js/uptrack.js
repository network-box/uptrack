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
