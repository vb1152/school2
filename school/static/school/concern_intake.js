document.addEventListener('DOMContentLoaded', function(){

    const refSelectField =document.getElementById('id_refers')
    const elemProgress = document.getElementById('progress')
    const barProgress = document.getElementById('progress-bar')
    const intakeForm = document.getElementById('containter-intake')
    const sbmConcernBtn = document.getElementById('submit-btn-concern')

    refSelectField.addEventListener('change', (e) => {
        console.log(e.target.value)
        if (e.target.value === 'R') {
            // Referral R - the bar is red
            //show red bar 
            // show intake form
            elemProgress.removeAttribute('hidden')
            barProgress.setAttribute('class', 'progress-bar bg-danger')
            intakeForm.removeAttribute('hidden')
            sbmConcernBtn.setAttribute('hidden', '')
            
            
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

        }
        else {
            elemProgress.setAttribute('hidden', '')
            intakeForm.setAttribute('hidden', '')
            sbmConcernBtn.removeAttribute('hidden')

        }
    })
    

})
