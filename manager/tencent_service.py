import json
from typing import List

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.iai.v20200303 import iai_client, models
from checkin.token import TENCENT_SECRET_KEY, TENCETN_SECRET_ID
import threading
import time


mutex = threading.Lock()
last_time = 0
cnt = 0


def request_tencent(func):
    def _f(*args, **kwargs):
        # mutex.acquire()
        global cnt, last_time
        if last_time == int(time.time()):
            if cnt == 45:
                time.sleep(1)
                last_time = int(time.time())
                cnt = 1
            else:
                cnt += 1
        else:
            last_time = int(time.time())
            cnt = 1
        cred = credential.Credential(TENCETN_SECRET_ID, TENCENT_SECRET_KEY)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "iai.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = iai_client.IaiClient(cred, "ap-beijing", clientProfile)
        res = func(client, *args, **kwargs)
        # mutex.release()
        return res

    return _f


@request_tencent
def create_group(client, name, gid):
    req = models.CreateGroupRequest()
    params = {
        "GroupId": gid,
        "GroupName": name
    }
    req.from_json_string(json.dumps(params))
    resp = client.CreateGroup(req)
    return json.loads(resp.to_json_string())


@request_tencent
def create_person(client, personId, personName, image):
    req = models.CreatePersonRequest()
    params = {
        "GroupId": "all",
        "PersonName": personName,
        "PersonId": personId,
        "Image": image
    }
    req.from_json_string(json.dumps(params))
    resp = client.CreatePerson(req)
    return json.loads(resp.to_json_string())


@request_tencent
def add_to_group(client, personId, group_ids: List[str]):
    req = models.CopyPersonRequest()
    params = {
        "GroupIds": group_ids,
        "PersonId": personId
    }
    req.from_json_string(json.dumps(params))
    resp = client.CopyPerson(req)
    return json.loads(resp.to_json_string())


@request_tencent
def remove_from_group(client, person_id, group_id):
    req = models.DeletePersonFromGroupRequest()
    params = {
        "PersonId": person_id,
        "GroupId": group_id
    }
    req.from_json_string(json.dumps(params))
    resp = client.DeletePersonFromGroup(req)
    return json.loads(resp.to_json_string())


@request_tencent
def get_person_info(client, person_id):
    req = models.GetPersonBaseInfoRequest()
    params = {
        "PersonId": person_id
    }
    req.from_json_string(json.dumps(params))
    resp = client.GetPersonBaseInfo(req)
    return json.loads(resp.to_json_string())


@request_tencent
def delete_face(client, person_id, face_id):
    req = models.DeleteFaceRequest()
    params = {
        "FaceIds": [ face_id ],
        "PersonId": person_id
    }
    req.from_json_string(json.dumps(params))

    resp = client.DeleteFace(req)
    return json.loads(resp.to_json_string())


@request_tencent
def upload_image(client, person_id, image):
    from manager.models import AppUser, JoinClass
    try:
        info = get_person_info(person_id)
        if len(info['FaceIds']) == 5:
            delete_face(person_id, info['FaceIds'][0])
        req = models.CreateFaceRequest()
        params = {
            "Images": [ image ],
            "PersonId": person_id
        }
        req.from_json_string(json.dumps(params))
        resp = client.CreateFace(req)
        return json.loads(resp.to_json_string())
    except TencentCloudSDKException as e:
        if e.code == "InvalidParameterValue.PersonIdNotExist":
            person = AppUser.objects.get(id=person_id)
            c = create_person(person_id, person.name, image)
            class_ids = [str(x.course_id) for x in JoinClass.objects.filter(user=person)]
            if class_ids:
                print(person_id, class_ids)
                add_to_group(person_id, class_ids)
            return c
        raise e


@request_tencent
def checkin(client, course_id, image):
    req = models.SearchFacesRequest()
    params = {
        "GroupIds": [ course_id ],
        "Image": image
    }
    req.from_json_string(json.dumps(params))
    resp = client.SearchFaces(req)
    res = json.loads(resp.to_json_string())
    target_person = res['Results'][0]['Candidates'][0]
    if target_person['Score'] >= 60:
        return target_person['PersonId']
    return None


if __name__ == '__main__':
    print(add_to_group("20164488", ['5']))
