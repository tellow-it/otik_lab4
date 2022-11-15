import itertools
import collections
import re
import math

f = 'task1.txt'


def read_byte(filename):
    with open(filename, 'rb') as file:
        text = file.read().hex()
        return text


def length_x(filename):
    text = read_byte(filename)
    return int(len(text) / 2)


def numbers_ai_aj(filename):
    text = read_byte(filename)
    list_elements = list(set([text[i:i + 2] for i in range(0, len(text), 2)]))
    combinations_el = list(itertools.permutations(list_elements, 2))
    for el in [(x, x) for x in list_elements]:
        combinations_el.append(el)
    sum_comb_el = [x[0] + x[1] for x in combinations_el]
    counter_dict = collections.Counter()

    for aj_ai in sum_comb_el:
        counter_dict[aj_ai] = len(re.findall(aj_ai, text))
    return counter_dict


def numbers_aj(filename):
    text = read_byte(filename)
    list_elements = list(set([text[i:i + 2] for i in range(0, len(text), 2)]))
    counter_dict = numbers_ai_aj(filename)
    counter_aj_dict = collections.Counter()
    for el in list_elements:
        for key in counter_dict.keys():
            if el == key[:2]:
                counter_aj_dict[el] += counter_dict[key]
    return counter_aj_dict


def p_ai(filename):
    text = read_byte(filename)
    list_elements = [text[i:i + 2] for i in range(0, len(text), 2)]
    counter_ai_dict = collections.Counter(list_elements)
    dict_p_ai = dict()
    for key in counter_ai_dict.keys():
        dict_p_ai[key] = round(counter_ai_dict[key] / length_x(f), 4)
    return dict_p_ai


def p_ai_aj(filename):
    text = read_byte(filename)
    list_elements = list(set([text[i:i + 2] for i in range(0, len(text), 2)]))
    combinations_el = list(itertools.permutations(list_elements, 2))
    counter_ai_aj = numbers_ai_aj(filename)
    for key in counter_ai_aj.keys():
        counter_ai_aj[key] = round(counter_ai_aj[key] / length_x(filename), 4)
    dict_p_ai = p_ai(filename)
    sum_comb_el = [x[0] + '|' + x[1] for x in combinations_el]
    dict_p = {}
    for el in sum_comb_el:
        dict_p[el] = round(counter_ai_aj[f'{el[0:2] + el[3:]}'] / dict_p_ai[el[3:]], 4)
    return dict_p


def sum_info(filename):
    text = read_byte(filename)
    list_elements = list(set([text[i:i + 2] for i in range(0, len(text), 2)]))
    counter_dict = collections.Counter()

    for ai in list_elements:
        counter_dict[ai] = len(re.findall(ai, text))

    dict_p_ai = p_ai(filename)

    sum_information = 0
    for key in counter_dict.keys():
        sum_information += counter_dict[key] * math.log(1 / dict_p_ai[key])
    return round(sum_information, 4)


print("Задание 1")
print("Побайтово считанный файл в hex: ", read_byte(f))
print("Длина n  файла Х в символах первичного алфавита: ", length_x(f))
print("Количество вхождений подстрок aj_ai: \n", numbers_ai_aj(f))
print("Количество вхождений любых двух-символьных подстрок, начинающих с aj: \n", numbers_aj(f))
print("Безусловная вероятность p(ai) каждого из символов ai принадлежащих A1: \n", p_ai(f))
print("Условная вероятность p(ai|aj) каждой парой символов ai,aj: \n", p_ai_aj(f))
print("Оценивает суммарное количество информации I(X) в файле: ", sum_info(f))
