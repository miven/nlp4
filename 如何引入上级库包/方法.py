import json
import torch
from fairseq.models.roberta import RobertaModel
import sys
sys.path.append("..")
from commonsense_qa import *  # load the Commonsense QA task