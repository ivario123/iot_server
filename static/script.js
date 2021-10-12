index = 0;
devices = null;
current_name = null;
current_type = null;
current_state = null;
elements = null;
controll_segment = null;

window.onload = start();

function start() {
    fetch('/backend/list').then(function(response) {
        return response.json();
    }).then(function(json) {
        console.log(json);
        devices = json;
        current_name = document.getElementById("name");
        current_type = document.getElementById("type");
        current_state = document.getElementById("state");
        elements = [document.getElementById("1"), document.getElementById("2"), document.getElementById("3"), document.getElementById("4")]
        controll_segment = controll;
        controll_segment.innerHTML = "";
        update_lables();
        if (json.length == 0) {
            current_name.innerHTML = "No devices connected"
            return
        }
        change_active_device();

    });
}

function change_active_device() {
    update_lables();
    change_controlls();
    if (devices.length == 0) {
        current_name.innerHTML = "No devices connected"
        return
    }
    current_name.innerHTML = devices[index]["name"];
    current_state.innerHTML = devices[index]["state"];
    current_type.innerHTML = devices[index]["type"];
}

function send_change_state(state) {
    let data = { "name": devices[index]["name"], "state": state };

    fetch("/backend/change", {
        method: "POST",
        body: JSON.stringify(data)
    }).then(res => {
        start();
    });
}

function change_controlls() {
    if (devices[index]["type"] == "switch") {
        button = document.createElement("button");
        button.innerHTML = "Toggle";
        button.onclick = function() { send_change_state(1 - parseInt(devices[index]["state"])) };

        controll_segment.appendChild(button);
        return
    }

}

function itter_index(offset) {
    index += offset;
    change_active_device();
}

function update_lables() {
    for (i = -1; i < elements.length - 1; i++) {
        if (index + i >= 0 && index + i < devices.length) {
            elements[i + 1].innerHTML = devices[index + i]["name"];
            elements[i + 1].style.opacity = (elements.length - i) * 0.7;
            elements[i + 1].onclick = itter_index(i);
        } else {

            elements[i + 1].style.display = "none";
        }
    }
}