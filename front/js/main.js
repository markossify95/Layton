function select_or() {
    $('#logical').val("OR");
}

function select_and() {
    $('#logical').val("AND");
}

$(function () {
    $('#logical').click(function () {
        $(this).val() === "AND" ? select_or() : select_and();
    });
});

$(function () {
    $(".dropdown-menu a").click(function () {
        $(".criteria:first-child").text($(this).text());
        $(".criteria:first-child").val($(this).text());
    });
});

$(document).ready(function () {
    $("button[name='adder']").click(function () {
        var domElement = `
        <div class="input-group mb-3">
        <div class="input-group-prepend">
          <button class="btn btn-secondary dropdown-toggle criteria" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Choose criteria</button>
          <div class="dropdown-menu">
            <a class="dropdown-item" href="#">Kriterijum 1</a>
            <a class="dropdown-item" href="#">Kriterijum 2</a>
            <a class="dropdown-item" href="#">Kriterijum 3</a>
          </div>
        </div>
        <input type="text" class="form-control" aria-label="Text input with dropdown button">
        <div class="input-group-append">
          <input type="button" class="btn btn-secondary" id="logical" value="AND">
          </button>
        </div>
      </div>
      `;
        $("#query").append(domElement);
        // $("#query").append($("#comp").html())
    });
});
