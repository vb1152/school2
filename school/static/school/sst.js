document.addEventListener('DOMContentLoaded', function(){
    
    //select all observation buttons
    const observBtn = Array.from(document.querySelectorAll(`[data-observation="observ"]`))
    // set event listener and values on button after click 
    observBtn.forEach(element => {
        element.addEventListener('click', (btn) => {
            document.getElementById('teacher-id-in-modal').setAttribute('value', btn.target.getAttribute('data-teacher-id'))
            document.getElementById('teacher-name-in-modal').innerHTML = btn.target.getAttribute('data-names')
            document.getElementById('student-id-in-modal').setAttribute('value', btn.target.getAttribute('data-student-id'))
        })
    })

    //save Observation note from sst note
    const formObserv = document.getElementById('form-observ')
    formObserv.addEventListener('submit', function (e) {
        e.preventDefault()
        
        var url = '/save_observation'
        let obs_date = document.getElementById('id_date_observ').value
        let obs_text = document.getElementById('obs-text').value
        let teach_id = document.getElementById('teacher-id-in-modal').value
        let stud_id = document.getElementById('student-id-in-modal').value

        console.log(obs_date, obs_text, teach_id, stud_id)

    //     if (note_text.value.length === 0) {
    //         alert('Empty note is not allowed!')
    //         document.getElementById('close-modal').click();
    //     }
    //     let stud_id = document.getElementById('stud_id').innerHTML
    //     console.log('subm')

        fetch(url, {
            method: 'POST',
            headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                                  'obs_date': obs_date, 
                                  'obs_text': obs_text,
                                  'teach_id': teach_id,
                                  'stud_id': stud_id
                                })
            })
            .then(response => response.json())
            .then(data => {
            console.log(data);
            note_text.value = ''
            document.getElementById('close-modal-obs').click();

    //         //TODO Create new note on SDP profile, after geting responce from back-end

            })
        })
    

});