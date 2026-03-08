const mobileMenu = document.getElementById('mobile-menu');
const navMenu = document.querySelector('.nav-menu');

mobileMenu.addEventListener('click', () => {
    mobileMenu.classList.toggle('active');
    navMenu.classList.toggle('active');
});

document.getElementById('show-add-note-form').addEventListener('click', function() {
    document.querySelector('.add-note-form').style.display = 'block';
});

function deleteNote(noteId) {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
    })
    .then(response => {
        if (response.ok) {
            // Ak server vrátil úspešnú odpoveď, odstránime poznámku z DOM
            const noteItem = document.querySelector(`[onclick="deleteNote('${noteId}')"]`).closest('.note-item');
            if (noteItem) {
                noteItem.remove();
            }
        } else {
            console.error("Error deleting note:", response.status);
        }
    })
    .catch(error => {
        console.error("Error deleting note:", error);
    });
}