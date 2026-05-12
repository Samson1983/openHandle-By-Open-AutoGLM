# openHandle-by-Open-AutoGLM

[Readme in English](README_en.md)

<div align="center">
<img src=README.assets/openHandle-logo.png width="20%"/>
<img src=resources/logo.svg width="20%"/>
</div>
<p align="center">
👋 Join us on WeChat: hzfaic</a>
</p>



## Project Introduction

OpenHandle-by-Open-AutoGLM adds a blehttp module to the phone_agent directory. It adapts the interfaces provided by esp32c3 to Open-AutoGLM; other aspects remain unchanged.

The esp32c3 firmware can replace the capabilities of ADB (Android Debug Bridge) to control the device.

The app provides screen awareness for large models through screenshots. The agent can automatically parse intent, understand the current interface, plan the next action, and complete the entire process. The system also has a built-in sensitive operation confirmation mechanism and supports manual intervention in login or CAPTCHA scenarios.

> ⚠️

> This project is for research and learning purposes only. It is strictly prohibited to use it for illegally obtaining information, interfering with the system, or any illegal activities. Please carefully review the [Terms of Use](resources/privacy_policy.txt).

## Design Principle Diagram

<img src="README.assets/openHand-by-openAutoGLM%E9%80%BB%E8%BE%91%E5%9B%BE.png" alt="openHand-by-openAutoGLM Logic Diagram" style="zoom: 80%;" />

## Usage Steps:

1. First, download openHandle-By-Open-AutoGLM (open source).

2. If you have ESP32C3 hardware, download the SDK and flash it, or purchase the hardware directly;

3. Install the APK (open source) on your phone;

4. Connect and control it: Demo available;

## Quick Installation

## PC Environment Preparation

### 1. Python Environment

Python 3.10 or later is recommended.

### 2. Open the project using an IDE: such as PyCharm

### 3. Create a virtual environment

Open the command-line terminal:

![image-20260512162400208](README.assets/image-20260512162400208.png)

Type: `python -m venv .venv`

### 4. Enter the environment

Type: .venv\Scripts\activate.bat`

### 5. Install Python project dependencies

### Install dependencies

```bash
pip install -r requirements.txt

pip install -e .

```

## Startup command:

Example:
```shell
python main.py --base-url https://open.bigmodel.cn/api/paas/v4 --model "autoglm-phone" --apikey `"bcc5e3d20b2d4ff0ba9fc02f5b5197f8.TIVV4c4K20BCCEEB" --device-type blehttp --blehttp-url http://192.168.2.99:9123 "Open Meituan and search for the nearest hot pot restaurant"

`python main.py --base-url https://open.bigmodel.cn/api/paas/v4 --model "autoglm-phone" --apikey "bcc5e3d20b2d4ff0ba9fc02f5b5197f8.TIVV4c4K20BCCEEB" --device-type blehttp --blehttp-url http://192.168.2.99:9123 "Open Soda Music"

`python main.py --base-url https://open.bigmodel.cn/api/paas/v4 --model "autoglm-phone"` --apikey "bcc5e3d20b2d4ff0ba9fc02f5b5197f8.TIVV4c4K20BCCEEB" --device-type blehttp --blehttp-url http://192.168.2.99:9123 "Open Meituan to order a bottle of shampoo and get a notification to place the order"

python main.py --base-url https://open.bigmodel.cn/api/paas/v4 --model "autoglm-phone" --apikey "bcc5e3d20b2d4ff0ba9fc02f5b5197f8.TIVV4c4K20BCCEEB" --device-type blehttp --blehttp-url http://192.168.2.99:9123 "Buy a 15-yuan ticket on Taobao Tickets" This afternoon, I watched "Cold War 1994" at the Qin Cheng Li Cinema, in a middle seat, with a single meal of Coke and popcorn. I'm currently on the order page.


### Device Compatibility Instructions:

#### Phone Button and Slide Adaptation: See device_config.json configuration


``` General Bluetooth Button Values:

* 0xB0 = Home (Home Page)

* 0xB1 = Back (Back)

* 0xB3 = Recent Apps (Recent Tasks / Multitasking)

Slide to Implement Button Effect:

/home interface: (Home Page)

/back interface: (Back)

/recents: (Recent Tasks / Multitasking)


Currently, only the following models have been tested:

| Operation Method | Phone Model | Operating System |

| -------- | --------------- | ---------- |

| Button | Redmi Truo3 | android_16 |

| Slide | Redmi Note Pro9 | android_12 |

| | | |

More device models will be supported later;

---

## Debugging Instructions

### Model Configuration

```python
from phone_agent.model import ModelConfig

config = ModelConfig(
base_url="http://localhost:8000/v1",

api_key="EMPTY", # API key (if needed)

model_name="autoglm-phone-9b", # Model name

max_tokens=3000, # Maximum number of output tokens

temperature=0.1, # Sampling temperature

frequency_penalty=0.2, # Frequency penalty

```

### Agent Configuration

```python
from phone_agent.agent import AgentConfig

config = AgentConfig(
max_steps=100, # Maximum number of steps per task

device_id=None, # ADB device ID (None for automatic detection)

lang="cn", # Language Selection: cn (Chinese) or en (English)

verbose=True, # Print debugging information (including thought process and actions)

```

### Verbose Mode Output

When `verbose=True`, the Agent will output detailed information at each step:

```

===================================================

💭 Thought Process:

--------------------------------------------------
Currently on the system desktop, the Xiaohongshu app needs to be launched first.

--------------------------------------------------

🎯 Actions:

{
"_metadata": "do",

"action": "Launch",

"app": "Xiaohongshu"

==================================================

... (Continue to the next step after performing the action)

===================================================

💭 Thought Process:

--------------------------------------------------
Xiaohongshu is open, now you need to click the search box

--------------------------------------------------

🎯 Perform Action:

{
"_metadata": "do",

"action": "Tap",

"element": [500, 100]

}
===================================================

🎉 ==================================================

✅ Task Completed: Successfully searched for food guides

========================================================

```

This allows you to clearly see the AI's reasoning process and the specific operations at each step.

## Supported Applications

### Android Applications

Phone Agent supports 50+ mainstream Chinese applications:

| Categories | Applications |

|------|-----------------|

| Social Communication | WeChat, QQ, Weibo |

| E-commerce Shopping | Taobao, JD.com, Pinduoduo |

| Food Delivery | Meituan, Ele.me, KFC |

| Travel | Ctrip, 12306, Didi Chuxing |

| Video Entertainment | bilibili, Douyin, iQiyi |

| Music & Audio | NetEase Cloud Music, QQ Music, Himalaya |

| Lifestyle Services | Dianping, Gaode Map, Baidu Map |

| Content Communities | Xiaohongshu, Zhihu, Douban |

Run `python main.py --list-apps` to view the complete list.

## Available Operations

The Agent can perform the following operations:

| Operation | Description |

|--------------|-----------------|

| `Launch` | Launch the application |

| `Tap` | Tap a specified coordinate |

| `Type` | Enter text |

| `Swipe` | Swipe the screen |

| `Back` | Return to the previous page |

| `Home` | Return to the home screen |

| `Long Press` | Long press |

| `Double Tap` | Double tap |

| `Wait` | Wait for the page to load |

| `Take_over` | Request manual intervention (login/verification code, etc.) |

## Frequently Asked Questions

We have listed some common problems and their corresponding solutions:

### Screenshot Failure (Black Screen)

This usually means that the application is displaying a sensitive page (payment, password, banking applications). The Agent will automatically detect Test and request manual intervention.