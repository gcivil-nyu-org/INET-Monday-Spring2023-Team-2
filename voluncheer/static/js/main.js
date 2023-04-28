
// ======================== Editing Profile ===========================

var is_editing = false;
function EditProfile() {
  edit_button = document.getElementById("edit-button");
  view = document.getElementById("edit-form-view");
  edit = document.getElementById("edit-form-edit");
  if (is_editing) {
    is_editing = false;
    edit.style.display = "none";
    view.style.display = "inline-block";
  } else {
    is_editing = true;
    view.style.display = "none";
    edit.style.display = "inline-block";
  }
  $("#edit-form-edit a").html("link")
}

function ShowDetail(element) {
  var id = element.id;
  var form = document.getElementById(id+"-form");
  console.log(form.style.display);
  if (form.style.display != "inline-block") {
    form.style.display = "inline-block";
  } else {
    form.style.display = "none";
  }
};

function ShowSibling(element) {
  var id = element.id;
  var form = document.getElementById(id+"-siblings");
  console.log(form.style.display);
  if (form.style.display != "inline-block") {
    form.style.display = "inline-block";
    element.innerHTML = "Hide All Recurrings"
  } else {
    form.style.display = "none";
    element.innerHTML = "Show All Recurrings"
  }
};