#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
getClassSchedule  登录教务系统，获取课表，进行解析及导出

@Author: MiaoTony,JackYu
"""

import requests
import re
from bs4 import BeautifulSoup
from hashlib import sha1
import time
import random
import json
import logging
import tkinter as tk
import tkinter.ttk
from PIL import Image, ImageTk
from io import BytesIO
# from pytesseract import image_to_string
from timetable.lessonObj import Lesson
from timetable.examObj import Exam
from aip import AipOcr

session = requests.Session()
UAs = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
    "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
]
UA = random.choice(UAs)
headers = {
    "User-Agent": UA,  # UAs[random.randint(0, len(UAs) - 1)],  # random UA
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    # "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    # "Cookie":"GSESSIONID=F6052EDFBEF1E44EEE69375BA5F233CD;SERVERNAME=s2;JSESSIONID=F6052EDFBEF1E44EEE69375BA5F233CD;semester.id=62"
}
# 设置session的请求头信息
session.headers = headers
host = r'http://aao-eas.nuaa.edu.cn'

# 文字识别
def get_file_content(file):
    with open(file, 'rb') as fp:
        return fp.read()

def img_to_str(image_path):
    config = {
        'appId': '19099446',
        'apiKey': 'CaKSFYkYzCl98K6hVxT1ji2q',
        'secretKey': 'cgW37s22yBcXVVCDFbA99pxy7gE8h9Pl'
    }
    client = AipOcr(**config)
    image = get_file_content(image_path)
    options = {}
    options["language_type"] = "ENG"
    # 低精度版
    # result = client.basicGeneral(image, options)
    # 高精度版
    result = client.basicAccurate(image, options)
    # 正确的返回内容
    # {'log_id': 6209448477332784560, 'words_result_num': 1, 'words_result': [{'words': 'UKhi '}]}
    # 错误码例子
    # errorcode = {
    #     "error_code": 110,
    #     "error_msg": "Access token invalid or no longer valid"
    # }
    # 错误码为17代表当日500次用完 ,18代表QPS超限额
    if 'error_code' in result:
        if result['error_code'] == 17:
            result = client.basicGeneral(image, options)
    if 'words_result' in result:
        return '\n'.join([w['words'] for w in result['words_result']])


def aao_login(stuID, stuPwd, captcha_str, retry_cnt=1):
    """
    登录新教务系统
    :param stuID: 学号
    :param stuPwd: 密码
    :param retry_cnt: 登录重试次数
    :return: name: {str} 姓名(学号)
    """
    try_cnt = 1
    while try_cnt <= retry_cnt:
        # session.cookies.clear()  # 先清一下cookie

        r1 = session.get(host + '/eams/login.action')
        # logging.debug(r1.text)
        # captcha_resp = session.get(host + '/eams/captcha/image.action')  # Captcha 验证码图片

        # 验证码识别
        captcha_str = ''
        while True:
            t = time.time()
            timenow = int(round(t * 1000))
            # print(timenow)
            # Captcha 验证码
            captcha_resp = session.get(host + '/eams/captcha/image.action?d=' + str(timenow))  # Captcha 验证码图片
            captcha_img = Image.open(BytesIO(captcha_resp.content))
            # captcha_img.show()  # show the captcha
            cap = captcha_img.resize((95, 35), Image.ANTIALIAS)
            cap.save("cap" + str(stuID) + ".png")
            captcha_str = img_to_str('cap' + str(stuID) + '.png')
            captcha_str = captcha_str.replace(' ', '')
            # 由于使用了精确文字识别，经常只显示三个字母
            if len(captcha_str) > 3:
                break

        print("本次验证码是："+captcha_str)
        temp_token_match = re.compile(r"CryptoJS\.SHA1\(\'([0-9a-zA-Z\-]*)\'")

        # 搜索密钥
        content = r1.text
        if temp_token_match.search(content):
            print("Search token OK!")
            temp_token = temp_token_match.search(r1.text).group(1)
            logging.debug(temp_token)
            postPwd = temp_token + stuPwd
            # logging.debug(postPwd)

            # 开始进行SHA1加密
            s1 = sha1()  # 创建sha1对象
            s1.update(postPwd.encode())  # 对s1进行更新
            postPwd = s1.hexdigest()  # 加密处理
            # logging.debug(postPwd)  # 结果是40位字符串


            # 开始登录啦
            postData = {'username': stuID, 'password': postPwd, 'captcha_response': captcha_str}
            time.sleep(0.5 * try_cnt)  # fix Issue #2 `Too Quick Click` bug, sleep for longer time for a new trial
            r2 = session.post(host + '/eams/login.action', data=postData)
            if r2.status_code == 200 or r2.status_code == 302:
                logging.debug(r2.text)
                temp_key = temp_token_match.search(r2.text)
                if temp_key:  # 找到密钥说明没有登录成功，需要重试
                    print("学号与密码错误或者验证码识别出错，请重新登录\n")
                    temp_key = temp_key.group(1)
                    logging.debug(temp_key)
                    exit(2)
                elif re.search(r"ui-state-error", r2.text):  # 过快点击
                    print("ERROR! 请不要过快点击!\n")
                    time.sleep(1)
                    try_cnt += 1
                    # session.headers["User-Agent"] = UAs[1]  # random.randint(0, len(UAs)-1)  # 换UA也不行
                    # exit(3)
                else:
                    temp_soup = BeautifulSoup(r2.text.encode('utf-8'), 'lxml')
                    name = temp_soup.find('a', class_='personal-name').string.strip()
                    print("Login OK!\nHello, {}!".format(name))
                    return name
            else:
                print("登录失败!\n")
                # exit(1)
                return "error"
        else:
            print('Search token ERROR!\n')
            # exit(1)
            return "error"
    print("ERROR! 过一会儿再试试吧...\n")
    # exit(3)


def getCourseTable(choice=0):
    """
    获取课表
    :param choice: 0 for std, 1 for class.个人课表or班级课表，默认为个人课表。
    :return:courseTable: {Response} 课表html响应
    """
    time.sleep(0.3)  # fix Issue #2 `Too Quick Click` bug
    courseTableResponse = session.get(host + '/eams/courseTableForStd.action')
    # logging.debug(courseTableResponse.text)

    temp_ids_match = re.compile(r"bg\.form\.addInput\(form,\"ids\",\"([0-9]*)\"")
    temp_ids = temp_ids_match.findall(courseTableResponse.text)
    if temp_ids:
        logging.debug(temp_ids)  # [0] for std, [1] for class.

        # postData_course = {
        #     "ignoreHead": "1",
        #     "setting.kind": "std",
        #     "startWeek": "",
        #     "project.id": "1",
        #     "semester.id": "62",
        #     "ids": "xxxxx"
        # }

        if choice == 1:  # 班级课表
            ids = temp_ids[1]
            kind = "class"
        else:  # 个人课表   choice == 0
            ids = temp_ids[0]
            kind = "std"

        courseTable_postData = {
            # "ignoreHead": "1",
            "setting.kind": kind,
            # "startWeek": "",  # None for all weeks
            # "project.id": "1",
            # "semester.id": session.cookies.get_dict()['semester.id'],
            "ids": ids
        }
        courseTable = session.get(host + r'/eams/courseTableForStd!courseTable.action',
                                  params=courseTable_postData)
        # courseTable = session.post(host + '/eams/courseTableForStd!courseTable.action',
        #                            data=courseTable_postData)

        # logging.debug(courseTable.text)
        # logging.debug(session.cookies.get_dict())
        return courseTable
    else:
        print("Get ids ERROR!")
        exit(4)


def parseCourseTable(courseTable):
    """
    解析课表
    :param courseTable: {Response} 课表html响应
    :return: list_lessonObj: {list} 由Lesson类构成的列表
    """
    soup = BeautifulSoup(courseTable.text.encode('utf-8'), 'lxml')

    """personal info"""
    personalInfo = soup.select('div#ExportA > div')[0].get_text()
    logging.debug(personalInfo)  # DEBUG
    stuClass = re.findall(r'(所属班级|班级名称):\s*([A-Za-z\d]*)', personalInfo)[0]  # 个人课表为`所属班级`，班级课表为`班级名称`
    print('班级:' + stuClass[1])
    practiceWeek = re.findall(r'实践周：\s*(.*)', personalInfo, re.DOTALL)[0]
    practiceWeek = "".join(practiceWeek.split())
    print('实践周:' + practiceWeek)

    courseTable_JS = soup.select('div#ExportA > script')[0].get_text()
    # logging.debug(courseTable_JS)
    list_courses = courseTable_JS.split('var teachers =')

    """Regex"""
    re_teachers = re.compile(r'actTeachers\s*=\s*\[(.+)];')
    re_singleTeacher = re.compile(r'({.+?})')
    re_courseInfo = re.compile(
        r'actTeacherName\.join\(\',\'\),\s*(.*),\s*(.*),\s*(.*),\s*(.*),\s*(.*),\s*(.*),\s*(.*),\s*(.*),\s*(.*),\s*(.*)\s*,\s*(.*)\s*\)')
    # courseId,courseName,roomId,roomName,vaildWeeks,taskId,remark,assistantName,experiItemName,schGroupNo,teachClassName
    re_courseTime = re.compile(r'index\s*=\s*(\d+)\s*\*\s*unitCount\s*\+\s*(\d+);')

    list_lessonObj = []  # Initialization
    course_cnt = 1
    for singleCourse in list_courses[1:]:
        print('No.{} course: '.format(course_cnt))

        logging.info('Parsing teacher(s)...')
        list_teacher = []
        teachers = re_teachers.findall(singleCourse)
        if len(teachers) == 0:  # fix teacher not specified bug
            list_teacher = []
        else:
            teacher = re_singleTeacher.findall(teachers[0])
            if len(teacher) > 1:  # More than 1 teachers
                for teacher_i in teacher:
                    teacher_i = teacher_i.replace('id', '\"id\"').replace('name', '\"name\"').replace('lab', '\"lab\"')
                    list_teacher.append(json.loads(teacher_i))
            else:  # Single teacher
                teacher = teacher[0].replace('id', '\"id\"').replace('name', '\"name\"').replace('lab', '\"lab\"')
                list_teacher.append(json.loads(teacher))
        logging.info(list_teacher)

        logging.info('Parsing course info...')  # DEBUG
        courseInfo = re_courseInfo.search(singleCourse, re.DOTALL | re.MULTILINE)
        logging.debug(courseInfo)

        logging.info('Parsing course time...')  # DEBUG
        courseTime = re_courseTime.findall(singleCourse)
        logging.info(courseTime)

        new_lessonObj = Lesson(list_teacher, courseInfo, courseTime)
        # 把课程的全部信息都传给Lesson，在初始化时进行具体信息的匹配，后续有改动直接在Lesson类里面改就完事了
        """Print info"""
        print(new_lessonObj)
        list_lessonObj.append(new_lessonObj)

        course_cnt += 1
        print()
    return list_lessonObj