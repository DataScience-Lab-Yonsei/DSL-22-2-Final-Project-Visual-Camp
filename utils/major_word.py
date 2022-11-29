import os
import pandas as pd
import matplotlib.pyplot as plt

from utils.data_handler import DataHandler
from utils.word_padding import calc_pad_width
from utils.visual import set_scale, plot_text



os.chdir('..')
path_root = os.getcwd()
handler = DataHandler(path_root)
word_aois = handler.get_word_aoi()


# 각 라인별 단어 수
order = [i.order for i in word_aois]
line_word_cnt = []

for i in range(len(order)):
    if i != (len(order)-1):
        if order[i+1] == 0:
            line_word_cnt.append(order[i]+1)
    else:
        line_word_cnt.append(order[i]+1)


# 라인별로 전체 단어 중 몇 번째인지 넘버링
full_word_cnt = list(range(len(word_aois)))
line_order_numbers = []

for i in line_word_cnt:
    if len(full_word_cnt) > 0:
        line_order_numbers.append(full_word_cnt[:i])
        del full_word_cnt[:i]


# 읽기에 중요하다 판단한 단어 = major word
# major word가 전체 단어 중 몇 번째인지
# 발표 준비를 우선해 데이터는 일단 직접 입력했습니다. 추후 자동화를 위한 수정 예정...
major_word = ['옷감 ', '짜는 ', '법을 ', '급한 ', '신중한 ', '엉망인 ', '날실과 ', '씨실의 ', '짜임으로 ']
# print([{'word': j.word, 'line': j.line, 'order': j.order, 'id': j.idx} for i in major_word for j in word_aois if i == j.word])
maj_word_info = [[{'line': 0, 'order': 5},
                 {'line': 0, 'order': 6},
                 {'line': 0, 'order': 7}],
                 {'line': 1, 'order': 3},
                 {'line': 3, 'order': 8},
                 {'line': 7, 'order': 1},
                 [{'line': 10, 'order': 0},
                 {'line': 10, 'order': 1},
                 {'line': 10, 'order': 2}]]

maj_order_numbers = []

for i in maj_word_info:
    if type(i) is list:
        maj_order_number = [line_order_numbers[j['line']][j['order']] for j in i]
        maj_order_numbers.append(maj_order_number)
    else:
        maj_order_number = line_order_numbers[i['line']][i['order']]
        maj_order_numbers.append(maj_order_number)


# major word의 padded area
pad_xs1, pad_ys1, pad_xs2, pad_ys2 = calc_pad_width(word_aois)
maj_pad_xs1, maj_pad_ys1, maj_pad_xs2, maj_pad_ys2 = [], [], [], []

for i in maj_order_numbers:
    if type(i) is list:
        pad_area = [[pad_xs1[j], pad_ys1[j], pad_xs2[j], pad_ys2[j]] for j in i]
        maj_pad_xs1.append(pad_area[-1][0])
        maj_pad_ys1.append(pad_area[-1][1])
        maj_pad_xs2.append(pad_area[0][2])
        maj_pad_ys2.append(pad_area[0][3])
    else:
        maj_pad_xs1.append(pad_xs1[i])
        maj_pad_ys1.append(pad_ys1[i])
        maj_pad_xs2.append(pad_xs2[i])
        maj_pad_ys2.append(pad_ys2[i])


# major word area plot
# 한글 깨짐 ('AppleGothic'은 자간이 넓어 사용 불가)
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'Apple SD Gothic Neo'

fig, ax = plt.subplots(1, 2, figsize=(20, 10))
set_scale(handler.get_resolution(), ax)

plot_text(ax[0], word_aois)
plot_text(ax[1], word_aois)

ax[1].scatter(maj_pad_xs1, maj_pad_ys1, c='purple', s=10)  # 영점 기준 단어 좌하단
ax[1].scatter(maj_pad_xs2, maj_pad_ys2, c='red', s=10)  # 영점 기준 단어 우상단
ax[1].set_title("Major Word")

# plt.show()


# major word area 내 fixation 유무 확인
all_handler = DataHandler(path_root, is_sample=False)
# print([(i.idx, i.age) for i in all_handler.data])
# print(len([(i.idx, i.age) for i in all_handler.data]))
cf = [i.correctedFixationList for i in all_handler.data if i.age == 11]
id = [i.idx for i in all_handler.data if i.age == 11]
# print(len(id))
# print(id)
# 왜 4학년 데이터 중 6355e7d4dc3623a175741f99는 잡히지 않는지 확인 필요

check_in_maj_words = []

for i in range(len(cf)):
    cf_xs = [cf[i][j].x for j in range(len(cf[i]))]
    cf_ys = [cf[i][j].y for j in range(len(cf[i]))]

    check_in_maj_word = []  # 각 major word area에 한 학생의 fixation이 포함되는지

    for j in range(len(maj_pad_xs1)):
        xs_in_maj_word = []         # 각 major word area에 들어오는 한 학생의 fixation x좌표

        for t in range(len(cf_xs)):
            if (maj_pad_xs2[j] <= cf_xs[t] <= maj_pad_xs1[j]) and (maj_pad_ys2[j] <= cf_ys[t] <= maj_pad_ys1[j]):
                xs_in_maj_word.append(cf_xs[t])

        if len(xs_in_maj_word) > 0:
            check_in_maj_word.append(1)
        else:
            check_in_maj_word.append(0)

    check_in_maj_words.append(check_in_maj_word)

check_in_maj_words_5 = list(map(sum, check_in_maj_words))


# id, major word 포함 여부로 data frame 생성
df = pd.DataFrame((zip(id, check_in_maj_words, check_in_maj_words_5)), columns = ['_id', 'IN major words', 'IN major words (5point)'])
print(df)
df.to_excel("metric_major word.xlsx")