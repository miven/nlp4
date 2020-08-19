import torch
import torch.nn as nn
import numpy as np

__author__ = "Yu-Hsiang Huang"
# 这里面写的是注意力代码公式.
class ScaledDotProductAttention(nn.Module):
    ''' Scaled Dot-Product Attention '''

    def __init__(self, temperature, attn_dropout=0.1):
        super().__init__()
        self.temperature = temperature
        self.dropout = nn.Dropout(attn_dropout)
        self.softmax = nn.Softmax(dim=2)

    def forward(self, q, k, v, mask=None):

        attn = torch.bmm(q, k.transpose(1, 2)) # bmm:就是矩阵乘法.
        attn = attn / self.temperature

        if mask is not None:
            attn = attn.masked_fill(mask, -np.inf) # 如果是true 就用负无穷来替代. 所以下面做softmax之后,就让他的注意力为0了.因为本身这个pad 就只是填充用的,无意义.

        attn = self.softmax(attn)
        attn = self.dropout(attn)
        output = torch.bmm(attn, v)

        return output, attn
