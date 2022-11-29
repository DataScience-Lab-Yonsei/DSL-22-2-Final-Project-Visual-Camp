"""
[Mission 2]
Make line allocation Algorithm!
    - Raw Fixation --> Corrected Fixation

Notation:
    - RF : Raw Fixation
    - CF : Corrected Fixation
"""
from collections import defaultdict
import env
from utils._allo_func import rm_noise, get_transform, rm_peak, get_offset, classify_backward, allocate_line_id, allocate_order_id, to_CorrectedFixation


def run(rfs, word_aois, bias):
    # 전처리
    rfs = rm_noise(rfs)
    rfs = get_transform(rfs, word_aois)
    rfs = rm_peak(rfs, word_aois)
    rfs = get_offset(rfs, word_aois)

    rfs = classify_backward(rfs, word_aois)

    # 줄, 단어 배정
    rfs = allocate_line_id(rfs, word_aois, bias)
    rfs = allocate_order_id(rfs, word_aois)
    cfs = to_CorrectedFixation(rfs, word_aois)

    if env.LOG_ALL:
        ftype_status = defaultdict(int)
        for cf in cfs:
            assert cf.ftype is not None, "Missing Fixation type exists"
            ftype_status[cf.ftype] += 1
        print(ftype_status)
    return cfs
