document.addEventListener('DOMContentLoaded', function(){


    var exampleModal = document.getElementById('exampleModal')
    exampleModal.addEventListener('show.bs.modal', function (event) {

    // Button that triggered the modal
    var button = event.relatedTarget
    // Extract info from data-bs-* attributes
    var recipient = button.getAttribute('data-bs-whatever')
    // If necessary, you could initiate an AJAX request here
    // and then do the updating in a callback.

    //save note from PTC
    document.getElementById('form-note').addEventListener('submit', function (e) {
        e.preventDefault()
        var url = '/save_note_from_PTC'
        let note_date = document.getElementById('id_date').value
        let note_text = document.getElementById('note-text')
        if (note_text.value.length === 0) {
            alert('Empty note is not allowed!')
            document.getElementById('close-modal').click();
        }
        let stud_id = document.getElementById('stud_id').innerHTML
        console.log('subm')

        fetch(url, {
            method: 'POST',
            headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({'note_date': note_date, 
                                    'note_text': note_text.value,
                                    'stud_id': stud_id})
            })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            note_text.value = ''
            document.getElementById('close-modal').click();

            //TODO Create new note on SDP profile, after geting responce from back-end

            })
        })
    //set current date to a date field in modal window
    document.getElementById('id_date').value = new Date().toISOString().substring(0, 10);
    })

    //change color of the text in the concern table
    const refferStatus = document.querySelectorAll(`[data-reffers="reffers"]`) //(`[data-id="box1"]`); data-reffers="reffers"
    refferStatus.forEach((element) => { 
        if (element.innerHTML === 'Concern Resolved') {
            element.parentElement.setAttribute('class', 'col-sm-3 text-success')
        }
        else if (element.innerHTML === 'Referral') {
            element.parentElement.setAttribute('class', 'col-sm-3 text-danger')
        }
    })

})
