import pandas as pd
import json
from pathlib import Path

FILENAME = Path(__file__).parent / "report.json"
CSV_PATH = Path(__file__).parent / "users_data.csv"

def save_report(report):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print("✅ 已保存至 report.json\n")

# 加载 CSV
try:
    data = pd.read_csv(CSV_PATH)
except FileNotFoundError:
    print("❌ 找不到 users_data.csv，请检查文件路径")
    exit()

# 加载历史报告
try:
    with open(FILENAME, "r", encoding="utf-8") as f:
        report = json.load(f)
        print(f"✅ 已加载最新统计结果")
except (FileNotFoundError, json.JSONDecodeError):
        report = {}
print(report)

while True:
        print("=" * 30)
        print("     学员数据分析器")
        print("=" * 30)
        print("1. 统计总人数")
        print("2. 统计各国人数")
        print("3. 统计对赌完成率")
        print("0. 退出")
        print("-" * 30)
        choice = input("请输入选项：").strip()  # .strip() 去除误输入的空格

        if choice == "1":
            print("\n学生总数为：", len(data), "\n")
            report["total_students"] = len(data)
            save_report(report)
        
        elif choice == "2":
            country_counts = data['country'].value_counts().reset_index()
            country_counts.columns = ['country', 'count']
            print(f"\n{country_counts.to_string(index=False)}\n")
            report["country_counts"] = country_counts.set_index('country')['count'].to_dict()
            save_report(report)
        
        elif choice == "3":
            filtered_data = data[data["bet_status"]== "completed"]
            number_completed = len(filtered_data)
            completion_rate = number_completed / len(data)
            print("\n对赌完成率是", f"{completion_rate:.1%}", "\n")
            report["completion_rate"] = completion_rate
            save_report(report)
        
        elif choice == "0":
            print("再见！")
            break

        else:
            print("⚠️ 无效选项，请输入 0-3\n")  # 处理非法输入
            
