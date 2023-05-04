// focus 'roomInput' when user opens the page
document.querySelector("#roomInput").focus();

// submit if the user presses the enter key
document.querySelector("#roomInput").onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter key
        document.querySelector("#roomConnect").click();
    }
};

// redirect to '/room/<roomInput>/'
document.querySelector("#roomConnect").onclick = function () {
    let roomName = document.querySelector("#roomInput").value;
    if (roomName != "") {
        window.location.pathname = "chatroom/" + roomName + "/";
    } else {
        let err = document.querySelector('#room-error');
        err.innerHTML = "Room name is required.<br/>";
    }
}

// redirect to '/room/<roomSelect>/'
// document.querySelector("#roomSelect").onchange = function () {
//     let roomName = document.querySelector("#roomSelect").value.split(" (")[0];
//     window.location.pathname = "chatroom/" + roomName + "/";
// }

$('.chat_list').on('click', function (evt) {
    console.log(this.id);
    var roomName = this.id.split(" (")[0];
    if (roomName != "") {
        window.location.pathname = "chatroom/" + roomName + "/";
    } else {
        let err = document.querySelector('#room-error');
        err.innerHTML = "Room name is required.<br/>";
    }
});
