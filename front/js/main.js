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

$(function () {
    $('.container').on('click', '.close', function () {
        $(this).closest('div[data-type="template"]').remove();
    });
});

var button_id = 2;
var dropdown_id = 2;

$(document).ready(function () {
    var prefixes = [];
    $.ajax({
        url: "http://127.0.0.1:8080/prefixes",
        dataType: 'json',
        type: 'get',
        crossDomain: true,
        contentType: 'application/json; charset=utf-8',
        success: function (data) {
            prefixes = data;
        }
    });


    $("button[name='adder']").click(function () {
        console.log(prefixes['0']);
        var tempNode = document.querySelector("div[data-type='template']").cloneNode(true); //true for deep clone
        // console.log(tempNode.find('.logical'));
        $(tempNode).find('.logical').attr('id', 'l' + button_id++);
        $(tempNode).find('.logical').text('AND');
        $(tempNode).find('.logical').val('AND');
        $(tempNode).find('.criteria').attr('id', 'dd' + dropdown_id++);
        $(tempNode).find('.criteria').text('Choose criteria');
        $(tempNode).find('.criteria').val('Choose criteria');
        $.each(prefixes['0'], function (k, v) {
            var dropdown = $(tempNode).find('.dropdown-menu');
            $(dropdown).append("<a class='dropdown-item' href='#'>" + v + "</a>");
        });
        tempNode.style.display = "block";
        document.querySelector("div[data-type='template']").parentNode.appendChild(tempNode);
        $("html, body").animate({scrollTop: $(document).height()}, 500);
    });

    //ajax function OVA TRAZI IZMENU I PRAVILNO PAKOVANJE U JSON
    $("button[name='searcher']").click(function () {
        var jsonObj = [];
        var all_divs = document.getElementsByClassName("query-container");
        // console.log(all_divs);
        for (i = 1; i < all_divs.length; i++) {
            var d = $(all_divs[i]);
            var btn = $(d.find('.criteria')[0]);
            var txt = $(d.find('.query-text')[0]);
            var logic = $(d.find('.logical')[0]);
            item = {};
            var key = "";
            $.each(prefixes['0'], function (k, v) {
                if (btn.val() === v) {
                    key = k;
                    return false;
                }
            });
            item [key] = txt.val();
            item ["logic"] = logic.val();

            jsonObj.push(item);
        }
        console.log(jsonObj);
    });
});

