# nuaaTimetableWeb
南航课表获取网页版

本项目在[NUAA_ClassSchedule](https://github.com/miaotony/NUAA_ClassSchedule)这个项目的基础上，使用django2.2.11版本开发。由于嫌麻烦未使用Python虚拟环境，在使用本项目的时候请参照下面的库版本：

Django == 2.2.11

baidu-aip== 2.2.18.0

其他库的版本请参考[NUAA_ClassSchedule](https://github.com/miaotony/NUAA_ClassSchedule)中的requests.txt。

本项目使用百度文字识别api识别验证码，因而，如果你希望使用的话，请勿[百度ai开放平台](https://ai.baidu.com/tech/ocr)申请，在timetable文件夹下面的views.py中填写你的应用的AppID、API Key、Secret Key。

```python
def img_to_str1(image_path):
    # 百度文字基本识别设置
    config = {
        'appId': 'AppID',
        'apiKey': 'API Key',
        'secretKey': 'Secret Key'
    }
    client = AipOcr(**config)
    image = get_file_content(image_path)
    options = {}
    # 设置语言为英文
    options["language_type"] = "ENG"
    result = client.basicGeneral(image, options)
    if 'words_result' in result:
        return '\n'.join([w['words'] for w in result['words_result']])
```

我搭了一个在线网站：kb.ijackyu.com，如果你也希望使用的话，请加我的QQ：1480851073。这么做的原因主要是我的服务器无法同时满足太多人的请求，因而限制人数使用，而且百度的文字识别api每天只能免费调用500次。