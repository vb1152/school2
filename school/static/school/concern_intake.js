document.addEventListener('DOMContentLoaded', function(){
    //  TODO File should be deleted as its not used anymore 
    const consernForm = document.getElementById('consern-form')

    const refSelectField =document.getElementById('id_refers')
    const elemProgress = document.getElementById('progress')
    const barProgress = document.getElementById('progress-bar')
    const intakeForm = document.getElementById('new-intake-form')
    const sbmConcernBtn = document.getElementById('submit-btn-concern')
    
    const inputElements = intakeForm.querySelectorAll("input, select, checkbox, textarea")
    inputElements.forEach(element => {
        element.setAttribute('disabled', '')
    })


    refSelectField.addEventListener('change', (e) => {
        if (e.target.value === 'R') {
            // Referral R - the bar is red -> show red bar, show intake form
            elemProgress.removeAttribute('hidden')
            barProgress.setAttribute('class', 'progress-bar bg-danger')
            intakeForm.removeAttribute('hidden')
           
            
            inputElements.forEach(element => {
                element.removeAttribute('disabled')
                element.setAttribute('required', '')

            })
            // inputsField = intakeForm.getElementsByTagName('input')
            
            // console.log(inputsField.length)
            
            // Array.from(inputsField).forEach(element => {
            //     console.log(element)
            //     element.setAttribute('required', '')
            //     element.setAttribute('class', 'form-control')
            // });
            
            // sbmConcernBtn.setAttribute('hidden', '')

            // focus on the first field of intake form
            document.getElementById('id_timeline').scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"});
            
            // maybe 
                // hide submit button for a consern form. 
                // maybe 

                // Referral R - the bar is red; 
        }

        else if (e.target.value === 'RES') {
            //Concern Resolved RES - the bar is green
            elemProgress.removeAttribute('hidden')
            barProgress.setAttribute('class', 'progress-bar bg-success')
            intakeForm.setAttribute('hidden', '')
            sbmConcernBtn.removeAttribute('hidden')
            
            inputElements.forEach(element => {
                element.setAttribute('disabled', '')
                element.removeAttribute('required')

            })
        }
        else {
            elemProgress.setAttribute('hidden', '')
            intakeForm.setAttribute('hidden', '')
            sbmConcernBtn.removeAttribute('hidden')
            
            inputElements.forEach(element => {
                element.setAttribute('disabled', '')
                element.removeAttribute('required')
            })
        }
    })
})
