import numpy as np
import pandas as pd
import scipy.stats

# 전반부, 후반부 나누는 라인값
# 절반으로 설정 
# def line_threshold(df_meta, ID):
#     tot = df_meta[df_meta['idx'] == ID]['line'].to_numpy()
#     thr = np.around(tot/2)
#    return thr[0]


# duration ttest pvalue
# 귀무가설: 두 집단의 평균이 같다
# pvalue 값이 클수록 귀무가설 기각 불가, 따라서 두 집단의 평균이 같다고 판단 가능
def duration_ttest(df, ID):
    df_1 = df[df['ID'] == ID]
    tot = list(df_1['line'])[-1]
    thr = tot/2
    df_up = df_1[df_1['line']<= thr ]
    df_down = df_1[df_1['line']> thr ]
    df_up_dur = list(df_up['duration'])
    df_down_dur = list(df_down['duration'])
    result = scipy.stats.ttest_ind(df_up_dur, df_down_dur, equal_var=False)
    
    return result[1]


# x좌표 f검정 pvalue
# pvalue값이 클수록 귀무가설 기각 불가, 따라서 두 집단의 분산이 같다고 판단 가능
def fixation_x_foneway(df, ID):
    df_1 = df[df['ID'] == ID]
    tot = list(df_1['line'])[-1]
    thr = tot/2
    df_up = df_1[df_1['line']<= thr ]
    df_down = df_1[df_1['line']> thr ]
    df_up_x = list(df_up['x'])
    df_down_x = list(df_down['x'])
    result = scipy.stats.f_oneway(df_up_x, df_down_x)
    
    return result[1]


# y좌표 f검정 pvalue
# 줄 배정 이전의 y좌표 사용
# pvalue값이 클수록 귀무가설 기각 불가, 따라서 두 집단의 분산이 같다고 판단 가능
def fixation_y_foneway(df, ID):
    df_1 = df[df['ID'] == ID]
    tot = list(df_1['line_id'])[-1]
    thr = tot/2
    df_up = df_1[df_1['line_id']<= thr ]
    df_down = df_1[df_1['line_id']> thr ]
    df_up_y = list(df_up['y'])
    df_down_y = list(df_down['y'])
    result = scipy.stats.f_oneway(df_up_y, df_down_y)
    
    return result[1]

# 백분위 값 구하기 
def make_percent_lst(df):
    per = np.array(df)
    per = np.around((per/np.max(per))*100)
    per_lst = per.tolist()
    return per_lst


def make_df(df, df_raw):
    id_lst = list(df["ID"].unique())
    dur_mean = []
    x_var = []
    y_var = []
    for id in id_lst:
        p_val_dur =duration_ttest(df, ID=id)
        p_val_x = fixation_x_foneway(df, ID=id)
        p_val_y = fixation_y_foneway(df_raw, ID=id)
        dur_mean.append(p_val_dur)
        x_var.append(p_val_x)
        y_var.append(p_val_y)
    df_result = pd.DataFrame(zip(id_lst, dur_mean, x_var, y_var))
    df_result = df_result.fillna(0)
    df_result.columns = ['ID', 'duration pval', 'xvar pval', 'yvar pval']
    dur_per_lst =  make_percent_lst(df_result['duration pval'])
    x_per_lst = make_percent_lst(df_result['xvar pval'])
    y_per_lst = make_percent_lst(df_result['yvar pval'])
    df_result['duration pval 백분위'] = dur_per_lst
    df_result['xvar pval 백분위'] = x_per_lst
    df_result['yvar pval 백분위'] = y_per_lst
    
    return df_result
    

# 실행
df = pd.read_excel('C:/Users/USER/Desktop/project/SmartVisC.line/data/result_correctedFixation.xlsx') # 라인 배정 이후 결과
df_raw = pd.read_excel('C:/Users/USER/Desktop/project/SmartVisC.line/data/result_rawFixation.xlsx') # 라인 배정 이전 결과

df_res = make_df(df, df_raw)
df_res.to_excel('C:/Users/USER/Desktop/project/SmartVisC.line/data/result_comparison.xlsx')