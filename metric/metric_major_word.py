import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utils.data_handler import DataHandler
from utils.word_padding import calc_pad_width
from utils.visual import set_scale, plot_text


# 지문 내 단어들을 full count해서 order를 매긴 걸 라인별로 나눈 것
# 예를 들어 2줄짜리 지문이 각 줄마다 10, 11단어가 들어있다면 다음과 같이 출력
# [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]]
def word_full_order(path_root, grade=4):
    grade_id = [150, 300, 200, 0, 100, 250]     # sample index (순서대로 1~6학년의 데이터 중 임의로 정한 index)
    sample_id = grade_id[grade-1]

    handler = DataHandler(path_root, sample_id)
    word_aois = handler.get_word_aoi()

    # 각 라인별 단어 수
    order = [i.order for i in word_aois]
    line_word_cnt = []

    for i in range(len(order)):
        if i != (len(order) - 1):
            if order[i + 1] == 0:
                line_word_cnt.append(order[i] + 1)
        else:
            line_word_cnt.append(order[i] + 1)

    # 라인별로 전체 단어 중 몇 번째인지 넘버링
    full_word_cnt = list(range(len(word_aois)))
    line_full_order = []

    for i in line_word_cnt:
        if len(full_word_cnt) > 0:
            line_full_order.append(full_word_cnt[:i])
            del full_word_cnt[:i]

    return handler, word_aois, line_full_order


# word_full_order()를 바탕으로 major word의 지문 내 위치 찾기
# 즉 major word가 전체 단어 중 몇 번째인지
# major word가 ['옷감 ', '짜는 ', '법을 '], '급한 ', '신중한 '이라면
# input으로 들어가는 MW_info는 다음과 같은 형식으로 (여러 어절인 경우 처음과 끝만)
# [[{'line': 0, 'order': 5}, {'line': 0, 'order': 7}], {'line': 1, 'order': 3}, {'line': 3, 'order': 8}]
def MajorWord_full_order(path_root, MW_info, grade=4):
    handler, word_aois, line_full_order = word_full_order(path_root, grade)
    MW_full_orders = []

    for i in MW_info:
        if type(i) is list:     # 여러 단어가 묶인 경우 ex. ['옷감 ', '짜는 ', '법을 ']
            MW_full_order = [line_full_order[j['line']][j['order']] for j in i]
            MW_full_orders.append(MW_full_order)
        else:       # 단일 단어의 경우
            MW_full_order = line_full_order[i['line']][i['order']]
            MW_full_orders.append(MW_full_order)

    return handler, word_aois, MW_full_orders


def MajorWord_padding(path_root, MW_info, grade=4, plot=False):
    handler, word_aois, MW_full_orders = MajorWord_full_order(path_root, MW_info, grade)

    pad_xs1, pad_ys1, pad_xs2, pad_ys2 = calc_pad_width(word_aois)
    MW_pad_xs1, MW_pad_ys1, MW_pad_xs2, MW_pad_ys2 = [], [], [], []

    for i in MW_full_orders:
        if type(i) is list:
            pad_area = [[pad_xs1[j], pad_ys1[j], pad_xs2[j], pad_ys2[j]] for j in i]
            MW_pad_xs1.append(pad_area[-1][0])
            MW_pad_ys1.append(pad_area[-1][1])
            MW_pad_xs2.append(pad_area[0][2])
            MW_pad_ys2.append(pad_area[0][3])
        else:
            MW_pad_xs1.append(pad_xs1[i])
            MW_pad_ys1.append(pad_ys1[i])
            MW_pad_xs2.append(pad_xs2[i])
            MW_pad_ys2.append(pad_ys2[i])

    # major word 확인용 - 원하는 단어가 맞는지 시각화
    if plot:
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.family'] = 'Apple SD Gothic Neo'
        fig, ax = plt.subplots(1, 2, figsize=(20, 10))

        set_scale(handler.get_resolution(), ax)

        plot_text(ax[0], word_aois)
        plot_text(ax[1], word_aois)

        ax[1].scatter(MW_pad_xs1, MW_pad_ys1, c='purple', s=10)     # major word 시작점
        ax[1].scatter(MW_pad_xs2, MW_pad_ys2, c='red', s=10)        # major word 끝점
        ax[1].set_title("Major Word")

        plt.show()

    return MW_pad_xs1, MW_pad_ys1, MW_pad_xs2, MW_pad_ys2


