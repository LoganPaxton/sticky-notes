// Parse Notepad ID from URL
function getNotepadId() {
    const pathParts = window.location.pathname.split('/');
    return pathParts[pathParts.length - 1] || null;
}

// Save all notes
function save_notes() {
    const notes = document.querySelectorAll(".note");
    const notesData = [];

    notes.forEach(note => {
        const title = note.querySelector("h3").innerText.trim();
        const body = note.querySelector("p").innerText.trim();
        notesData.push({ title, body });
    });

    console.log(notesData || "No data!");

    const id = getNotepadId();
    const url = `/api?id=${id}`;

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(notesData)
        }).then(res => {
        if (res.ok) {
            console.log("Notes saved!");
        } else {
            console.log("Failed to save notes.");
        }
    });
}

function fetch_notes() {
    const id = getNotepadId();

    if (id == "" || id.length < 6) {
        return null
    }

    const url = `/api?id=${id}`
    console.log(url)
    fetch(url)
    
        .then(response => {
            
            if (!response.ok) {
                throw new Error("HTTP Error. Status: " + response.status);
            }

            return response.json();
        })
        .then(data => {
            console.log(data);
            insert_data(data);
        })
        .catch(error => {
            console.log("Error: " + error);
        })
}

function insert_data(data) {
    const note_data = data['data'];

    if (!Array.isArray(note_data) || note_data.length === 0) {
        return;
    }

    for (const note of note_data) {
        console.log(`Note ID: ${note['note-id']} | Title: ${note['title']} | Body: ${note['body']}`);
        createNote(note['title'], note['body']);
    }
}

function createNote(title, body) {
    const note = document.createElement("div");
    note.classList.add("note");

    const h3 = document.createElement("h3");
    h3.textContent = title;
    h3.contentEditable = true

    const p = document.createElement("p");
    p.textContent = body;
    p.contentEditable = true;

    note.appendChild(h3);
    note.appendChild(p);

    document.getElementById("notes-container").appendChild(note);
}

setInterval(save_notes, 30000);