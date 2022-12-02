document.addEventListener('DOMContentLoaded', function(){
    const progSelectField =document.getElementById('id_progress')
    const elemProgress = document.getElementById('progress')
    const barProgress = document.getElementById('progress-bar')

    progSelectField.addEventListener('change', (e) => {
        if (e.target.value === 'Y') {
            //The bar is green
            elemProgress.removeAttribute('hidden')
            barProgress.setAttribute('class', 'progress-bar bg-success')
        }
        else if (e.target.value === 'N') {
            elemProgress.removeAttribute('hidden')
            barProgress.setAttribute('class', 'progress-bar bg-danger')
        }
        else {
            elemProgress.setAttribute('hidden', '')
        }
    })
})
