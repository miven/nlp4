import os
from pathlib import Path


VOCAB_DIR = Path(__file__).resolve().parent.parent / "data"  # 获取绝对路径的方法
PAD = "@@PADDING@@"
UNK = "@@UNKNOWN@@"
START_TOKEN = "$START"
SEQ_DELIMETERS = {"tokens": " ",
                  "labels": "SEPL|||SEPR",
                  "operations": "SEPL__SEPR"}


def get_verb_form_dicts():
    path_to_dict = os.path.join(VOCAB_DIR, "verb-form-vocab.txt")
    encode, decode = {}, {}
    with open(path_to_dict, encoding="utf-8") as f:
        for line in f:
            words, tags = line.split(":")
            word1, word2 = words.split("_")
            tag1, tag2 = tags.split("_")
            decode_key = f"{word1}_{tag1}_{tag2.strip()}"
            if decode_key not in decode:
                encode[words] = tags
                decode[decode_key] = word2
    return encode, decode


ENCODE_VERB_DICT, DECODE_VERB_DICT = get_verb_form_dicts()


def get_target_sent_by_edits(source_tokens, edits):
    target_tokens = source_tokens[:]+['']# 需要加一个空字符串,避免最后添加时候的bug
    shift_idx = 0
    for edit in edits:
        start, end, label, _ = edit
        target_pos = start + shift_idx
        source_token = target_tokens[target_pos] if target_pos >= 0 else ''
        if label == "": # 用label来判断是4中操作中的哪一个.
            del target_tokens[target_pos]
            shift_idx -= 1
        elif start == end:
            word = label.replace("$APPEND_", "")
            target_tokens[target_pos: target_pos] = [word] # 这个语法就是数组的插入.
            shift_idx += 1
        elif label.startswith("$TRANSFORM_"):
            word = apply_reverse_transformation(source_token, label)
            if word is None:
                word = source_token
            target_tokens[target_pos] = word
        elif start == end - 1:
            word = label.replace("$REPLACE_", "")
            target_tokens[target_pos] = word
        elif label.startswith("$MERGE_"):
            target_tokens[target_pos + 1: target_pos + 1] = [label]
            shift_idx += 1

    return replace_merge_transforms(target_tokens)


def replace_merge_transforms(tokens):
    if all(not x.startswith("$MERGE_") for x in tokens):
        return tokens

    target_line = " ".join(tokens)
    target_line = target_line.replace(" $MERGE_HYPHEN ", "-")
    target_line = target_line.replace(" $MERGE_SPACE ", "")
    return target_line.split()


def convert_using_case(token, smart_action):
    if not smart_action.startswith("$TRANSFORM_CASE_"):
        return token
    if smart_action.endswith("LOWER"):
        return token.lower()
    elif smart_action.endswith("UPPER"):
        return token.upper()
    elif smart_action.endswith("CAPITAL"):
        return token.capitalize()
    elif smart_action.endswith("CAPITAL_1"):
        return token[0] + token[1:].capitalize()
    elif smart_action.endswith("UPPER_-1"):
        return token[:-1].upper() + token[-1]
    else:
        return token


def convert_using_verb(token, smart_action):
    key_word = "$TRANSFORM_VERB_"
    if not smart_action.startswith(key_word):
        raise Exception(f"Unknown action type {smart_action}")
    encoding_part = f"{token}_{smart_action[len(key_word):]}"
    decoded_target_word = decode_verb_form(encoding_part)
    return decoded_target_word


def convert_using_split(token, smart_action):
    key_word = "$TRANSFORM_SPLIT"
    if not smart_action.startswith(key_word):
        raise Exception(f"Unknown action type {smart_action}")
    target_words = token.split("-")
    return " ".join(target_words)


def convert_using_plural(token, smart_action):
    if smart_action.endswith("PLURAL"):
        return token + "s"
    elif smart_action.endswith("SINGULAR"):
        return token[:-1]
    else:
        raise Exception(f"Unknown action type {smart_action}")
complex_plural = os.path.join(VOCAB_DIR, "complex_plural")
complex_plural2={}
with open(complex_plural, encoding="utf-8") as f:
    for line in f:
        w1, w2 = line.split(":")
        complex_plural2[w1]=w2

complex_plural=complex_plural2




spelling_mistake = os.path.join(VOCAB_DIR, "spelling_mistake")
spelling_mistake2={}
with open(spelling_mistake, encoding="utf-8") as f:
    for line in f:
        w1, w2 = line.split(":")
        spelling_mistake2[w1]=w2

spelling_mistake=spelling_mistake2







# 跟train无关. train时候跟tgt无关了, 只跟output.txt有关.

