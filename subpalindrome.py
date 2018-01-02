# Viraj's solution
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes
# a string as input and returns the i and j indices that
# correspond to the beginning and end indices of the longest
# palindrome in the string.
#
# Grading Notes:
#
# You will only be marked correct if your function runs
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!


def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    text = text.upper()
    txtLength = len(text)
    x, y = 0, 0
    nx, ny = 0, 0
    if(txtLength == 0):
        return x, y
    for i, c in enumerate(text):
        if((i + 1) < txtLength and c == text[i + 1]):
            # print('right')
            nx, ny = longer_palindrome(text, i, i + 1, min(i, txtLength - (i + 1 + 1)))
            if(nx < x or ny > y):
                x, y = nx, ny
        if(i != 0 and c == text[i - 1]):
            # print('left')
            nx, ny = longer_palindrome(text, i - 1, i, min(i - 1, txtLength - (i + 1)))
            if(nx < x or ny > y):
                x, y = nx, ny
        if((i + 1) < txtLength and i != 0 and text[i + 1] == text[i - 1]):
            # print('both')
            nx, ny = longer_palindrome(text, i - 1, i + 1, min(i - 1, txtLength - (i + 1 + 1)))
            if(nx < x or ny > y):
                x, y = nx, ny
        if((y - x + 1) == txtLength):
            break
    # print('x={}, y={}'.format(x, y + 1))
    return x, (y + 1)


def longer_palindrome(text, start, end, remaining):
    # print('start={}, end={}, rem={}'.format(start, end, remaining))
    for i in range(1, remaining + 1):
        left = text[start - 1]
        right = text[end + 1]
        if(left != right):
            return start, end
        start = start - 1
        end = end + 1
    return start, end


def test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8, 21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    assert L('a') == (0, 1)
    assert L('detartrated') == (0, 11)
    return 'tests pass'


print(test())
