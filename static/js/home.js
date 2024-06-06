const homeForm = document.getElementById("home-form");
const csrf = document.getElementsByName('csrfmiddlewaretoken');
const url = ""

let filter = null
const photoName = document.getElementById('id_name')
const photoImage = document.getElementById('id_image')

let id = null


homeForm.addEventListener('submit', e=>{
    e.preventDefault()

    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('name', photoName.value)
    fd.append('image', photoImage.files[0])
    fd.append('action', filter)
    fd.append('id', id)

    console.log(photoImage.files[0])

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(response){
            const data = JSON.parse(response.data)
            
            console.log(response)
            const sText = `successfully saved ${response.name}`
            handleAlerts('success', sText)
        },
        error: function(error){
            console.log(error)
            handleAlerts('danger', 'ups..something went wrong')
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})