# predict时候通过变换的到最终文本.             src--------token----(tag)-------------tgt^
def apply_reverse_transformation(source_token, transform):
    if transform.startswith("$TRANSFORM"):
        # deal with equal
        if transform == "$KEEP":
            return source_token
        # deal with case
        if transform.startswith("$TRANSFORM_CASE"):
            return convert_using_case(source_token, transform)
        # deal with verb
        if transform.startswith("$TRANSFORM_VERB"): # big 并不是动词,  ------动词词表中没有,
            try:
                  return convert_using_verb(source_token, transform)
            except:
                return source_token
        # deal with split
        if transform.startswith("$TRANSFORM_SPLIT"):
            return convert_using_split(source_token, transform)
        # deal with single/plural
        if transform.startswith("$TRANSFORM_AGREEMENT"):
            return convert_using_plural(source_token, transform)
        # raise exception if not find correct type
        if transform.startswith("$TRANSFORM_COMPLEX_PLURAL"):# 用字典恢复target
            try:
                return  complex_plural[source_token]  # 如果超出了字典的范围就当keep用!!!!!!!!!!!!!----------------------这个地方需要仔细看看!!!!!!!!!!!!!!!!否则train会失效. 这就是刚才发现的问题, vorb变换里面为什么没有这个问题呢? 因为vorb变换里面的词典包含所有的vorb,任意vorb都在词典中存在. 所以不存在没法变换的情况. 这点是之后看如何克服!!!!!!!!!!!!!还没想到好方法. 突然好想理解了,好像这里的处理, 没有这个key 就直接keep没问题. 因为 predict时候肯定是可以的, 然后看train的时候逻辑是否正确. train的时候, 用平行预料首先先打好了标签, 之后预测的时候也只是用 yhat 和y之间的交叉熵.没有涉及这个tag--->target的变换.所以不影响训练. 仍然能吧应该keep没keep的做出loss, 应该speelingmistake 没spellingmistake的的做出loss. 从这里面想,predict的时候vorb也有bug,也需要fix
            except:
                return source_token
        if transform.startswith("$TRANSFORM_SPELLING_MISTAKE"):# 用字典恢复target,
            try:
                 return spelling_mistake[source_token]
            except:
                return source_token
        raise Exception(f"Unknown action type {transform}")
    else:
        return source_token


def read_parallel_lines(fn1, fn2):
    lines1 = read_lines(fn1, skip_strip=True)
    lines2 = read_lines(fn2, skip_strip=True)
    lines1=[i for i in lines1 if i !='']
    lines2=[i for i in lines2 if i !='']
    assert len(lines1) == len(lines2)
    out_lines1, out_lines2 = [], []
    for line1, line2 in zip(lines1, lines2):
        if not line1.strip() or not line2.strip():  # 只要平行预料中存在一个strip的就同时跳过2个预料对应句子.
            continue
        else:
            out_lines1.append(line1)
            out_lines2.append(line2)
    return out_lines1, out_lines2


def read_lines(fn, skip_strip=False):
    if not os.path.exists(fn):
        return []
    with open(fn, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return [s.strip() for s in lines if s.strip() or skip_strip]


def write_lines(fn, lines, mode='w'):
    if mode == 'w' and os.path.exists(fn):
        os.remove(fn)
    with open(fn, encoding='utf-8', mode=mode) as f:
        f.writelines(['%s\n' % s for s in lines])


def decode_verb_form(original):
    return DECODE_VERB_DICT.get(original)


def encode_verb_form(original_word, corrected_word):
    decoding_request = original_word + "_" + corrected_word
    decoding_response = ENCODE_VERB_DICT.get(decoding_request, "").strip()# 就是在词典中搜索.
    if original_word and decoding_response:
        answer = decoding_response
    else:
        answer = None
    return answer









def get_weights_name(transformer_name, lowercase):
    if transformer_name == 'bert' and lowercase:
        return 'bert-base-uncased'
    if transformer_name == 'bert' and not lowercase:
        return 'bert-base-cased'
    if transformer_name == 'distilbert':
        if not lowercase:
            print('Warning! This model was trained only on uncased sentences.')
        return 'distilbert-base-uncased'
    if transformer_name == 'albert':
        if not lowercase:
            print('Warning! This model was trained only on uncased sentences.')
        return 'albert-base-v1'
    if lowercase:
        print('Warning! This model was trained only on cased sentences.')
    if transformer_name == 'roberta':
        return 'roberta-base'
    if transformer_name == 'gpt2':
        return 'gpt2'
    if transformer_name == 'transformerxl':
        return 'transfo-xl-wt103'
    if transformer_name == 'xlnet':
        return 'xlnet-base-cased'
