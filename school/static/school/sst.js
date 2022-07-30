document.addEventListener('DOMContentLoaded', function(){
    
    //document.querySelectorAll(`[data-id="box1"]`);
    const observBtn = Array.from(document.querySelectorAll(`[data-observation="observ"]`))

    console.log(observBtn)

    observBtn.forEach(element => {
        element.addEventListener('click', (btn) => {
            document.getElementById('teacher-id-in-modal').setAttribute('value', btn.target.getAttribute('data-teacher-id'))
            document.getElementById('teacher-name-in-modal').innerHTML = btn.target.getAttribute('data-names')
        })
    })

    // //save Observation note from sst note from PTC
    // document.getElementById('form-note').addEventListener('submit', function (e) {
    //     e.preventDefault()
    //     var url = '/save_note_from_PTC'
    //     let note_date = document.getElementById('id_date').value
    //     let note_text = document.getElementById('note-text')
    //     if (note_text.value.length === 0) {
    //         alert('Empty note is not allowed!')
    //         document.getElementById('close-modal').click();
    //     }
    //     let stud_id = document.getElementById('stud_id').innerHTML
    //     console.log('subm')

    //     fetch(url, {
    //         method: 'POST',
    //         headers: {
    //         'Content-Type':'application/json',
    //         'X-CSRFToken': csrftoken
    //         },
    //         body: JSON.stringify({'note_date': note_date, 
    //                                 'note_text': note_text.value,
    //                                 'stud_id': stud_id})
    //         })
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log(data);
    //         note_text.value = ''
    //         document.getElementById('close-modal').click();

    //         //TODO Create new note on SDP profile, after geting responce from back-end

    //         })
    //     })
    

});