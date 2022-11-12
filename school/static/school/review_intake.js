document.addEventListener('DOMContentLoaded', function(){
    const progSelectField =document.getElementById('id_progress')
    const elemProgress = document.getElementById('progress')
    const barProgress = document.getElementById('progress-bar')
    const intakeForm = document.getElementById('new-intake-form')
    const sbmConcernBtn = document.getElementById('submit-btn-concern')

    const inputElements = intakeForm.querySelectorAll("input, select, checkbox, textarea")
    inputElements.forEach(element => {
        element.setAttribute('disabled', '')
    })

    console.log(intakeForm)

    progSelectField.addEventListener('change', (e) => {
        console.log('change', e.target.value)
        if (e.target.value === 'Y') {
            //The bar is green
            elemProgress.removeAttribute('hidden')
            barProgress.setAttribute('class', 'progress-bar bg-success')
            intakeForm.setAttribute('hidden', '')
            // sbmConcernBtn.removeAttribute('hidden')
            
            inputElements.forEach(element => {
                element.setAttribute('disabled', '')
                element.removeAttribute('required')
            })
        }
        else if (e.target.value === 'N') {
            //Concern Resolved RES - the bar is green
            elemProgress.removeAttribute('hidden')
            barProgress.setAttribute('class', 'progress-bar bg-danger')
            intakeForm.removeAttribute('hidden')
            // sbmConcernBtn.removeAttribute('hidden')
            
            inputElements.forEach(element => {
                element.removeAttribute('disabled')
                element.setAttribute('required', '')
            })
        }
        else {
            elemProgress.setAttribute('hidden', '')
            intakeForm.setAttribute('hidden', '')
            // sbmConcernBtn.removeAttribute('hidden')
            
            inputElements.forEach(element => {
                element.setAttribute('disabled', '')
                element.removeAttribute('required')
            })
        }
    })
})
