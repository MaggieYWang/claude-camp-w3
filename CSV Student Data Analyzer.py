"""
CSV 学员数据分析器
功能：读取学员 CSV，统计总人数、各国人数、对赌完成率，并保存为 report.json
"""

import pandas as pd
import json
from pathlib import Path

FILENAME = Path(__file__).parent / "report.json"
CSV_PATH = Path(__file__).parent / "users_data.csv"

def save_report(report):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print("✅ 已保存至 report.json\n")

def print_menu():
    print("=" * 30)
    print("     学员数据分析器")
    print("=" * 30)
    print("1. 统计总人数")
    print("2. 统计各国人数")
    print("3. 统计对赌完成率")
    print("0. 退出")
    print("-" * 30)

def clean_data(df):
    # 数据清洗函数，返回清洗后的 DataFrame 和问题记录
    issues = []

    # 1. 处理邮箱为空
    missing_email = df['email'].isna() | (df['email'].str.strip() == "")
    if missing_email.any():
        missing_names = df.loc[missing_email, 'name'].tolist()
        issues.append(f"⚠️  以下学员邮箱为空，已填充占位符：{missing_names}")
        df.loc[missing_email, 'email'] = "unknown@placeholder.com"

    # 2. 统一日期格式
    def parse_date(date):
        try:
            return pd.to_datetime(date).strftime("%Y-%m-%d")
        except Exception:
            issues.append(f"⚠️  无法解析日期：{date}，已置为 NaT")
            return None

    df['joined_date'] = df['joined_date'].apply(parse_date)

    # 3. 统一国家名称大小写（首字母大写）
    df['country'] = df['country'].str.strip().str.title()

    # 4. 统一对赌状态大小写
    df['bet_status'] = df['bet_status'].str.strip().str.lower()

    return df, issues

# 加载 CSV
try:
    raw_data = pd.read_csv(CSV_PATH)
except FileNotFoundError:
    print("❌ 找不到 users_data.csv，请检查文件路径")
    exit()

# 清洗数据
data, issues = clean_data(raw_data.copy())

if issues:
    print("\n".join(issues))
    print()
else:
    print("✅ 数据校验通过，无异常\n")

# 加载历史报告
try:
    with open(FILENAME, "r", encoding="utf-8") as f:
        report = json.load(f)
        print(f"✅ 已加载最新统计结果")
except (FileNotFoundError, json.JSONDecodeError):
        report = {}

while True:
    print_menu()
    choice = input("请输入选项：").strip()  # .strip() 去除误输入的空格

    if choice == "1":
        print(f"\n学生总数为：{len(data)}\n")
        report["total_students"] = len(data)
        save_report(report)
    
    elif choice == "2":
        country_counts = data['country'].value_counts().reset_index()
        country_counts.columns = ['country', 'count']
        print(f"\n{country_counts.to_string(index=False)}\n")
        report["country_counts"] = country_counts.set_index('country')['count'].to_dict()
        save_report(report)
    
    elif choice == "3":
        number_completed = (data["bet_status"] == "completed").sum()
        completion_rate = number_completed / len(data)
        print("\n对赌完成率是", f"{completion_rate:.1%}", "\n")
        report["completion_rate"] = round(completion_rate, 4)
        save_report(report)
    
    elif choice == "0":
        print("再见！")
        break

    else:
        print("⚠️ 无效选项，请输入 0-3\n")  # 处理非法输入
            
