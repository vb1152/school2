document.addEventListener('DOMContentLoaded', function(){

    const refSelectField =document.getElementById('id_refers')
    const elemProgress = document.getElementById('progress')
    const barProgress = document.getElementById('progress-bar')
    const intakeForm = document.getElementById('new-intake-form')

    const inputElements = intakeForm.querySelectorAll("input, select, checkbox, textarea")

    if (refSelectField.value === 'RES') {
        elemProgress.removeAttribute('hidden')
        barProgress.setAttribute('class', 'progress-bar bg-success')
    } else if (refSelectField.value === 'R') {
        elemProgress.removeAttribute('hidden')
        barProgress.setAttribute('class', 'progress-bar bg-danger')
        intakeForm.removeAttribute('hidden')

        inputElements.forEach(element => {
            console.log(element)
            element.removeAttribute('disabled')
            element.setAttribute('required', '')

        })

    }

    refSelectField.addEventListener('change', (e) => {
        if (e.target.value === 'R') {
            console.log('R')
            elemProgress.removeAttribute('hidden')
            barProgress.setAttribute('class', 'progress-bar bg-danger')
            intakeForm.removeAttribute('hidden')

            inputElements.forEach(element => {
                element.removeAttribute('disabled')
                element.setAttribute('required', '')

            })
        } 

        else if (e.target.value === 'RES') {
            console.log('res')
            //Concern Resolved RES - the bar is green
            elemProgress.removeAttribute('hidden')
            barProgress.setAttribute('class', 'progress-bar bg-success')
            intakeForm.setAttribute('hidden', '')
            // sbmConcernBtn.removeAttribute('hidden')
            
            inputElements.forEach(element => {
                element.setAttribute('disabled', '')
                element.removeAttribute('required')

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
            console.log('else')
        }
    })
})
