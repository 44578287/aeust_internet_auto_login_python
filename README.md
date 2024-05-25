# AEUST 登录脚本

该Python脚本旨在为AEUST用户管理网络认证并保持活跃的互联网连接。它包括登录网络、保持连接和详细记录操作与错误的功能。
## 目录 
1. [功能](https://chatgpt.com/c/39acb7ea-a702-4b72-922f-9afcc729ede1#%E5%8A%9F%E8%83%BD) 
2. [设置](https://chatgpt.com/c/39acb7ea-a702-4b72-922f-9afcc729ede1#%E8%AE%BE%E7%BD%AE) 
3. [使用方法](https://chatgpt.com/c/39acb7ea-a702-4b72-922f-9afcc729ede1#%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95) 
4. [类和方法](https://chatgpt.com/c/39acb7ea-a702-4b72-922f-9afcc729ede1#%E7%B1%BB%E5%92%8C%E6%96%B9%E6%B3%95) 
5. [日志记录](https://chatgpt.com/c/39acb7ea-a702-4b72-922f-9afcc729ede1#%E6%97%A5%E5%BF%97%E8%AE%B0%E5%BD%95) 
6. [错误处理](https://chatgpt.com/c/39acb7ea-a702-4b72-922f-9afcc729ede1#%E9%94%99%E8%AF%AF%E5%A4%84%E7%90%86)
## 功能 
- 禁用 `urllib3` 的 `InsecureRequestWarning`。
- 详细记录脚本执行和错误信息。
- 从HTML响应中提取并使用登录令牌和URL。
- 通过定期发送请求保持活跃的网络连接。
## 设置 
1. **安装所需库** 

使用pip安装所需的Python库：

```sh
pip install requests urllib3
``` 
2. **准备环境** 

确保脚本具有在其目录中创建和写入日志文件的必要权限。
## 使用方法 
1. **运行脚本** 

使用Python执行脚本：

```sh
python main.py
```



脚本将：
- 检查网络是否连接。
- 如果网络未连接，将尝试使用提供的用户名和密码登录。
- 登录成功后，定期发送请求以保持连接。
## 类和方法
### `AEUST_Login`
#### `__init__(self, username, password)`
- 使用给定的用户名和密码初始化登录对象。
#### `get_login_token(self)`
- 返回当前的登录令牌。
#### `get_keepalive_token(self)`
- 返回当前的保持连接令牌。
#### `extract_html(html_body)`
- 使用正则表达式从给定的HTML内容中提取并返回URL。
#### `check_internet(self)` 
- 通过发送GET请求到“[https://example.com/”来检查网络是否连接。]() 
- 如果网络已连接，返回 `True`。
- 如果网络需要认证，返回登录URL。 
- 如果网络连接失败，返回 `False`。
#### `login(self)`
- 尝试使用提取的登录URL和提供的凭证登录网络。
- 如果登录成功，返回保持连接URL。
- 如果登录失败，记录错误和警告信息。
#### `keepalive(self)`
- 发送GET请求到保持连接URL以维持网络连接。
- 返回保持连接请求的响应。
## 日志记录

脚本在 `log` 目录中创建一个带时间戳的日志文件。它以不同级别（INFO、WARNING、ERROR、DEBUG）记录信息： 
- **INFO** ：有关脚本进度和操作的一般信息。 
- **WARNING** ：可能需要注意的非关键问题。 
- **ERROR** ：阻止脚本正常运行的关键问题。 
- **DEBUG** ：有助于调试的详细信息。

日志消息同时打印到控制台并写入日志文件。
## 错误处理

脚本包括多个错误处理机制以确保稳健性： 
- **连接错误** ：检查互联网连接时捕获并记录连接错误。 
- **无效令牌** ：检查登录和保持连接令牌是否有效，并记录适当的消息。 
- **重试** ：如果网络连接失败，实施带延迟的重试机制。
## 示例日志消息

```plaintext
2024-05-25 10:00:00 - INFO - 项目发布地址 @ https://445720.xyz 和 https://github.com/445782870
2024-05-25 10:00:00 - INFO - ck小捷 QQ:2407896713 邮箱:g9964957@gmail.com
2024-05-25 10:00:30 - INFO - 网络已连接
2024-05-25 10:01:00 - WARNING - 网络连接失败，将在10秒后重试...
2024-05-25 10:01:10 - INFO - 网络已连接
```



脚本记录关于项目和作者的初始消息，随后是有关网络连接状态和遇到的错误的状态更新。

通过遵循设置和使用方法，用户可以确保可靠的网络连接，并具备详细的日志记录和错误处理功能。
