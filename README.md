# API接口文档

## 一些约定

1. 所有API全部使用GET调用。
2. 所有图片全部使用base64传输。
3. 除登录外所有接口请求时都需要携带token字段用于身份验证。
4. 所有接口的返回值中都包含success字段表示是否请求成功。若请求失败success=false且包含另一个message字段表示出错的原因。

## 登录

### 请求

```
login?id=SY2006230&psw=123456
login?image=人脸登录图片
```

图片 base64 数据，base64 编码后大小不可超过5M。jpg格式长边像素不可超过4000，其他格式图片长边像素不可超2000。支持PNG、JPG、JPEG、BMP，不支持 GIF 图片。

### 返回

```json
{
    "success": true,
    "user": {
        "name": "湛忆初",
        "id": "SY2006123",
        "image": "base64...",
        "token": "balabala"
    },
    "courses": [
        {
            "id": "renrenjiaohu",
            "name": "人人交互",
            "time": [{
            	"start_week": 1,
                "end_week": 19,
                "day": 3,
            	"start_time": "14:00",
            	"end_time": "16:00"
        	}, {
            	"start_week": 1,
                "end_week": 19,
                "day": 5,
            	"start_time": "14:00",
            	"end_time": "16:00"

        	}],
            "checking": false
        }
    ]
}
```

登录成功后返回个人简要信息和课程列表。

user字段中的token为验证信息，之后所有的请求都需要携带token。

课程信息中的时间字段为数组类型，start_week、end_week为起止周数，day为星期几，取值为1-7，start_time与end_time为起止时间。

```json
{
    "success": false,
    "message": "账号/密码错误"
}
```

## 获得课程列表

### 请求

```
course-list?token=token
```

获得此学生的课程列表，返回值与登录中的courses字段一致。

## 获得课程详细信息

### 请求

```
course-info?token=token&id=id
```

id为course-list中课程的id

### 返回

```json
{
    "success": true,
	"name": "人工智能",
    "time": [{
        "start_data": "2020-4-14",
        "repeat": 14,
        "start_time": "14:00",
        "end_time": "16:00"
    }, {
        "start_data": "2020-4-16",
        "repeat": 14,
        "start_time": "14:00",
        "end_time": "16:00"
    }],
    "teacher": "马保国",
    "teacher_id": "mabaoguo",
    "checking": true,
    "method": 1,
    "count": 1,
    "result": [{
            "photographer_id": "SY2006123",
            "photographer_name": "张三",
            "target_id": "SY2006230",
            "target_name": "张三"
        }
    ]
}
```

checking为true时表示正在签到，此时result才有意义。

method为枚举量，含义如下：

+ == 1：自拍。
+ == 2：拍别人。
+ == 3：被别人拍。
+ == 4：拍老师。

count为需要拍照的数量，仅在method==2和3时有意义。

result为签到结果数组。photographer为拍照人，target为被拍照人。

+ method == 1时，photographer_id与target_id相等且均与自身user_id相等视为成功。
+ method == 2时，photographer_id与自身user_id相等视为成功。
+ method == 3时，target_id与自身user_id相等视为成功。
+ method == 4时，target_id与自身teacher_id相等视为成功。

## 签到

### 请求
**签到使用POST请求，参数使用x-www-form-urlencoded**
```
check-in
```

###参数
```
token=balabala&course-id=1&image=base64...
```

### 返回

```json
{
    "success": "true",
    "photographer_id": "SY2006123",
    "photographer_name": "张三",
    "target_id": "SY2006230",
    "target_name": "张三"
}
```

## 上传头像
**上传头像使用POST请求，参数使用x-www-form-urlencoded**
### 请求

```
upload-image
```

### 参数
```
token=balablaba&image=base64..
```

### 返回

```json
{"success": true}
```
