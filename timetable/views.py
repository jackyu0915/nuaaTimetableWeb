from django.shortcuts import render, HttpResponse, redirect
from timetable import models
from functools import wraps
import os
from platform import system as system_platform
import time
import logging
import argparse
from getpass import getpass
from datetime import datetime, timedelta
from pytz import timezone
from timetable.getClassSchedule import *
from aip import AipOcr
from PIL import Image
import json


# Create your views here.


# 文字识别
def get_file_content(file):
    with open(file, 'rb') as fp:
        return fp.read()


def img_to_str(image_path):
    # 百度文字精确识别设置
    config = {
        'appId': '19099446',
        'apiKey': 'CaKSFYkYzCl98K6hVxT1ji2q',
        'secretKey': 'cgW37s22yBcXVVCDFbA99pxy7gE8h9Pl'
    }
    client = AipOcr(**config)
    image = get_file_content(image_path)
    options = {}
    options["language_type"] = "ENG"
    result = client.basicAccurate(image, options)
    # result = client.basicGeneral(image, options)
    if 'words_result' in result:
        return '\n'.join([w['words'] for w in result['words_result']])


def img_to_str1(image_path):
    # 百度文字基本识别设置
    config = {
        'appId': '19099446',
        'apiKey': 'CaKSFYkYzCl98K6hVxT1ji2q',
        'secretKey': 'cgW37s22yBcXVVCDFbA99pxy7gE8h9Pl'
    }
    client = AipOcr(**config)
    image = get_file_content(image_path)
    options = {}
    # 设置语言为英文
    options["language_type"] = "ENG"
    result = client.basicGeneral(image, options)
    if 'words_result' in result:
        return '\n'.join([w['words'] for w in result['words_result']])


def aao_logins(request):
    # 学号及密码
    error = ''
    if request.method == 'POST':
        stuID = request.POST.get('username')
        stuPwd = request.POST.get('pwd')
        is_login = request.get_signed_cookie('is_login', salt='sha1', default='')
        stuID = str(stuID)
        userInfo = models.user_info.objects.get(user=stuID)
        logintimes = int(userInfo.times)
        print('------------')
        print(logintimes)
        if userInfo != '':
            if userInfo.pwd == stuPwd:
                # 记录登陆次数
                logintimes = logintimes + 1

                allinfo1 = models.user_info.objects.get(user=stuID)
                allinfo1.times = logintimes
                allinfo1.save()
                url = request.GET.get('url')
                if url:
                    return_url = url
                else:
                    return_url = '/home/'
                ret = redirect(return_url)
                ret.set_signed_cookie('is_login', 'true', salt='sha1')  # 加密
                ret.set_signed_cookie('ID', stuID, salt='sha1')
                ret.set_signed_cookie('pwd', stuID, salt=stuPwd)
                # 每2次更新一下数据
                if ((logintimes + 2) % 1) == 0:
                    models.lesson_info.objects.filter(user=stuID).delete()
                else:
                    return ret
                choice = 0  # 0 for std, 1 for class.个人课表or班级课表
                retry_cnt = 3  # 登录重试次数
                semester_year = '2019-2020'
                semester = '2'
                semester_start_date = datetime(2020, 3, 16, 0, 0, 0, tzinfo=timezone('Asia/Shanghai'))

                # 百度文字识别接口识别，每天免费500次，这里调用了两次，防止不一样
                try:
                    captcha_str = ''
                    while True:
                        # Captcha 验证码 # Fix Issue #13 bug, but only for Windows & MacOS.
                        captcha_resp = session.get(host + '/eams/captcha/image.action')  # Captcha 验证码图片
                        captcha_img = Image.open(BytesIO(captcha_resp.content))
                        # captcha_img.show()  # show the captcha
                        cap = captcha_img.resize((95, 35), Image.ANTIALIAS)
                        cap.save("cap0417.png")
                        captcha_str = img_to_str('cap0417.png')
                        captcha_str = captcha_str.replace(' ', '')
                        # 由于使用了精确文字识别，经常只显示三个字母
                        if len(captcha_str) > 3:
                            break
                    print(captcha_str)
                    name = aao_login(stuID, stuPwd, captcha_str, retry_cnt)
                    temp_time = time.time()  # 计个时看看
                    print('\n## Meow~下面开始获取{}课表啦！\n'.format({0: '个人', 1: '班级'}.get(choice)))
                    courseTable = getCourseTable(choice=choice)

                    list_lessonObj = parseCourseTable(courseTable)
                    for lesson in list_lessonObj:
                        models.lesson_info.objects.create(info=lesson, user=stuID)
                    print('## 下面开始获取考试信息啦！\n')
                    examSchedule = getExamSchedule()
                    list_examObj = parseExamSchedule(examSchedule)
                except Exception as e:
                    print("ERROR! 欢迎在GitHub上提出issue & Pull Request!")
                    print(e)
                finally:
                    session.cookies.clear()  # 清一下cookie
                    if system_platform() == 'Windows':  # Fix Linux `sh: 1: pause: not found` bug
                        os.system('pause')
                return ret
            else:
                error = '用户名或者密码错误'
    return render(request, 'aao_login.html', {'error': error})


