const imageForm = document.getElementById("image-form");
const confirmBtn = document.getElementById("confirm-btn");
const csrf = document.getElementsByName('csrfmiddlewaretoken');
const imageContainer = document.getElementById('img-pic')
const name = document.getElementById('id_name')
const image = document.getElementById('id_image')
const btnBox = document.getElementById('btn-box')
const url = ""

const mediaURL = window.location.href
console.log(mediaURL)

const btns = [...btnBox.children]
let filter = null

btns.forEach(btn => btn.addEventListener('click', ()=>{
    filter = btn.getAttribute('data-filter')

    console.log(filter)
}))


imageForm.addEventListener('submit', e=>{
    e.preventDefault()

    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('name', photoName)
    fd.append('image', photoImage)
    fd.append('action', filter)
    fd.append('id', photoID)

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(response){
            const data = JSON.parse(response.data)
            console.log(response)
            window.location.reload();
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