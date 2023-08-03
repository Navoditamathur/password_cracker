import hashlib
from itertools import permutations, combinations
import datetime

from config import *

def crack_pwd(user_name, detailed=False):
    start_time = datetime.datetime.now()
    user_found = False
    msg = ""
    pwd_strength = "Strong"
    with open(auth_list) as f:
        for line in f:
            if line.split("\t")[0] == user_name:
                user_found = True
                hash_pwd = line.split("\t")[1].strip()
                break
    if not user_found:
        msg = "User with" + user_name + " does not exist"
    else:
        with open(dictionary) as dict:
            words = set(word.strip().lower() for word in dict)
            for word in words:
                hash_word = hashlib.md5(word.encode()).hexdigest()
                if hash_pwd == hash_word:
                    pwd_strength = "Weak"
                    end_time = datetime.datetime.now()
                    return [True, word, pwd_strength, end_time - start_time]
            for word in words:
                if detailed:
                    match_found = match_all_possible_passwords(word, hash_pwd)
                else:
                    match_found = match_possible_passwords(word, hash_pwd)
                if match_found[0]:
                    pwd_strength = "Moderate"
                    end_time = datetime.datetime.now()
                    return [True, match_found[1], pwd_strength, end_time - start_time]
    end_time = datetime.datetime.now()
    return [False, False, pwd_strength, end_time - start_time, msg]


def match_all_possible_passwords(word, hash_pwd):
    total_chars_allowed = total_extra_chars_allowed + 1
    for i in range(total_chars_allowed):
        for j in range(total_chars_allowed):
            if i == 0 and j == 0:
                continue
            for num in combinations(nums, i):
                for char in combinations(special_chars, j):
                    possible_pwd = word
                    for c in list(char):
                        possible_pwd += c
                    for n in list(num):
                        possible_pwd += n
                    for p in permutations(possible_pwd):
                        possible_pwd_hash = hashlib.md5(''.join(p).encode()).hexdigest()
                        if hash_pwd == possible_pwd_hash:
                            return [True, ''.join(p)]
    return [False, False]

def match_possible_passwords(word, hash_pwd):
    total_chars_allowed = total_extra_chars_allowed + 1
    for i in range(total_chars_allowed):
        for j in range(total_chars_allowed):
            if i == 0 and j == 0:
                continue
            for num in combinations(nums, i):
                for char in combinations(special_chars, j):
                    possible_pwd = [word]
                    for c in list(char):
                        possible_pwd.append(c)
                    for n in list(num):
                        possible_pwd.append(n)
                    for p in permutations(possible_pwd):
                        possible_pwd_hash = hashlib.md5(''.join(p).encode()).hexdigest()
                        if hash_pwd == possible_pwd_hash:
                            return [True,''.join(p)]
    return [False, False]




