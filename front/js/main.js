function select_and_or(id, str) {
    $('#' + id).val(str);
}

$(function () {
    $('.container').on('click', '.logical', function () {
        console.log("Click na id: " + $(this).attr('id'));
        $(this).val() === "AND" ? select_and_or($(this).attr('id'), "OR") : select_and_or($(this).attr('id'), "AND");
    });
});

$(function () {
    $('.container').on('click', '.dropdown-menu a', function () {
        var par_nod = $(this).closest('.input-group-prepend').find('.criteria').attr('id');
        var full_par_nod = "#" + par_nod + ":first-child";
        console.log(full_par_nod);

        $(full_par_nod).text($(this).text());
        $(full_par_nod).val($(this).text());
        $("html, body").animate({scrollTop: $(document).height()}, 500);

    });
});

var button_id = 2;
var dropdown_id = 2;

$(document).ready(function () {
    $("button[name='adder']").click(function () {
        var tempNode = document.querySelector("div[data-type='template']").cloneNode(true); //true for deep clone
        // console.log(tempNode.find('.logical'));
        $(tempNode).find('.logical').attr('id', 'l' + button_id++);
        $(tempNode).find('.logical').text('AND');
        $(tempNode).find('.logical').val('AND');
        $(tempNode).find('.criteria').attr('id', 'dd' + dropdown_id++);
        $(tempNode).find('.criteria').text('Choose criteria');
        $(tempNode).find('.criteria').val('Choose criteria');
        document.querySelector("div[data-type='template']").parentNode.appendChild(tempNode);
        $("html, body").animate({scrollTop: $(document).height()}, 500);
    });
});
