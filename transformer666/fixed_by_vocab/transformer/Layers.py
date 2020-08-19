''' Define the Layers '''
import torch.nn as nn
from transformer.SubLayers import MultiHeadAttention, PositionwiseFeedForward

__author__ = "Yu-Hsiang Huang"


class EncoderLayer(nn.Module):
    ''' Compose with two layers '''

    def __init__(self, d_model, d_inner, n_head, d_k, d_v, dropout=0.1):
        super(EncoderLayer, self).__init__()
        self.slf_attn = MultiHeadAttention(
            n_head, d_model, d_k, d_v, dropout=dropout)
        self.pos_ffn = PositionwiseFeedForward(d_model, d_inner, dropout=dropout)

    def forward(self, enc_input, non_pad_mask=None, slf_attn_mask=None):
        enc_output, enc_slf_attn = self.slf_attn(  # 第一个是结果,第二是注意力参数表.作为查看用.对结果没用.
            enc_input, enc_input, enc_input, mask=slf_attn_mask) # q,k,v 的输入都是一样的.
        enc_output *= non_pad_mask# 再次去掉那些pad位置.

        enc_output = self.pos_ffn(enc_output)
        enc_output *= non_pad_mask

        return enc_output, enc_slf_attn


class DecoderLayer(nn.Module):
    ''' Compose with three layers '''

    def __init__(self, d_model, d_inner, n_head, d_k, d_v, dropout=0.1):
        super(DecoderLayer, self).__init__()
        self.slf_attn = MultiHeadAttention(n_head, d_model, d_k, d_v, dropout=dropout) # 解码里面多一层.enc_attn
        self.enc_attn = MultiHeadAttention(n_head, d_model, d_k, d_v, dropout=dropout)
        self.pos_ffn = PositionwiseFeedForward(d_model, d_inner, dropout=dropout)

        from pathlib import Path
        output_filedir = Path(__file__).resolve().parent.parent / 'vocab_pair'  # 获取绝对路径的方法

        dic2={}
        with open (output_filedir ,encoding='utf-8') as f:
            tmp=f.readlines()
            for i in tmp:
                i=i.strip('\n').split(':')
                dic2[i[0]]=i[1]
        self.check_dic=dic2
        tmmm=1









    def forward(self, dec_input, enc_output, non_pad_mask=None, slf_attn_mask=None, dec_enc_attn_mask=None):
        dec_output, dec_slf_attn = self.slf_attn(
            dec_input, dec_input, dec_input, mask=slf_attn_mask) # 一共有3个mask, 第一个自注意力,需要future加pad2个mask
        dec_output *= non_pad_mask         # 都是qkv

        dec_output, dec_enc_attn = self.enc_attn( # 还是qkv 算法
            dec_output, enc_output, enc_output, mask=dec_enc_attn_mask) #第二个 再进入enc_attn

        '''
        dec_output:q
        enc_output:k
        enc_output:v
             
        
        dec_enc_attn: 设个就是decoding和encoidng 之间的attention 我们就用这个来进行修改loss
        如果碰到了字典中的对,那么我们就让他loss 趋近时候 对应attention变大,这样, 经过训练
        网络就学到了 他俩的关系.并且关系大,还让翻译的loss低. 也就是我们要的效果.
        既保证了翻译的正确性,又保证了自定义词典之间的翻译正确性!!!!!!!!!!!!!!
        从而提高翻译效率!!!!!!!!!!!!!!!!
        '''



        dec_output *= non_pad_mask

        dec_output = self.pos_ffn(dec_output)
        dec_output *= non_pad_mask

        return dec_output, dec_slf_attn, dec_enc_attn
