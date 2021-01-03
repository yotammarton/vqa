from vqa_model import evaluate
from dataset import VQADataset
from torch.utils.data import DataLoader
from compute_softscore import compute_targets
import numpy as np
import torch
import torch.nn as nn
import os


# TODO GAL: function called "evaluate_hw2()" . The function should load the VQA 2.0 validation set, load
#  your trained network (you can assume that the model file is located in the script folder) and
#  return the average accuracy on the val-set. This function should be written in a separate script.
#  Use this line to load your model:
#  model.load_state_dict(torch.load('model.pkl',map_location=lambda storage, loc: storage))

def evaluate_hw2():
    """
    download data to current directory, convert to .pt files, upload images to RAM and evaluate on validation set
    linux only
    """
    compute_targets(dir='datashare')

    # download validation set and convert to .pt files instead of .jpg
    os.system('wget "http://images.cocodataset.org/zips/val2014.zip"')
    os.system('unzip val2014.zip')
    os.system('rm val2014.zip')

    # argument create_imgs_tensors will convert all .jpg files to .pt files permanently
    vqa_val_dataset = VQADataset(target_pickle_path='data/cache/val_target.pkl',  # from compute_targets()
                                 questions_json_path='/datashare/v2_OpenEnded_mscoco_val2014_questions.json',
                                 images_path=os.getcwd(),  # current working directory
                                 phase='val', create_imgs_tensors=True, read_from_tensor_files=True, force_mem=True)
    val_dataloader = DataLoader(vqa_val_dataset, batch_size=128, shuffle=False, drop_last=False)

    weights_path = ''  # TODO add the weights path
    model = torch.load(weights_path)
    vqa_val_dataset.all_questions_to_word_idxs(model)
    vqa_val_dataset.num_classes = model.num_classes

    criterion = nn.BCEWithLogitsLoss(reduction='sum')
    val_mean_loss, _, val_mean_acc = evaluate(val_dataloader, model, criterion, 0, vqa_val_dataset)

    return val_mean_loss, val_mean_acc


if __name__ == '__main__':
    loss, accuracy = evaluate_hw2()
