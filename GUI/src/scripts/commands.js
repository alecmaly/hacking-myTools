const cmd_storage_key = 'previous_commands'


// GUI
function SetCurrentCommand(cmd) {
    document.querySelector('#new_cmd_input').value = cmd
}


// dropdown
function ClearPreviousCommandsFromDropdown() {
    const dropdown_parent = document.querySelector('#dropdown_previous_commands')
    const previous_commands = document.querySelectorAll('.previous-command')

    previous_commands.forEach(cmd => {
        dropdown_parent.removeChild(cmd)
    })
}

function PopulatePreviousCommandsDropdown() {
    var dropdown_parent = document.querySelector('#dropdown_previous_commands')
    // clear previous commands
    ClearPreviousCommandsFromDropdown()


    // populate previous commands
    const previous_commands = JSON.parse(localStorage.getItem(cmd_storage_key)) || []

    Array.from(previous_commands).forEach(cmd => {
        var ele = document.createElement('div')
        ele.classList = 'dropdown-item pointer previous-command'
        ele.innerHTML  = cmd.cmd
        ele.onclick = function(){ SetCurrentCommand(cmd.cmd) };

        dropdown_parent.prepend(ele)
        
        // <a class="dropdown-item" href="#">Action</a>
    })
}


// ran commands
//current_ran_command | ran_commands
function PopulateRanCommands() {
    ClearRanCommands()
    const ran_commands_parent = document.querySelector('#ran_commands')

    const previous_commands = GetPreviousCommands()
    Array.from(previous_commands).forEach(cmd => {
        var ele = document.createElement('div')
        ele.setAttribute('name', cmd.id)
        ele.classList = 'nav-link ran-command pointer'
        ele.innerHTML = cmd.cmd
        ele.onclick = () => { 
            SetCurrentRanCommand(cmd)
        }
        
        ran_commands_parent.prepend(ele)
    })

}

function ClearRanCommands() {
    const ran_commands_parent = document.querySelector('#ran_commands')

    const ran_commands = document.querySelectorAll('.ran-command')
    Array.from(ran_commands).forEach(ele => {
        ran_commands_parent.removeChild(ele)
    })
}


function SetCurrentRanCommand(cmd) {
    const ran_commands_parent = document.querySelector('#ran_commands')
    Array.from(ran_commands_parent.children).forEach(ran_command_ele => {
        ran_command_ele.classList.remove('active')
    })
    
    document.querySelector(`[name="${cmd.id}"]`).classList.add('active')

    document.querySelector('#current_ran_command').innerText = cmd.output 
    document.querySelector('#current_ran_command').style.color = cmd.status == 200 ? 'black' : 'red'
}





// local storage
function ClearPreviousCommandsFromLocalStorage() {
    localStorage.removeItem(cmd_storage_key)
    PopulatePreviousCommandsDropdown()
    PopulateRanCommands()
}

function GetPreviousCommands() {
    var previous_commands = localStorage.getItem(cmd_storage_key)
    previous_commands = previous_commands != null ? JSON.parse(previous_commands) : []
    return previous_commands
}





// other
async function GetCommandTemplates() {
    var cmds = await fetch('http://' + location.host + '/assets/cmd_templates.json')
                .then(resp => { return resp.json() })
                .then(json => { return json })
    return cmds
}
async function GetCommandTemplate(key) {
    var cmds = await fetch('http://' + location.host + '/assets/cmd_templates.json')
                .then(resp => { return resp.json() })
                .then(json => { return json })


    var cmd = cmds.find(cmd => { return cmd.key === key })
    return cmd.cmd || ''
}

async function SetCurrentCommandFromTemplate(key) {
    var cmd = await GetCommandTemplate(key)
    
    document.querySelector("#new_cmd_input").value = cmd
}



async function ExecuteCommand() {
    const uri = 'http://' + location.host + '/api/util/execute_cmd'

    const cmd = document.querySelector('#new_cmd_input').value
    data = {
        "cmd": cmd
    }

    // execute command
    const resp = await fetch(uri, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        headers: {
          'Content-Type': 'application/json'
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    })
    
    var output = await resp.text().then(text => { return text })


    // push command to local storage
    var previous_commands = GetPreviousCommands()
    previous_commands.push({"id": uuidv4(), "cmd":cmd, "output": output, "status": resp.status})
    localStorage.setItem(cmd_storage_key, JSON.stringify(previous_commands))


    // set previous command dropdown
    PopulatePreviousCommandsDropdown()
    PopulateRanCommands()
    // select latest ran command

    // setTimeout(() => {
        document.querySelector('#ran_commands').children[0].click()
        
    // }, 500)
}
