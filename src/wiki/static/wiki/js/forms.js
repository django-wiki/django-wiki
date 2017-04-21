// Bootstrap-specific js for wiki form widgets

function setBtnGroupVal(elem) {
    btngroup = $(elem).parents('.btn-group');
    selected_a = btngroup.find('a[selected]');
    if (selected_a.length > 0) {
        val = selected_a.attr('data-value');
        label = selected_a.html();
    } else {
        btngroup.find('a').first().attr('selected', 'selected');
        setBtnGroupVal(elem);
    }
    btngroup.find('input').val(val);
    btngroup.find('.btn-group-label').html(label);
}
$(document).ready(function() {
    $('.btn-group-form input').each(function() {
        setBtnGroupVal(this);
    });
    $('.btn-group-form li a').click(function() {
        $(this).parent().siblings().find('a').attr('selected', false);
        $(this).attr('selected', true);
        setBtnGroupVal(this);
    });
})
