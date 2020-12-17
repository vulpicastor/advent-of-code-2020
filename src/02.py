def parse_policy(policy):
    occurrence, letter = policy.split()
    low, high = occurrence.split('-')
    low = int(low)
    high = int(high)
    return low, high, letter

def check_policy(low, high, letter, s):
    occurrence = s.count(letter)
    if low <= occurrence <= high:
        return True
    return False

def check_policy_two(low, high, letter, s):
    if (s[low-1] == letter) != (s[high-1] == letter):
        return True
    return False

def check_line(l, func):
    policy, s = l.split(': ')
    s = s.strip()
    return func(*parse_policy(policy), s)

def main():
    with open('input/02.txt') as f:
        lines = f.readlines()
    print(sum(map(lambda s: check_line(s, check_policy), lines)))
    print(sum(map(lambda s: check_line(s, check_policy_two), lines)))

main()
