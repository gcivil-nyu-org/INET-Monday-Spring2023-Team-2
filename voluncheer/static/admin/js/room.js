const roomName = JSON.parse(document.getElementById('roomName').textContent);
const userPK = JSON.parse(document.getElementById('userPK').textContent);
const volunteerJson = JSON.parse(document.getElementById('volunteerJson').textContent);
const organizationJson = JSON.parse(document.getElementById('organizationJson').textContent);

let chatLog = document.querySelector("#msg_history");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");
let msgContainer = document.getElementById("msg_history")

$('.chat_list').on('click', function (evt) {
    console.log(this.id);
    var roomName = this.id;
    window.location.pathname = "chatroom/" + roomName + "/";
});

// adds a new option to 'onlineUsersSelector'
function onlineUsersSelectorAdd(value) {
    if (document.querySelector("option[value='" + value + "']")) return;
    let newOption = document.createElement("option");
    newOption.value = value;
    newOption.innerHTML = value;
    onlineUsersSelector.appendChild(newOption);
}

// removes an option from 'onlineUsersSelector'
function onlineUsersSelectorRemove(value) {
    let oldOption = document.querySelector("option[value='" + value + "']");
    if (oldOption !== null) oldOption.remove();
}

// focus 'chatMessageInput' when user opens the page
chatMessageInput.focus();

// submit if the user presses the enter key
chatMessageInput.onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};

function sendChatMsg() {
    if (chatMessageInput.value.length === 0) return;
    var date = new Date(Date.now()); 
    var photo;
    if (Object.keys(volunteerJson).length) {
        photo = volunteerJson;
    } else if (Object.keys(organizationJson).length) {
        photo = organizationJson;
    }
    var msg = JSON.stringify({
        "user": userPK,
        "message": chatMessageInput.value,
        "room": roomName,
        "timestamp": date.toGMTString(),
        "photo": photo,
    });
    chatSocket.send(msg);

    chatMessageInput.value = "";
}

let chatSocket = null;

function connect() {
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/");

    chatSocket.onopen = function (e) {
        console.log("Successfully connected to the WebSocket.");
    }

    chatSocket.onclose = function (e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function () {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        switch (data.type) {
            case "chat_message":
                var date = new Date(Date.now());
                var incoming_template = `<div class="incoming_msg">
                <div class="incoming_msg_img"> <img src="`+
                data.photo+`" alt="TestOrg"> </div>
                <div class="received_msg">
                  <div class="received_withd_msg">
                    <p>` + data.message + `</p>
                    <span class="time_date">` + date.toGMTString() + `</span></div>
                    </div>
                  </div>`;
                var outgoing_template = `<div class="outgoing_msg">
                <div class="sent_msg">
                  <p>` + data.message + `</p>
                  <span class="time_date">` + date.toGMTString() + `</span> </div>
                  </div>`
                msgContainer.innerHTML += incoming_template + "\n";
                break;
            default:
                console.error("Unknown message type!");
                break;
        }

        // scroll 'chatLog' to the bottom
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    chatSocket.onerror = function (err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }
}
connect();