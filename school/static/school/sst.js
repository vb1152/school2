document.addEventListener('DOMContentLoaded', function () {

    // $(document).ready( function () {
    $('#student_table').DataTable({
        searching: true,
        order: [[0, 'desc']],
    });

    $('#consern_table').DataTable({
        searching: true,
        order: [[0, 'desc']],
    });
    // });


    //select all observation buttons
    const observBtn = Array.from(document.querySelectorAll(`[data-observation="observ"]`))
    // set event listener and values on button after click 
    observBtn.forEach(element => {
        element.addEventListener('click', (btn) => {
            document.getElementById('teacher-id-in-modal').setAttribute('value', btn.target.getAttribute('data-teacher-id'))
            document.getElementById('teacher-name-in-modal').innerHTML = btn.target.getAttribute('data-names')
            document.getElementById('student-id-in-modal').setAttribute('value', btn.target.getAttribute('data-student-id'))
            document.getElementById('stream-id-in-modal').setAttribute('value', btn.target.getAttribute('data-stream-id'))

        })
    })

    //save Observation note from sst note
    const formObserv = document.getElementById('form-observ')
    formObserv.addEventListener('submit', function (e) {
        e.preventDefault()

        var url = '/save_observation'
        let obs_date = document.getElementById('id_date_observ')
        let obs_text = document.getElementById('obs-text')
        let teach_id = document.getElementById('teacher-id-in-modal').value
        let stud_id = document.getElementById('student-id-in-modal').value
        let stream_id = document.getElementById('stream-id-in-modal').value

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                'obs_date': obs_date.value,
                'obs_text': obs_text.value,
                'teach_id': teach_id,
                'stud_id': stud_id,
                'stream_id': stream_id
            })
        })
            .then(response => response.json())
            .then(data => {
                obs_text.value = ''
                obs_date.value = ''
                document.getElementById('close-modal-obs').click();

                alert('Thank you! Observation is saved!')
            })
            .catch((error) => {
                console.error('Error:', error);
                obs_text.value = ''
                obs_date.value = ''
                document.getElementById('close-modal-obs').click();
                alert('ERROR! Some problem.')
            });
    })


});