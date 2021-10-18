index = 0;
devices = null;
current_name = null;
current_type = null;
current_state = null;
elements = null;
controll_segment = null;

window.onload = start();

function start() {
    fetch('/backend/list').then(function (response) {
        return response.json();
    }).then(function (json) {
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
function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
        currentDate = Date.now();
    } while (currentDate - date < milliseconds);
}
function send_change_state(state) {
    let data = { "name": devices[index]["name"], "state": state };

    fetch("/backend/change", {
        method: "POST",
        body: JSON.stringify(data)
    }).then(res => {
        sleep(100);
        start();
    });

}
function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}
function change_controlls() {
    removeAllChildNodes(controll_segment);
    switch(devices[index]["type"]){
        case "switch":
            button = document.createElement("button");
            button.className = "button is-large";
            button.innerHTML = "Toggle";
            button.onclick = function () { send_change_state(1 - parseInt(devices[index]["state"])) };
            controll_segment.appendChild(button);
            break;
        case "dimmer":
            slider = document.createElement("div");
            slider.id = "slider";
            script = document.createElement("script");
            script.innerHTML =  `
            <script>
                $("#slider").roundSlider({
                    sliderType: "min-range",
                    circleShape: "pie",
                    startAngle: "315",
                    lineCap: "round",
                    radius: 130,
                    width: 20,
                
                    min: -50,
                    max: 50,
                    
                    svgMode: true,
                    pathColor: "#eee",
                    borderWidth: 0,
                    
                    startValue: 0,
                    
                    valueChange: function (e) {
                        var color = e.isInvertedRange ? "#FF5722" : "#8BC34A";
                    
                    $("#slider").roundSlider({ "rangeColor": color, "tooltipColor": color });
                    }
                });
                
                var sliderObj = $("#slider").data("roundSlider");
                sliderObj.setValue(30);
            </script>
            `
            controll_segment.appendChild(slider);
            
            break;
    }

}

function itter_index(offset) {
    index += offset;
    change_active_device();
}

function update_lables() {
    for (i = -1; i < elements.length - 1; i++) {

        elements[i + 1].style.display = "none";
        if (0 <= index + i && index + i < devices.length) {
            elements[i + 1].innerHTML = devices[index + i]["name"];
            elements[i + 1].style.opacity = (elements.length - i) * 0.5;
            switch (i) {
                case -1:
                    elements[i + 1].onclick = function () { itter_index(-1) };
                    break;
                case 0:
                    elements[i + 1].onclick = function () { itter_index(0) };
                    break;
                case 1:
                    elements[i + 1].onclick = function () { itter_index(1) };
                    break;
                case 2:
                    elements[i + 1].onclick = function () { itter_index(2) };
                    break;
            }
            elements[i + 1].style.display = "";
        }
    }
}