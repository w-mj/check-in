function addStudent() {
    $("#new-student").show()
}

function showmax(id) {
    $("#imgModal").attr("src", $("#"+id).attr('src'))
    $("#myModal").modal('show')
}

function doAddStudent() {
    let id = $("#new-student-id").val()
    let name = $("#new-student-name").val()
    let data = {
        token: model.token,
        course_id: model.course.id,
        student_id: id
    }
    if (name != null && name !== "") {
        data['student_name'] = name
    }
    axios.get('/api/add-student', {params: data}).then(()=>location.reload())
}

function doDelStudent(id) {
    let data = {
        token: model.token,
        course_id: model.course.id,
        student_id: id
    }
    axios.get('/api/del-student', {params: data}).then(()=>location.reload())
}