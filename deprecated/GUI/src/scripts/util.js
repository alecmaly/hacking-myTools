
function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}


function setEnterAction(selector, callback) {
    var input = document.querySelector(selector);

    // Execute a function when the user releases a key on the keyboard
    input.addEventListener("keyup", function(event) {
        // Number 13 is the "Enter" key on the keyboard
        if (event.keyCode === 13) {
            // Cancel the default action, if needed
            event.preventDefault();
            // Trigger the button element with a click
            callback()
        }
    });
}

async function onLoad() {
    RefreshAll()

    // set input button enter
    setEnterAction('#new_working_dir', () => { document.getElementById("new_working_dir_submit").click() })
    setEnterAction('#new_cmd_input', ExecuteCommand)

    // bind copy to clipboard
    document.querySelector('#current_working_dir').addEventListener('click', copyToClipboard) 
}

const copyToClipboard = evt => {
    const str = evt.target.innerText
    const el = document.createElement('textarea');
    el.value = str;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);

    displayAlert('alert alert-success alert-dismissible fade show', 'Copied to clipboard', 2000)
};


function displayAlert(classes, msg, timer) {
    var alert_anchor = document.getElementById('alert_anchor')
    var alert = document.createElement('div')
        
    alert.classList = classes
    

    alert.innerHTML = msg + `
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    `
    alert_anchor.appendChild(alert)
    setTimeout(() => { $(".alert").alert('close') }, timer)
}


async function RefreshAll() {
    GetWorkingDir()
    PopulatePreviousCommandsDropdown()
    UpdateRanCommandsGUI()
}

// working directory functions
async function GetWorkingDir() {
    var uri = 'http://' + location.host + '/api/util/working_dir'
    var current_dir = await fetch(uri)
    .then(data => { return data.text() })
    .then(text => { return text })

    document.querySelector('#current_working_dir').innerText = current_dir
}

async function SetWorkingDir() {
    var uri = 'http://' + location.host + '/api/util/working_dir'

    data = {
        "path": document.querySelector('#new_working_dir').value
    }
    const response = await fetch(uri, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        headers: {
          'Content-Type': 'application/json'
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: JSON.stringify(data) // body data type must match "Content-Type" header
      });

      GetWorkingDir()
}

















