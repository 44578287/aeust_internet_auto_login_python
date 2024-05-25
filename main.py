import logging
import os
import re
import sys
import time
from datetime import datetime
from urllib.parse import urlparse

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# 禁用 InsecureRequestWarning 警告
urllib3.disable_warnings(InsecureRequestWarning)

# 获取当前脚本的绝对路径和所在目录
current_script_path = os.path.abspath(__file__)
current_script_directory = os.path.dirname(current_script_path)

# 配置日志路径
log_path = os.path.join(current_script_directory, 'log')
os.makedirs(log_path, exist_ok=True)
log_filename = os.path.join(log_path, f'{datetime.now().strftime("%Y-%m-%d-%H_%M_%S")}.log')

# 配置日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 创建文件处理器和控制台处理器
file_handler = logging.FileHandler(log_filename, encoding='utf-8')
console_handler = logging.StreamHandler()

# 设置处理器日志级别
file_handler.setLevel(logging.INFO)
console_handler.setLevel(logging.INFO)

# 创建日志格式器并添加到处理器
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 将处理器添加到日志记录器
logger.addHandler(file_handler)
logger.addHandler(console_handler)


class AEUST_Login:
    def __init__(self, username, password):
        self.__login_url = None
        self.__login_token = None
        self.__keepalive_url = None
        self.__keepalive_token = None
        self.__username = username
        self.__password = password

    def get_login_token(self):
        return self.__login_token

    def get_keepalive_token(self):
        return self.__keepalive_token

    @staticmethod
    def extract_html(html_body):
        match = re.search(r'window\.location="(.*?)";', html_body)
        if match:
            return match.group(1)
        return None

    def check_internet(self):
        try:
            response = requests.get("https://example.com/", verify=False)
        except requests.exceptions.ConnectionError as e:
            logger.warning("网络发生故障: " + str(e))
            return False

        self.__login_url = self.extract_html(response.text)
        if self.__login_url is None and response.status_code == 200:
            logger.debug("网络已连接")
            return True
        elif self.__login_url is not None:
            logger.info("网络尚未授权")
            return self.__login_url
        else:
            logger.warning("网络连接失败且无法获取连接Token")
            return False

    def login(self):
        if self.__login_url is None:
            logger.error("登入地址未初始化")
            return None

        self.__login_token = urlparse(self.__login_url).query
        logger.debug("登入检查Token: " + str(self.__login_token))

        login_response = requests.get(self.__login_url, verify=False)
        if login_response.status_code == 200:
            logger.debug("登入检查Token已生效: " + self.__login_token)

            login_url_parsed = urlparse(self.__login_url)
            login_response = requests.post(
                f"{login_url_parsed.scheme}://{login_url_parsed.hostname}:{login_url_parsed.port}/",
                data={
                    "magic": self.__login_token,
                    "username": self.__username,
                    "password": self.__password,
                    "submit": "确认"
                },
                verify=False
            )

            if login_response.status_code == 200:
                self.__keepalive_url = self.extract_html(login_response.text)
                if self.__keepalive_url is None:
                    logger.error("心跳地址提取失败")
                    #sys.exit(1)

                logger.info("登入成功: " + self.__username)
                logger.debug("心跳地址: " + self.__keepalive_url)
                self.__keepalive_token = urlparse(self.__keepalive_url).query
                return self.__keepalive_url
            else:
                logger.warning("登入请求失败")
        else:
            logger.warning("登入检查Token未生效")

        return None

    def keepalive(self):
        if self.__keepalive_url is None:
            logger.warning("心跳地址未初始化")
            return None

        return requests.get(self.__keepalive_url, verify=False)


if __name__ == '__main__':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

    logger.info("项目发布地址 @ https://445720.xyz and https://github.com/445782870")
    logger.info("ck小捷 QQ:2407896713 mail:g9964957@gmail.com")

    aeust_login = AEUST_Login("学号", "密码")

    while True:
        check_status = aeust_login.check_internet()
        if isinstance(check_status, str):
            aeust_login.login()
        elif check_status:
            logger.info("网络已连接")
            time.sleep(30)  # 休眠30秒后继续检查
        else:
            logger.warning("网络连接失败，将在10秒后重试...")
            time.sleep(10)  # 休眠10秒后重试
