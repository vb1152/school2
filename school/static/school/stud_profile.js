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
    // get current date and save it in a variable
    const current_date = new Date().toISOString().substring(0, 10);
    //set current date to a date field in modal window
    document.getElementById('id_date').value = current_date
    })

    //change color of the text in the concern table
    const refferStatus = document.querySelectorAll(`[data-reffers="reffers"]`) //(`[data-id="box1"]`); data-reffers="reffers"
    refferStatus.forEach((element) => { 
        if (element.innerHTML === 'Concern Resolved') {
            element.parentElement.setAttribute('class', 'col text-success')
        }
        else if (element.innerHTML === 'Referral') {
            element.parentElement.setAttribute('class', 'col text-danger')
        }
    })

    //get all dropdowns from stream in one row
    const streamDropArray = document.querySelectorAll(`[data-functional="add-stream"]`)
    streamDropArray.forEach(streamEl => streamEl.addEventListener("click", makeRow))

})



function makeRow(elem){
    console.log('click make row', elem.target)
    // Find a <table> element with id="myTable":
    var tbodyRef = document.getElementById("stream-table").getElementsByTagName('tbody')[0];
    
    // Insert a row at the end of the table
    let newRow = tbodyRef.insertRow(-1);

    // Insert new cells (<td> elements) at the 1st and 2nd position of the "new" <tr> element:
    var cell1 = newRow.insertCell(0);
    var cell2 = newRow.insertCell(1);
    var cell3 = newRow.insertCell(2);
    var cell4 = newRow.insertCell(3);
    var cell5 = newRow.insertCell(4);
    var cell6 = newRow.insertCell(5);
    var cell7 = newRow.insertCell(6);
    var cell8 = newRow.insertCell(7);

    //send data about new stream to back-end 
    let url = '/new_stream'
    let student_id = document.getElementById('stud_id').innerHTML
    const now = new Date()
    let date_stream_str = now.toLocaleDateString("en-US")
    const inThreeWeeks = new Date(new Date(now).setDate(now.getDate() + 21))
    console.log(date_stream_str)

    fetch(url, {
        method: 'POST',
        headers: {
        'Content-Type':'application/json',
        'X-CSRFToken': csrftoken
            },
        body: JSON.stringify({'stream': elem.target.innerHTML,
                                'stud_id': student_id,
                                // 'start_date': date_stream_str,
                                // 'review_date': inThreeWeeks,
                            })
    })
    
    
    let stud_name = document.getElementById('stud-name').innerHTML
    

   
    
    // Add some text to the new cells:
    cell1.innerHTML = stud_name;
    cell2.innerHTML = elem.target.innerHTML;
    cell3.innerHTML = "1"
    cell6.innerHTML = date_stream_str
    cell7.innerHTML = inThreeWeeks.toLocaleDateString()
    cell8.style.backgroundColor = 'red'



    console.log(current_date)
}