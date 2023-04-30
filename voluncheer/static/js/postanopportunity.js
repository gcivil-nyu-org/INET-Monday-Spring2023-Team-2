const recurring_checkbox = document.getElementById("id_is_recurring")
//Set to recurrence and end_date to disabled
if (!recurring_checkbox.checked) {
    $("#id_recurrence").prop('disabled', true)
    $("#id_end_date").prop('disabled', true)
}

//On click, enable or disable fields
recurring_checkbox.addEventListener("click", enable_fields)

function enable_fields() {
    if (recurring_checkbox.checked) {
        $("#id_recurrence").prop('disabled', false)
        $("#id_end_date").prop('disabled', false)
    }
    else {
        $("#id_recurrence").prop('disabled', true)
        $("#id_end_date").prop('disabled', true)
    }
}


$("#id_category").change(function () {
    var categoryId = $(this).val();

    //Update subcategory...
    var url = $("#opportunity_form").attr("data-subcat-url");
    $.ajax({
        url: url,
        data: {
            'category': categoryId
        },
        success: function (data) {
            $("#id_subcategory").html(data);
        }
    });

    //...then update subsubcategory
    url = $("#opportunity_form").attr("data-subsubcat-url");
    $.ajax({
        url: url,
        data: {
            'category': categoryId
        },
        success: function (data) {
            $("#id_subsubcategory").html(data);
        }
    });
});

$("#id_subcategory").change(function () {
    var subcategoryId = $(this).val();

    //Update subcategory only
    var url = $("#opportunity_form").attr("data-subsubcat-url");
    $.ajax({
        url: url,
        data: {
            'subcategory': subcategoryId
        },
        success: function (data) {
            $("#id_subsubcategory").html(data);
        }
    });
});


$("#id_date").change(function () {
    var date = $(this).val();
    var date = new Date(date);
    var dd = date.getDate();
    var mm = date.getMonth() + 4; //January is 0, restrain to 3 month!
    var yyyy = date.getFullYear();
    if (dd < 10) {
        dd = '0' + dd;
    }
    if (mm < 10) {
        mm = '0' + mm;
    }
    limit = yyyy + '-' + mm + '-' + dd;
    document.getElementById("id_end_date").setAttribute("max", limit);
})