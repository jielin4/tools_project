__author__ = "Jie Lin"
__date__ = "May 04, 2019"

import os
import sys
import json
# loading text


def load_text(path):
    f = open(path)
    word_lines = f.readlines()
    f.close()
    return [str(num.strip()) for num in word_lines]

# calculate lower/upper boundary and median


def lower(dataPoints):
    if not dataPoints:
        raise StatsError('no data points passed')
    sortedPoints = sorted(dataPoints)
    ind = round(len(sortedPoints) * 0.05)
    Q = sortedPoints[ind]
    return Q


def upper(dataPoints):
   # check the input is not empty
    if not dataPoints:
        raise StatsError('no data points passed')
    sortedPoints = sorted(dataPoints)
    ind = round(len(sortedPoints) * 0.95)
    Q = sortedPoints[ind]

    return Q


def median(lst):
    n = len(lst)
    if n < 1:
        return None
    if n % 2 == 1:
        return sorted(lst)[n//2]
    else:
        return sum(sorted(lst)[n//2-1:n//2+1])/2.0
# calculate lower/upper boundary and median for kid_safe parameter


def median2(dataPoints):
    list_ = []
    count = 0
    for i in dataPoints:
        if i > 0:
            list_.append(i)
    return median(list_)


def upper2(dataPoints):
    list_ = []
    count = 0
    for i in dataPoints:
        if i > 0:
            list_.append(i)
            count += 1
    return upper(list_)


def lower2(dataPoints):
    list_ = []
    count = 0
    for i in dataPoints:
        if i > 0:
            list_.append(i)
            count += 1
    return lower(list_)


def main_def():
    # loading word list
    bad = load_text('words/bad.txt')
    love = load_text('words/love.txt')
    positive = load_text('words/positive.txt')
    negative = load_text('words/negative.txt')
    common = load_text('words/common.txt')
    path = "Lyrics/"
    if len(sys.argv) > 1:
        if str(sys.argv[1])[-1] == '\\':
            path = str(sys.argv[1])
        else:
            print("Path is wrong, using the default path: Lyrics/")
            path = "Lyrics/"
    files = os.listdir(path)
    ch = []
    # read files
    for file in files:
        song = {}
        words_number, bad_words, love_words, common_words = 0, 0, 0, 0
        positive_words, negative_words = 0, 0
        info = file.strip(".txt").split("~")
        f = open(path+file, encoding="utf8")
        lyrics = f.readlines()
        f.close()
        for line in lyrics:
            words_list = line.strip("\n").split()
            words_number += len(words_list)
            # count word number
            for lst in words_list:
                if lst in bad:
                    bad_words += 1
                if lst in love:
                    love_words += 1
                if lst in positive:
                    positive_words += 1
                if lst in negative:
                    negative_words += 1
                if lst not in common:
                    common_words += 1
        safe_score = bad_words/words_number
        love_score = love_words / words_number
        mood_score = (positive_words - negative_words) / words_number
        length_score = words_number
        complexity_score = common_words/words_number
        song["id"] = int(info[0])
        song["artist"] = info[1].replace("-", " ")
        song["title"] = info[2].replace("-", " ")
        song["kid_safe"] = safe_score
        song["love"] = love_score
        song["mood"] = mood_score
        song["length"] = length_score
        song["complexity"] = complexity_score
        ch.append(song)
    # convert raw score to the scaled one for love,mood,length,complexity
    list_ = ['love', 'mood', 'length', 'complexity']
    for c in list_:
        temp = list(map((lambda i: i[c]), ch))
        temp2 = [(x-median(temp))/(upper(temp)-lower(temp))+0.5 for x in temp]
        scaled_score = [1 if x > 1 else 0 if x < 0 else x for x in temp2]
        for d in ch:
            d.update((k, round(scaled_score[ch.index(d)], 2))
                     for k, v in d.items() if k == c)
    # onvert raw score to the scaled one for kid_safe
    temp = list(map((lambda i: i['kid_safe']), ch))
    temp2 = [(x-median2(temp))/(upper2(temp)-lower2(temp)) +
             0.5 if x > 0 else x for x in temp]
    temp3 = [1-x for x in temp2]
    scaled_score = [1 if x > 1 else 0 if x < 0 else x for x in temp3]
    for d in ch:
        d.update((k, round(scaled_score[ch.index(d)], 2))
                 for k, v in d.items() if k == c)
    # output data

    result = {"characterizations": ch}
    output = json.dumps(result)
    return output


if __name__ == '__main__':
    output = main_def()
    name = "result.txt"
    f = open(name, 'w')
    f.write(output)
