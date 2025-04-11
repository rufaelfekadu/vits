import os
import json
import math
import torch
from torch import nn
from tqdm import tqdm
from torch.nn import functional as F
from torch.utils.data import DataLoader


import commons
import utils
from data_utils import TextAudioLoader, TextAudioCollate, TextAudioSpeakerLoader, TextAudioSpeakerCollate
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence

from scipy.io.wavfile import write
from pathlib import Path
import regex
import soundfile as sf

def remove_diacretics(text):
    diacritic_pattern = r'[\u064B-\u0652]'
    text = regex.sub(diacritic_pattern, '', text)
    return text

def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

config_path = "configs/arvoice.json"
ckpt_path = "logs/arvoice_sr/G_187000.pth"
eval_file = "filelists/arvoice_sr_test_filelist.txt"
eval_dir = "logs/arvoice_sr/eval/epoch_2000/no_diacretics"
os.makedirs(eval_dir, exist_ok=True)


# exp_name = Path(ckpt_path).parts[-2]

# out_path = "evaluation/" + exp_name

# os.makedirs(out_path, exist_ok=True)

hps = utils.get_hparams_from_file(config_path)

net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    n_speakers=hps.data.n_speakers,
    **hps.model).cuda()
_ = net_g.eval()

_ = utils.load_checkpoint(ckpt_path , net_g, None)

samples = []

with open(eval_file, "r", encoding="utf-8") as f:
    for line in f:
        samples.append(line.strip().split("|"))
        
for i, (name, spkr, text) in tqdm(enumerate(samples)):
    name = name.split("/")[-1]
    # text = remove_diacretics(text)
    stn = get_text(text, hps)
    with torch.no_grad():
        x = stn.cuda().unsqueeze(0)
        x_lengths = torch.LongTensor([stn.size(0)]).cuda()
        sid = torch.LongTensor([int(spkr)]).cuda()
        audio = net_g.infer(x, x_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
        sf.write(f"{eval_dir}/{name}", audio, 22050)