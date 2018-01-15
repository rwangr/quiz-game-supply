# Quiz Game Supply

这个脚本能够通过截屏和调用百度运OCR文字识别接口，获得题目和答案选项文本，通过主流搜索平台检索题目，获得答案选项词频统计，最后推荐词频最高的选项。正常情况下，整个过程每题耗时约3~4秒。

运行脚本前，需要将手机屏幕投射到电脑上，以供截屏。测试时是通过macOS自带的Quick Player的影片录制功能，将iPhone的屏幕投射到桌面。由于全屏幕截屏是调用了macOS系统命令，因此脚本暂时仅支持Mac。

## 配置运行环境
克隆Repo到本地，并定位到这个文件夹：
```sh
$ git clone https://github.com/rwangr/quiz-game-supply.git
$ cd ./quiz-game-supply
```
准备好Python 3.x运行环境。如果使用conda，可直接使用文件environment.txt创建新环境：
```sh
$ conda create --name <ENV_NAME> --file environment.txt
$ source activate <ENV_NAME>
```
用pip安装文件requirement.txt里的依赖库：
```sh
$ pip install --requirement requirement.txt --yes
```

## 配置百度云OCR
准备百度云账号。在 控制台 > 产品服务 > 文字识别 中创建应用，并获得应用的AppID, API Key和Secret Key。 

用获得的AppID, API Key和Secret Key修改配置文件secret.ini.template，**并将文件重命名为secret.ini**：
```sh
[BAIDU_OCR]
# BAIDU_OCR OCR Configuration
# NO quote needed around value
# Rename this file as secret.ini after modification
APP_ID = <YOUR_APP_ID>
API_KEY = <YOUR_API_KEY>
SECRET_KEY = <YOUR_SECRET_KEY>
```
## 调整截图区域
在文件```main.py```中，变量```QUIZ_APPS```用于配置游戏应用名、答案选项数量、截图裁剪区域和模糊区域。
```
QUIZ_APPS=[
{'app_name':'冲顶大会',
 'answer_count':3,
 'crop_area':(45,190,450,580), #iPhone 6,6s,7 on 1440*900 display resolution Mac
 'mask_area':[]},

{'app_name':'芝士超人',
 'answer_count':3,
 'crop_area':(24,120,470,500), #iPhone 6,6s,7 on 1440*900 display resolution Mac
 'mask_area':[]},

{'app_name':'头脑王者',
 'answer_count':4,
 'crop_area':(65,250,430,810), #iPhone 6,6s,7 on 1440*900 display resolution Mac
 'mask_area':[(25,435,85,465),(410,435,470,465)]} #iPhone 6,6s,7 on 1440*900 display resolution Mac
]
```
其中：
- ```'app_name'```指定应用显示名称，用于多个应用选择；
- ```'answer_count'```指定答案选项数量；
- ```'crop_area'```指定截图裁剪区域，裁剪区域需要包含题目和答案选项，且尽可能排除不相关文字干扰。前（后）两个数字代表裁剪起（终）点横纵坐标；
- ```'mask_area'```指定截图模糊区域，对于无法通过裁剪排除的不相关文字，需要模糊处理，以保证脚本能正确处理。用法同```'crop_area'```，支持指定多个模糊区域。

## 运行
运行文件```main.py```，并按照提示输入。在题目出现后，按[Enter]开始，稍后可以看到识别和检索统计结果。
```sh
$ python main.py
```
