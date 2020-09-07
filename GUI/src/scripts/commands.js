const cmd_storage_key = 'previous_commands'
const ranCmd_storage_key = 'ran_commands'


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
function UpdateRanCommandsGUI() {
    ClearRanCommandsGUI()
    const ran_commands_parent = document.querySelector('#ran_commands')

    const ran_commands = GetRanCommands()
    Array.from(ran_commands).forEach(cmd => {
        var container = document.createElement('div')

        // deletion X
        var delete_obj = document.createElement('span')
        delete_obj.classList = 'pointer'
        delete_obj.style.float = 'right'
        delete_obj.style.color = 'red'
        delete_obj.innerText = 'X'
        delete_obj.onclick = () => { alert(cmd.id); DeleteRunCommand(cmd.id); UpdateRanCommandsGUI() }



        // command
        var ele = document.createElement('span')
        ele.setAttribute('name', cmd.id)
        ele.classList = 'nav-link ran-command pointer'
        ele.innerHTML = cmd.cmd 
        ele.onclick = () => { 
            SetCurrentRanCommand(cmd)
        }

        container.appendChild(ele)
        container.appendChild(delete_obj)
        
        ran_commands_parent.prepend(container)
    })
}

function GetRanCommands() {
    var ran_commands = localStorage.getItem(ranCmd_storage_key)
    ran_commands = ran_commands != null ? JSON.parse(ran_commands) : []
    return ran_commands
}

function SaveCurrentCmdToRanCommands() {
    // push command to local storage
    const ran_commands = GetRanCommands()

    const cmd = document.querySelector('#output_cmd').innerText
    const output = document.querySelector('#current_ran_command').innerText

    ran_commands.push({"id": uuidv4(), "cmd":cmd, "output": output})
    localStorage.setItem(ranCmd_storage_key, JSON.stringify(ran_commands))

    // console.log(GetRanCommands())
    UpdateRanCommandsGUI()
}

function DeleteRanCommand(id) {
    const ran_commands = GetRanCommands().filter(cmd => { return cmd.id !== id })
    localStorage.setItem(ranCmd_storage_key, ran_commands)
}

function ClearRanCommandsFromLocalStorage() {
    localStorage.removeItem(ranCmd_storage_key)
    UpdateRanCommandsGUI()
}

function ClearRanCommandsGUI() {
    const ran_commands_parent = document.querySelector('#ran_commands')

    const ran_commands = document.querySelectorAll('.ran-command')
    Array.from(ran_commands).forEach(ele => {
        ran_commands_parent.removeChild(ele)
    })
}
function ClearSelectedRanCommand() {
    const ran_commands_parent = document.querySelector('#ran_commands')
    Array.from(ran_commands_parent.children).forEach(ran_command_ele => {
        ran_command_ele.classList.remove('active')
    })
}

function SetCurrentRanCommand(cmd) {
    ClearSelectedRanCommand()
    
    document.querySelector(`[name="${cmd.id}"]`).classList.add('active')

    document.querySelector('#current_ran_command').innerText = cmd.output 
    // document.querySelector('#current_ran_command').style.color = cmd.status == 200 ? 'black' : 'red'
    document.querySelector('#output_cmd').innerText = cmd.cmd
}





// local storage
function ClearPreviousCommandsFromLocalStorage() {
    localStorage.removeItem(cmd_storage_key)
    PopulatePreviousCommandsDropdown()
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
    const uri = 'http://' + location.host + '/api/util/stream_cmd'

    const cmd = document.querySelector('#new_cmd_input').value
    data = {
        "cmd": cmd
    }

    document.querySelector('#output_cmd').innerText = cmd

    // execute command
    const resp = await fetch(uri, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        headers: {
          'Content-Type': 'application/json'
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    })
    
    const reader = resp.body
        .pipeThrough(new TextDecoderStream())
        .getReader()

    let output = ''
    // clear cmd window
    document.querySelector('#current_ran_command').innerText = ''

    while (true) {
        const { value, done } = await reader.read()
        if (done) break;
        output += value
        document.querySelector('#current_ran_command').innerText = output
        // console.log('Received', value)
    }




    // push command to local storage
    var previous_commands = GetPreviousCommands()
    var status = output.split('\n').slice(-1)
    output = output.split('\n').slice(0, -1).join('\n')
    previous_commands.push({"id": uuidv4(), "cmd":cmd})
    localStorage.setItem(cmd_storage_key, JSON.stringify(previous_commands))


    // set previous command dropdown
    PopulatePreviousCommandsDropdown()
    UpdateRanCommandsGUI()
}
