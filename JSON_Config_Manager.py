"""
JSON 配置文件读写器
功能：读取config.json，修改设置，修改后保存回config.json
"""

import json
from pathlib import Path

FILENAME = Path(__file__).parent / "config.json"

DEFAULT_CONFIG = {
    "theme": "system",
    "language": "zh-CN",
    "font_size": 10,
    "font_colour": "#333333",
    "auto_save": True,
    "auto_save_interval": 5,
    "date_format": "YYYY-MM-DD"
}

LABELS = {
    "theme": "主题",
    "language": "语言",
    "font_size": "字体大小",
    "font_colour": "字体颜色",
    "auto_save": "自动保存",
    "auto_save_interval": "自动保存间隔",
    "date_format": "日期格式"
}

RULES = {
    "theme": {"type": str, "choices": ["light", "dark", "system"]},
    "language": {"type": str, "choices": ["zh-CN", "en-UK", "en-US", "ja-JP"]},
    "font_size": {"type": int, "min": 8, "max": 32},
    "font_colour": {"type": str},
    "auto_save": {"type": bool, "choices": ["true", "false"]},
    "auto_save_interval": {"type": int, "min": 1, "max": 300},
    "date_format": {"type": str, "choices": ["YYYY-MM-DD", "DD/MM/YYYY", "MM/DD/YYYY"]}
}

def print_menu():
    print("=" * 30)
    print("     JSON 配置文件读写器")
    print("=" * 30)
    print("请选择你要修改的设置：")
    for i, option in enumerate(LABELS, start=1):
        print(f"{i}. {LABELS[option]}")
    print("0. 退出")
    print("-" * 30)

def load_config():
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            configuration = json.load(f)
        print("✅ 已加载用户偏好设置")
    except (FileNotFoundError, json.JSONDecodeError):
        configuration = DEFAULT_CONFIG.copy()
    return configuration

def save_config(configuration):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(configuration, f, ensure_ascii=False, indent=2)
    print("✅ 已保存到本地")

def validate(option, value):
    rule = RULES[option]

    if "choices" in rule:
        if value.lower() not in rule["choices"]:
            print(f"❌ 无效输入，只能是：{' / '.join(rule['choices'])}")
            return False

    if rule["type"] == int:
        if not value.isdigit():
            print("❌ 请输入整数")
            return False
        value = int(value)
        if "min" in rule and value < rule["min"]:
            print(f"❌ 不能小于 {rule['min']}")
            return False
        if "max" in rule and value > rule["max"]:
            print(f"❌ 不能大于 {rule['max']}")
            return False

    return True

def main(config):
    keys = list(LABELS.keys())
    while True:
        print_menu()
        choice = input("请输入你的选项：")

        if choice == "0":
            print("再见！")
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(keys):
            option = keys[int(choice) - 1]
            preference = input(f"请输入新的{LABELS[option]}：")
            if not validate(option, preference):
                print("请重新选择")
            else:
                rule = RULES[option]
                if rule["type"] == bool:
                    config[option] = preference.lower() == "true"
                elif rule["type"] == int:
                    config[option] = int(preference)
                else:
                    config[option] = preference
                save_config(config)
        else:
            print("输入有误，请重新输入")

if __name__ == "__main__":
    config = load_config()
    main(config)