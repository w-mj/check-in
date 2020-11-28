
function checkin() {
    let data = {
        token: model.token,
        course: model.course.id,
        method: $("#inputState").val(),
        count: $("#inputZip").val()
    }
    axios.get('api/start-checkin', {params: data}).then(()=>{location.reload()})
}

function stop_checkin() {
    let data = {
        token: model.token,
        course: model.course.id
    }
    axios.get('api/stop-checkin', {params: data}).then(()=>location.reload())
}