def login_requires(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        # print(request.COOKIES)
        # is_login = request.COOKIES.get('is_login')
        is_login = request.get_signed_cookie('is_login', salt='sha1', default='')
        if is_login != 'true':
            return redirect('/aao_login/?url=' + request.path_info)
        ret = func(request, *args, **kwargs)
        return ret

    return inner


@login_requires
def index(request):
    return redirect('/home/')


# 课表主页
@login_requires
def home(request):
    user1 = request.get_signed_cookie('ID', salt='sha1', default='')
    # print('\n-------')
    # print(user1)
    infos1 = models.lesson_info.objects.values_list('user', 'info')
    # print(infos1[1])
    infos = []
    for i in infos1:
        infos.append(i)
    # print(infos)
    # 处理数据
    les_info = []
    les_info1 = []
    for info in infos:
        # les_info1 = []
        if info[0] == user1:
            les_info1 = str(info[1]).split('|')
            # print(les_info1)
            les_info.append(les_info1)
    print('上课信息获取成功')
    # print(les_info)
    # 生成二维列表
    list_lesson = [['' for i in range(11)] for j in range(7)]
    for list in les_info:
        if str(list[0]) == "体育":
            continue
        weeks = list[3]
        weeks = list[3][:3] + '-' + list[3][-3:]
        weeks = weeks.replace(',', '')
        # print(weeks)
        a = str(list[4])
        times = a
        times = times.replace('星期', '')
        times = times.replace(' 第', ',')
        times = times.replace('节', '')
        times1 = times.split(',')
        lenth = len(times1)
        for l in range(1, lenth):
            a = int(times1[0]) - 1
            b = int(times1[l]) - 1
            # print(a,b)
            list_lesson[a][b] = str(list[0]) + '@' + str(list[2]) + '\n' + str(weeks)
    # print(list_lesson)

    return render(request, 'timetable.html', {'courseList': json.dumps(list_lesson)})


def all_timetable(requests):
    return HttpResponse('hello')


@login_requires
def pwd_edit(request):
    # get请求
    if request.method == 'GET':
        return render(request, 'edit_pwd.html')
    # post请求
    else:
        # 获取用户提交的出版社
        user = request.POST.get('user')
        pwd_old = request.POST.get('pwd_old')
        pwd = request.POST.get('pwd')
        user_obj = models.user_info.objects.get(user=user)
        if pwd_old == user_obj.pwd:
            user_obj.pwd = pwd
            user_obj.save()  # 将修改内容提交到数据库
        else:
            error = ''
        return redirect('/home/')
