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
    responseArea = postData('/post', data, 'yes')
}
async function postData(url = '', data = {}, compile) {
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
    if(compile==='yes') {
        const text = await response.text()
        document.getElementById('outputArea').value = text
    }
}

async function updateTextArea(data) {
    const response = await fetch('/get')
    const text = await response.text()
    document.getElementById('textArea').value = text
}

function sse() {
    const evtSource = new EventSource(`/stream/${UUID}`);
    evtSource.addEventListener("ping", function(event) {
        document.getElementById('textArea').value = JSON.parse(event.data).text;
    });
    return evtSource
}

function sendText() {
    const textArea = document.getElementById('textArea');


    function updateValue(e) {
        saveText(textArea.value, UUID)
    }

    textArea.addEventListener('keydown', updateValue);
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
