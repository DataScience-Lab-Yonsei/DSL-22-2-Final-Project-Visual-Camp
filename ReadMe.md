# SmartVC

[2022-2학기 DSL X Visual Camp 기업연계 프로젝트] 시선데이터 기반 읽기 능력 평가 서비스 개선

팀원 강민주 김원 유채원 이승주 조보경 최명헌 황진우 전혜령 김예진

# Notice

Some codes and data are not available because of the policy of company.

# Overview

## Motivation 
![사진](/figure/1.PNG)

## Problem Definition
![사진](/figure/2.PNG)

# How to run

```
python main.py
```

There are some arguments to be changed.
- is_sample = True : Run SmartVC with specific sample. You can see more details at initialization of DataHandler(utils/data_handler.py)
- sample_id = 0 : In the case of run SmartVC with specific sample, you can choose which sample to run.
- export_table = True : Once we run SmartVC, we can export the result of the whole data in xlsx file. There are 3 files to be exported, which are tables of CorrectedFixation, RawFixation and WordAoi.   
- corrected_line_x(y) = True : Run line allocation algorithm with correction(our suggestion). If you allocate False, then line allocation is based on Nearest Neighbor Algorithm. Or, you can run with our suggestions.
- log_all = True: When you run SmartVC, you can easily debug current status.

# Details
## Data Structure

We wrap raw data with Python object. class Visc has several member variables, from Raw Fixation to WordAoi.\\
You cannot see more details because of the policy.

## Primary Modules

- data_handler.py

This is for DataHandler of our data. You can see more details regarding data process. 

- iVT.py

This is compose of several function to run iVT Filter. We can tell the process of iVT Filter in the function named "run".

# Sample

![사진](/figure/3.PNG)
