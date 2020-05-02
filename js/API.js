let UUID = null;
let eventResponse = null;

generateUUId().then(function() {
    eventResponse = sse();
});

sendText();


function sendToAPI(responseArea, text) {
    const data = {
        text: text
    }
    responseArea = postData('/post', data)
}
async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *client
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    const text = await response.json()
    document.getElementById('outputArea').value = text
}

async function updateTextArea(data) {
    const response = await fetch('/get')
    const text = await response.text()
    document.getElementById('textArea').value = text
}

function sse() {
    const evtSource = new EventSource(`/stream/${UUID}`);
    evtSource.addEventListener("ping", function(event) {
        document.getElementById('textArea').value = event.data;
    });
    return evtSource
}

function sendText() {
    const log = document.getElementById('textArea');


    function updateValue(e) {
        saveText(e.target.value, UUID)
    }

    log.addEventListener('input', updateValue);
}

function saveText(text, UUID) {
    const data = {
        text: text,
        user: UUID
    }
    postData('/save', data)
}

async function generateUUId() {
    UUID = await (await fetch('/generateUUID')).text()
}