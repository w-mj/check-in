/*
course = {"name": "\u4eba\u4eba\u4ea4\u4e92", "teacher_id": "100", "times": [{"start_week": 1, "end_week": 10, "start_time": "14:00", "end_time": "16:00", "day": 1}, {"start_week": 1, "end_week": 10, "start_time": "14:00", "end_time": "16:00", "day": 6}]}
 */
function initModifyModel(course) {
    $("#modalTimeList").empty()
    $("#courseName").attr('value', course['name'])
    $("#TeacherName").attr('value', model['user']['name'])
    for (let t of course['times']) {
        addTimeList(t)
    }
}

function modifyCourse(cid) {
    let course = model.courses.filter(x => x.id = cid)[0]
    initModifyModel(course)
}

function createCourse() {
    $("#modalTimeList").empty()
    $("#courseName").attr('value', null)
    $("#TeacherName").attr('value', null)
    addTimeList()
}

let cnt = 1

// time = {"start_week": 1, "end_week": 10, "start_time": "14:00", "end_time": "16:00", "day": 1}
function addTimeList(time={}) {
    let head = $("#modalTimeHead").clone()
    console.log(time);
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
            input.attr('value', v == null? "": v)
            input.attr('disabled', null)
        }
    }
    head.attr('id', 'time-' + cnt)
    cnt++;

    console.log(head.html())
    $("#modalTimeList").append(head)
}

function removeTimeList(id) {
    // console.log('remove' + id)
    $(`#${id}`).remove()
}