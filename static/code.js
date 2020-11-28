/*
course = {"name": "\u4eba\u4eba\u4ea4\u4e92", "teacher_id": "100", "times": [{"start_week": 1, "end_week": 10, "start_time": "14:00", "end_time": "16:00", "day": 1}, {"start_week": 1, "end_week": 10, "start_time": "14:00", "end_time": "16:00", "day": 6}]}
 */
function initModifyModel(course) {
    $("#modalTimeList").empty()
    $("#modifyModalHead").text("修改课程")
    $("#courseName").val(course['name'])
    $("#TeacherName").val(model['user']['name'])
    $("#modalSaveButton").attr('onclick', `addCourse(${course['id']})`)
    for (let t of course['times']) {
        addTimeList(t)
    }
}

function modifyCourse(cid) {
    let course = model.courses.filter(x => x.id === cid)[0]
    initModifyModel(course)
}

function createCourse() {
    $("#modalTimeList").empty()
    $("#modifyModalHead").text("新建课程")
    $("#courseName").val(null)
    $("#TeacherName").val(null)
    $("#modalSaveButton").attr('onclick', "addCourse()")
    addTimeList()
}

let cnt = 1

// time = {"start_week": 1, "end_week": 10, "start_time": "14:00", "end_time": "16:00", "day": 1}
function addTimeList(time={}) {
    let head = $("#modalTimeHead").clone()
    // console.log(time);
    for (let child of head.children()) {
        child = $(child)
        let input = $(child.children()[0])
        // console.log(input);
        if (input.prop('tagName') === 'BUTTON') {
            input.attr('class', 'btn btn-danger')
            input.text('-')
            input.attr('onclick', `removeTimeList("time-${cnt}")`)
        } else {
            let v = time[input.attr('placeholder')]
            input.val(v == null? "": v)
            input.attr('disabled', null)
        }
    }
    head.attr('id', 'time-' + cnt)
    cnt++;

    // console.log(head.html())
    $("#modalTimeList").append(head)
}

function removeTimeList(id) {
    $(`#${id}`).remove()
}

function addCourse(id=null) {
    let courseName = $("#courseName").val()
    let token = model.token
    console.log(courseName);

    let timeList = $("#modalTimeList").children()
    let data = {
        token,
        courseName
    }
    // let url = `api/add-course?token=${token}&courseName=${courseName}`
    if (id != null) {
        // url += `&id=${id}`
        data['id'] = id
    }
    for (let i =0; i < timeList.length; i++) {
        console.log(i);
        let time = $(timeList[i])
        for (let v of time.children()) {
            let t = $($(v).children()[0])
            if (t.prop('tagName') === 'INPUT') {
                // url += `&${t.attr('placeholder')}.${i}=${t.val()}`
                data[`${t.attr('placeholder')}${i}`] = t.val()
            }
        }
    }
    console.log(data);
    axios.get('api/add-course', {params: data}).then(response => {
        location.reload();
    })
}