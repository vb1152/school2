document.addEventListener('DOMContentLoaded', function(){
    //get all dropdowns from stream in one row
    const streamDropArray = document.querySelectorAll(`[data-functional="add-stream"]`)
    streamDropArray.forEach(streamEl => streamEl.addEventListener("click", makeRow))

    var myModal = document.getElementById('exampleModal')
    var myInputDate = document.getElementById('id_new_review_date')
    

    myModal.addEventListener('shown.bs.modal', function (el) {
        //set old date into datepicker window 
        var old_date_elem = el.relatedTarget
        myInputDate.setAttribute("value", old_date_elem.getAttribute('data-date'));
        // var stream_id = el.relatedTarget.getAttribute('data-stream-id')
        myInputDate.setAttribute('data-stream-id', old_date_elem.getAttribute('data-stream-id'))
        console.log(old_date_elem)
    })

    const formReviewDate = document.getElementById('form-review-date')
    formReviewDate.addEventListener('submit', function (e) {
        e.preventDefault()

        const url = '/save_new_review_date/'
        let new_date = document.getElementById('id_new_review_date')
        fetch(url, {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                'new_review_date': new_date.value,
                'stream_id': new_date.getAttribute('data-stream-id')
            })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('close-modal').click();
            // TODO get new date from responce and set it to clicked link
            // this is a functionality behind location.reload(). It needs to update 
            // new review date on a student profile page.
            location.reload()
        })
        .catch((error) => {
            console.log(error)
            document.getElementById('close-modal').click();
            alert('ERROR! Some problem.' + toString(error))
        });
    })

})


function makeRow(elem){
    console.log('click make row', elem.target)
    // Find a <table> element with id="myTable":
    var tbodyRef = document.getElementById("stream-table").getElementsByTagName('tbody')[0];
    
    // Insert a row at the end of the table
    let newRow = tbodyRef.insertRow(-1);

    // Insert new cells (<td> elements) at the 1st and 2nd position of the "new" <tr> element:
    var cell2 = newRow.insertCell(0);
    var cell3 = newRow.insertCell(1);
    var cell4 = newRow.insertCell(2);
    var cell5 = newRow.insertCell(3);
    var cell6 = newRow.insertCell(4);
    var cell7 = newRow.insertCell(5);
    var cell8 = newRow.insertCell(6);


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
        body: JSON.stringify({'stream_name': elem.target.innerHTML,
                              'stud_id': student_id,
                            })
    })
    
    // Add some text to the new cells:
    cell2.innerHTML = elem.target.innerHTML;
    cell3.innerHTML = "1"
    cell6.innerHTML = date_stream_str
    cell7.innerHTML = inThreeWeeks.toLocaleDateString()
    cell8.style.backgroundColor = 'red'

}