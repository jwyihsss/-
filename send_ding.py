#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import time
import datetime
from utils import *

import jenkins
import urllib3
from utils.mock_data.fake_data_control import Mock
from dingtalkchatbot.chatbot import DingtalkChatbot

url = config.jenkins.url
user = config.jenkins.user
password = config.jenkins.pwd
project_name = config.jenkins.project
mapping_url = config.jenkins.mapping_url
robot_webhook = config.ding_talk.webhook


class JenkinsContent:
    """获取Jenkins构建信息的类"""

    def __init__(self):
        urllib3.disable_warnings()
        # jenkins的IP地址
        self.jenkins_url = mapping_url
        # jenkins用户名和密码
        self.server = jenkins.Jenkins(self.jenkins_url, username=user, password=password)

    def jenkins_content_info(self):
        """获取Jenkins构建相关信息"""

        result_job = self.server.get_jobs()
        # jobs_name = result_job[0]["name"]
        job_name = project_name
        job_url = self.server.get_job_info(job_name)['url'].replace(url, mapping_url)
        job_last_number = self.server.get_job_info(job_name)['lastBuild']['number']
        job_result = self.server.get_build_info(job_name, job_last_number)['result']
        report_url = job_url + str(job_last_number) + '/allure'
        return result_job, job_name, job_url, job_last_number, report_url, job_result


class SendDingTalk(JenkinsContent):
    """发送钉钉通知的类"""

    def __init__(self):
        super().__init__()
        self.result_job, self.job_name, self.job_url, self.job_last_number, self.report_url, self.job_result = self.jenkins_content_info()

    def send_ding(self):
        content = {}
        file_path = root / 'allure-report/export/prometheusData.txt'
        f = open(file_path)
        for line in f.readlines():
            launch_name = line.strip('\n').split(' ')[0]
            num = line.strip('\n').split(' ')[1]
            content.update({launch_name: num})
        f.close()
        passed_num = content['launch_status_passed']  # 通过数量
        failed_num = content['launch_status_failed']  # 失败数量
        broken_num = content['launch_status_broken']  # 阻塞数量
        skipped_num = content['launch_status_skipped']  # 跳过数量
        case_num = content['launch_retries_run']  # 总数量
        run_duration = content['launch_time_duration']
        print(self.job_result)
        job_result = {
            "SUCCESS": '成功',
            'FAILURE': '失败',
            'ABORTED': '中止',
            'UNSTABLE': '悬挂'
        }[self.job_result]
        json_path = root / 'allure-report/widgets/summary.json'
        with open(json_path) as f:
            res = json.load(f)
        today = str(datetime.date.today())
        s = time.localtime(res['time']['start'] / 1000)
        report_time = time.strftime("%Y-%m-%d", s)

        if report_time == today:
            text = f'### **{self.job_name}接口自动化通知**\n' \
                   f"**Jenkins构建结果: {job_result}**\n\n" \
                   f"**测试环境: 线上环境**\n\n" \
                   f"**时间: {Mock('now_time')()}**\n\n" \
                   "------------\n\n" \
                   f"### **执行结果**\n\n" \
                   f"**成功率: <font color='#00dd00'>{round(int(passed_num) / int(case_num) * 100)}%</font>**\n\n" \
                   f"**总用例数: <font color='#0000FF'>{case_num}</font>**\n\n" \
                   f"**成功用例数: <font color='#008000'>{passed_num}</font>**\n\n" \
                   f"**失败用例数: <font color='#FF0000'>{failed_num}</font>**\n\n" \
                   f"**异常用例数: <font color='#FF0000'>{broken_num}</font>**\n\n" \
                   f"**跳过用例数: <font color='#FFA500'>{skipped_num}</font>**\n\n" \
                   f"**本次执行耗时: {round(int(run_duration) / 1000)}秒**\n\n" \
                   "------------\n\n" \
                   f"**测试报告:** [点击查看]({self.report_url}) \n\n" \
                   f"**测试地址:** {config.host} \n"

        else:
            text = f'### **{self.job_name}自动化通知**\n' \
                   f"**Jenkins构建结果: {job_result}**\n\n" \
                   "------------\n\n" \
                   f"**失败原因: <font color='#FF0000'>网络或代理已断开</font>**\n\n" \
                   "------------\n\n" \
                   f"**构建日志:** [点击查看]({self.job_url + str(self.job_last_number) + '/console'}) \n"

        title = f'接口自动化通知'
        send_msg = DingtalkChatbot(webhook=robot_webhook)
        send_msg.send_markdown(title=title,
                               text=text,
                               is_at_all=True)


if __name__ == '__main__':
    SendDingTalk().send_ding()



