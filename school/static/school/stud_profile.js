document.addEventListener('DOMContentLoaded', function(){
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