# major word area 내 fixation 유무 확인
# 왜 4학년 데이터 중 6355e7d4dc3623a175741f99는 잡히지 않는지
# grade를 학년에 맞게 1~6을 넣어 학년별로 확인하거나 / 0을 넣어 전체 학생 확인하는 것 가능하도록 구현
def check_in_MajorWords(path_root, MW_info, grade=4, to_excel=False):
    ages = [8, 9, 10, 11, 12, 13]
    all_handler = DataHandler(path_root, is_sample=False)

    if grade > 0:
        print(f'{grade}학년 학생에 대한 major word metric을 계산합니다.')
        MW_pad_xs1, MW_pad_ys1, MW_pad_xs2, MW_pad_ys2 = MajorWord_padding(path_root, MW_info, grade)

        age = ages[grade-1]
        cf = [i.correctedFixationList for i in all_handler.data if i.age == age]

        check_in_MWs = []

        for i in range(len(cf)):
            cf_xs = [cf[i][j].x for j in range(len(cf[i]))]
            cf_ys = [cf[i][j].y for j in range(len(cf[i]))]

            check_in_MW = []  # 각 major word area에 한 학생의 fixation이 포함되는지

            for j in range(len(MW_pad_xs1)):
                xs_in_MW = []  # 각 major word area에 들어오는 한 학생의 fixation x좌표

                for t in range(len(cf_xs)):
                    if (MW_pad_xs2[j] <= cf_xs[t] <= MW_pad_xs1[j]) and (MW_pad_ys2[j] <= cf_ys[t] <= MW_pad_ys1[j]):
                        xs_in_MW.append(cf_xs[t])

                if len(xs_in_MW) > 0:
                    check_in_MW.append(1)
                else:
                    check_in_MW.append(0)

            check_in_MWs.append(check_in_MW)

        check_in_MWs_score = list(map(sum, check_in_MWs))

        # id, major word 포함 여부로 data frame 생성 및 엑셀 출력
        if to_excel:
            id = [i.idx for i in all_handler.data if i.age == age]
            df = pd.DataFrame((zip(id, check_in_MWs, np.array(check_in_MWs_score)/len(MW_pad_xs1), check_in_MWs_score)),
                              columns=['_id', 'IN major words', 'percentage score', f'{len(MW_pad_xs1)}point score'])
            print(df)
            df.to_excel(f"metric_major word_grade{grade}.xlsx")

    else:        # 0을 입력하는 경우 = 전체 학생 출력
        print('전체 학생에 대한 major word metric을 계산합니다.')
        for age in ages:
            _grade = age - 7
            MW_pad_xs1, MW_pad_ys1, MW_pad_xs2, MW_pad_ys2 = MajorWord_padding(path_root, MW_info[_grade-1], _grade)
            cf = [i.correctedFixationList for i in all_handler.data if i.age == age]

            check_in_MWs = []

            for i in range(len(cf)):
                cf_xs = [cf[i][j].x for j in range(len(cf[i]))]
                cf_ys = [cf[i][j].y for j in range(len(cf[i]))]

                check_in_MW = []

                for j in range(len(MW_pad_xs1)):
                    xs_in_MW = []

                    for t in range(len(cf_xs)):
                        if (MW_pad_xs2[j] <= cf_xs[t] <= MW_pad_xs1[j]) and (
                                MW_pad_ys2[j] <= cf_ys[t] <= MW_pad_ys1[j]):
                            xs_in_MW.append(cf_xs[t])

                    if len(xs_in_MW) > 0:
                        check_in_MW.append(1)
                    else:
                        check_in_MW.append(0)

                check_in_MWs.append(check_in_MW)

            check_in_MWs_score = list(map(sum, check_in_MWs))

            id = [i.idx for i in all_handler.data if i.age == age]
            globals()[f'df_{_grade}'] = pd.DataFrame((zip(id, check_in_MWs, np.array(check_in_MWs_score)/len(MW_pad_xs1), check_in_MWs_score)),
                                                     columns=['_id', 'IN major words', 'percentage score', f'{len(MW_pad_xs1)}point score'])

        # id, major word 포함 여부로 data frame 생성 및 엑셀 출력
        if to_excel:
            df = pd.concat([df_1, df_2, df_3, df_4, df_5, df_6])
            print(df)
            df.to_excel("metric_major word_All.xlsx")


