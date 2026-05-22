from string_utils import reverse_words,  count_vowels, is_palindrome

def test_reverse_words():
    assert reverse_words("hello world") == "world hello"
    assert reverse_words("Hello world") == "world Hello"
    assert reverse_words("hello world!") == "world! hello"
    assert reverse_words("hello") == "hello"
    assert reverse_words("       ") == ""
    assert reverse_words("123") == "123"

def test_count_vowels():
    assert count_vowels("hello world") == 3
    assert count_vowels("hEllo world") == 3
    assert count_vowels("hll wrld") == 0
    assert count_vowels("") == 0

def test_is_palindrome():
    assert is_palindrome("hello world") == False
    assert is_palindrome("hello world hello") == True
    assert is_palindrome("hello") == True
    assert is_palindrome("") == True