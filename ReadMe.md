# Title

DSL X Visual Camp

# Data

Some codes and data are not available because of the policy of company.

# Title

SmartVC

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

# Data Structure

We wrap raw data with Python object. class Visc has several member variables, from Raw Fixation to WordAoi.\\
You can see more details in utils/data.py

# Primary Modules

- data_handler.py

This is for DataHandler of our data. You can see more details regarding data process. 

- iVT.py

This is compose of several function to run iVT Filter. We can tell the process of iVT Filter in the function named "run".



# version log

## ver.1.1

1. data.py
    - 새로 업데이트된 데이터에 대해 추가된 것들은 다음과 같습니다.
        - 현재 raw 데이터에 있지만 iVT, LineAllo에 무관했던 데이터들 중에서, 추후 metric에 필요해 보이는 데이터를 활성화했습니다
        - wordAoi는 우선 데이터가 다 존재한다고 가정해서 업데이트했습니다.
        - BoundaryPoint는 새로 추가된 데이터로, calibration 에 관련된 정보를 담고 있습니다.
2. data_handler.py
    - 새로 업데이트 된 데이터에 맞춰 로드하는 루틴을 바꿨습니다.
        - 현재 있는 데이터로 로드가 전부 진행됩니다.
        - 컴퓨터에서 오래 걸리는 경우, 일부 sample만 뽑아서 보실 경우, 다음과 같이 진행하시면 됩니다.
            - hander를 initialization을 하는 경우 is_sample=True로 추가하시고, sample_id=원하시는 숫자. 로 하시면 됩니다.
            - 간혹 sample_id가 전체 개수보다 넘은 경우 가장 마지막 sample을 사용하도록 합니다.
3. visual.py
    - 기존 돌아가는 방식과 동일하게 진행됩니다.
    - 다만 순서대로 어떻게 점이 찍히는지 확인하실 분들은 다음과 같이 진행하시면 됩니다.
        - 찍고 싶으신 점들로 plot_points()를 실행하실 줄에서 is_save=True, fig=fig를 추가하시면 됩니다.


