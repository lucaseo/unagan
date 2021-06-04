import os
import numpy as np
from multiprocessing import Pool
import pickle


def process_audios(feat_dir, feat_fn):
    feat_fp = os.path.join(feat_dir, f'{feat_fn}.npy')

    if os.path.exists(feat_fp):
        return feat_fn, np.load(feat_fp).shape[-1]
    else:
        return feat_fn, 0



if __name__ == "__main__":
    feat_type = 'mel'
    exp_dir = './training_data/exp_data/'  # base_out_dir from step2

    out_fp = os.path.join(exp_dir, 'dataset.pkl')

    # ### Process ###
    feat_dir = os.path.join(exp_dir, feat_type)

    feat_fns = [fn.replace('.npy', '') for fn in os.listdir(feat_dir)]
    dataset = []

    for feat in feat_fns:
        feat_fn, length = process_audios(feat_dir, feat)
        if length == 0:
            continue
        dataset.append((feat_fn, length))

    with open(out_fp, 'wb') as f:
        pickle.dump(dataset, f)

    print(len(dataset))