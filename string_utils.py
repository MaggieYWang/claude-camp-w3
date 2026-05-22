"""
字符串工具库
功能：反转单词顺序，统计元音字母数量，判断是否回文
"""

def reverse_words(user_input):
    words = user_input.strip().split()
    reversed_words = words[::-1]
    return " ".join(reversed_words)

def count_vowels(user_input):
    count = 0
    for letter in user_input:
        if letter in ["a", "e","i", "o", "u", "A", "E", "I", "O", "U"]:
            count = count +1
    return count

def is_palindrome(text):
    text_to_words = text.strip().split()
    if text_to_words == text_to_words[::-1]:
        return True
    else:
        return False

if __name__ == "__main__":
    user_input = str(input("请输入一段文字："))
    text = user_input.lower()
    print(f"反转单词顺序：{reverse_words(user_input)}")
    print(f"元音字母数量为{count_vowels(user_input)}")
    if is_palindrome(text):
        print("这段文字回文")
    else:
        print("这段文字不回文")