# Input data (팀 내에서 읽기에 중요하다 판단한 단어로 임의 지정)
# major word의 line과 order (지문 내 동일 단어가 중복되는 경우가 많아 이와 같이 단어를 입력하는 방법 선택)
MW_info_1st = [[{'line': 0, 'order': 1},
                {'line': 0, 'order': 3}],
                {'line': 1, 'order': 0},
                {'line': 1, 'order': 2},
                [{'line': 6, 'order': 3},
                {'line': 6, 'order': 4}],
                [{'line': 7, 'order': 5},
                {'line': 7, 'order': 6}],
                [{'line': 9, 'order': 1},
                {'line': 9, 'order': 5}]]

MW_info_2nd = [[{'line': 1, 'order': 1},
                {'line': 1, 'order': 3}],
                {'line': 1, 'order': 5},
                {'line': 2, 'order': 8},
                [{'line': 3, 'order': 0},
                {'line': 3, 'order': 2}],
                [{'line': 5, 'order': 6},
                {'line': 5, 'order': 7}],
                [{'line': 6, 'order': 0},
                {'line': 6, 'order': 1}]]

MW_info_3rd = [[{'line': 0, 'order': 4},
                {'line': 0, 'order': 7}],
                {'line': 2, 'order': 0},
               {'line': 3, 'order': 7},
               [{'line': 6, 'order': 1},
                {'line': 6, 'order': 4}],
               {'line': 9, 'order': 3},
               [{'line': 11, 'order': 0},
                {'line': 11, 'order': 3}],
               [{'line': 12, 'order': 8},
                {'line': 12, 'order': 10}]]

MW_info_4th = [[{'line': 0, 'order': 5},
                 {'line': 0, 'order': 7}],
                 {'line': 1, 'order': 3},
                 {'line': 3, 'order': 8},
                 {'line': 7, 'order': 1},
                 [{'line': 10, 'order': 0},
                 {'line': 10, 'order': 2}]]

MW_info_5th = [{'line': 0, 'order': 0},
               [{'line': 1, 'order': 2},
                {'line': 1, 'order': 3}],
                {'line': 13, 'order': 5}]

MW_info_6th = [[{'line': 0, 'order': 6},
               {'line': 0, 'order': 7}],
               {'line': 3, 'order': 5},
               {'line': 4, 'order': 4},
               [{'line': 4, 'order': 6},
                {'line': 4, 'order': 7}],
                {'line': 4, 'order': 11},
               [{'line': 6, 'order': 8},
                {'line': 6, 'order': 9}],
               [{'line': 10, 'order': 3},
                {'line': 10, 'order': 6}]]

MW_info = [MW_info_1st, MW_info_2nd, MW_info_3rd, MW_info_4th, MW_info_5th, MW_info_6th]

os.chdir('..')
path_root = os.getcwd()

## 학년별 처리
# MW_info가 input 형식에 맞게 잘 작성되었는지 시각화로 확인
# sample_grade = 6
# MajorWord_padding(path_root, MW_info[sample_grade-1], sample_grade, plot=True)

# 각 학년별 지표화 및 엑셀 파일로 저장
# for sample_grade in [1,2,3,4,5,6]:
#     print(check_in_MajorWords(path_root, MW_info[sample_grade-1], sample_grade, to_excel=True))


## 전체 학생 처리
# 전체 학생 지표화 및 엑셀 파일로 저장
# check_in_MajorWords(path_root, MW_info, grade=0, to_excel=True)