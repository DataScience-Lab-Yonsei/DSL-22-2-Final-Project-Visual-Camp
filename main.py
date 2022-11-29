import os
import argparse
from tqdm import tqdm

import env
from utils.data_handler import DataHandler
from utils.metric import export_all


parser = argparse.ArgumentParser(
                    prog='SmartVC',
                    description='What the program does')

parser.add_argument("--is_sample", type=bool, default=False)
parser.add_argument('--export_table', type=bool, default=False)
parser.add_argument('--correct_line_x', type=bool, default=False)
parser.add_argument('--correct_line_y', type=bool, default=False)
parser.add_argument('--log_all', type=bool, default=False)
args = parser.parse_args()


def main():
    for i in tqdm(range(len(handler.data))):
        try:
            handler.sample_id = i

            # Run iVT Filter
            handler.run_ivt()

            # Run Line Allocation
            handler.run_alloc()
        except (IndexError, ValueError) as err:
            handler.data[i].RawFixationList = None
            handler.data[i].correctedFixationList = None
            print(f"{i}/{len(handler.data)} data err :", err)

    if args.export_table:
        df = export_all(handler)
        df.to_excel('data/result.xlsx')
        print(df.head(10))

    # Phase-2 : Metric(TBD)

    # Mission 3: Metric


if __name__ == '__main__':
    env.CORRECT_X = args.correct_line_x
    env.CORRECT_Y = args.correct_line_y
    env.LOG_ALL = args.log_all

    path_root = os.getcwd()
    handler = DataHandler(path_root, is_sample=args.is_sample)

    main()
