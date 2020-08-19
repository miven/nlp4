import argparse
import os
from difflib import SequenceMatcher

import Levenshtein
import numpy as np
from tqdm import tqdm
'''
这个文件是给与true_data, false_data, 然后输出 他们对齐文件.里面包含他们的diff信息.
'''
from .helpers import write_lines, read_parallel_lines, encode_verb_form, \
    apply_reverse_transformation, SEQ_DELIMETERS, START_TOKEN


def perfect_align(t, T, insertions_allowed=0,
                  cost_function=Levenshtein.distance):
    # dp[i, j, k] is a minimal cost of matching first `i` tokens of `t` with
    # first `j` tokens of `T`, after making `k` insertions after last match of
    # token from `t`. In other words t[:i] aligned with T[:j].

    # Initialize with INFINITY (unknown)
    shape = (len(t) + 1, len(T) + 1, insertions_allowed + 1)
    dp = np.ones(shape, dtype=int) * int(1e9)
    come_from = np.ones(shape, dtype=int) * int(1e9)
    come_from_ins = np.ones(shape, dtype=int) * int(1e9)

    dp[0, 0, 0] = 0  # The only known starting point. Nothing matched to nothing.
    for i in range(len(t) + 1):  # Go inclusive
        for j in range(len(T) + 1):  # Go inclusive
            for q in range(insertions_allowed + 1):  # Go inclusive
                if i < len(t):
                    # Given matched sequence of t[:i] and T[:j], match token
                    # t[i] with following tokens T[j:k].
                    for k in range(j, len(T) + 1):
                        transform = \
                            apply_transformation(t[i], '   '.join(T[j:k]))
                        if transform:
                            cost = 0
                        else:
                            cost = cost_function(t[i], '   '.join(T[j:k]))
                        current = dp[i, j, q] + cost
                        if dp[i + 1, k, 0] > current:
                            dp[i + 1, k, 0] = current
                            come_from[i + 1, k, 0] = j
                            come_from_ins[i + 1, k, 0] = q
                if q < insertions_allowed:
                    # Given matched sequence of t[:i] and T[:j], create
                    # insertion with following tokens T[j:k].
                    for k in range(j, len(T) + 1):
                        cost = len('   '.join(T[j:k]))
                        current = dp[i, j, q] + cost
                        if dp[i, k, q + 1] > current:
                            dp[i, k, q + 1] = current
                            come_from[i, k, q + 1] = j
                            come_from_ins[i, k, q + 1] = q

    # Solution is in the dp[len(t), len(T), *]. Backtracking from there.
    alignment = []
    i = len(t)
    j = len(T)
    q = dp[i, j, :].argmin()
    while i > 0 or q > 0:
        is_insert = (come_from_ins[i, j, q] != q) and (q != 0)
        j, k, q = come_from[i, j, q], j, come_from_ins[i, j, q]
        if not is_insert:
            i -= 1

        if is_insert:
            alignment.append(['INSERT', T[j:k], (i, i)])
        else:
            alignment.append([f'REPLACE_{t[i]}', T[j:k], (i, i + 1)])

    assert j == 0

    return dp[len(t), len(T)].min(), list(reversed(alignment))


def _split(token):
    if not token:
        return []
    parts = token.split()
    return parts or [token]

# # merge space, merge hyphen ,$MERGE_SWAP  这个函数输出这3中变化.
def apply_merge_transformation(source_tokens, target_words, shift_idx):
    edits = []
    if len(source_tokens) > 1 and len(target_words) == 1:
        # check merge
        transform = check_merge(source_tokens, target_words)
        if transform:
            for i in range(len(source_tokens) - 1):
                edits.append([(shift_idx + i, shift_idx + i + 1), transform])
            return edits
# merge space, merge hyphen ,$MERGE_SWAP
    if len(source_tokens) == len(target_words) == 2:
        # check swap
        transform = check_swap(source_tokens, target_words)
        if transform:
            edits.append([(shift_idx, shift_idx + 1), transform])
    return edits


def is_sent_ok(sent, delimeters=SEQ_DELIMETERS):
    for del_val in delimeters.values():#首先判断这个文本是不是已经做过delimeter处理了.已经做处理的返回false.
        if del_val in sent and del_val != " ":
            return False
    return True


def check_casetype(source_token, target_token):
    if source_token.lower() != target_token.lower():
        return None
    if source_token.lower() == target_token:
        return "$TRANSFORM_CASE_LOWER"
    elif source_token.capitalize() == target_token:
        return "$TRANSFORM_CASE_CAPITAL"
    elif source_token.upper() == target_token:
        return "$TRANSFORM_CASE_UPPER"
    elif source_token[1:].capitalize() == target_token[1:] and source_token[0] == target_token[0]:
        return "$TRANSFORM_CASE_CAPITAL_1"
    elif source_token[:-1].upper() == target_token[:-1] and source_token[-1] == target_token[-1]:
        return "$TRANSFORM_CASE_UPPER_-1"
    else:
        return None


def check_equal(source_token, target_token):
    if source_token == target_token:
        return "$KEEP"
    else:
        return None


def check_split(source_token, target_tokens):
    if source_token.split("-") == target_tokens:
        return "$TRANSFORM_SPLIT_HYPHEN"
    else:
        return None


def check_merge(source_tokens, target_tokens):
    if "".join(source_tokens) == "".join(target_tokens):
        return "$MERGE_SPACE"
    elif "-".join(source_tokens) == "-".join(target_tokens):
        return "$MERGE_HYPHEN"
    else:
        return None


def check_swap(source_tokens, target_tokens):
    if source_tokens == [x for x in reversed(target_tokens)]:
        return "$MERGE_SWAP"
    else:
        return None

from .helpers import  VOCAB_DIR



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

# 跟complex_plural一样.
def check_spelling_mistake(source_token, target_token,spelling_mistake=spelling_mistake):
    spelling_mistake = spelling_mistake
    for i in spelling_mistake:
        if source_token == i and spelling_mistake[i] == target_token:
            return "$TRANSFORM_SPELLING_MISTAKE"
    return None








def check_plural(source_token, target_token,complex_plural=complex_plural):
    if source_token.endswith("s") and source_token[:-1] == target_token:
        return "$TRANSFORM_AGREEMENT_SINGULAR"
    elif target_token.endswith("s") and source_token == target_token[:-1]:
        return "$TRANSFORM_AGREEMENT_PLURAL"
    else:
        # 这里面简历一个词典. 做复杂
        complex_plural=complex_plural
        for i in complex_plural:
            if source_token==i and complex_plural[i]==target_token:
                return "$TRANSFORM_COMPLEX_PLURAL"
        return None


def check_verb(source_token, target_token):
    encoding = encode_verb_form(source_token, target_token)
    if encoding:
        return f"$TRANSFORM_VERB_{encoding}"
    else:
        return None

# 这个函数用来检测   $TRANSFORM_SPLIT_HYPHEN , $Keep, $大小写,
def apply_transformation(source_token, target_token):
    target_tokens = target_token.split()
    if len(target_tokens) > 1:
        # check split
        transform = check_split(source_token, target_tokens)
        if transform:
            return transform  # 需要仿照check_verb来进行修改. 2020-07-07,10点51  先修改check_plural 吧,这个毕竟是代码已经有框架了,直接改即可. 做问题一定要从最容易的开始做,逐渐加难度.
    checks = [check_equal, check_casetype, check_verb, check_plural,check_spelling_mistake]
    for check in checks:
        transform = check(source_token, target_token)
        if transform:
            return transform
    return None


def align_sequences(source_sent, target_sent):
    # check if sent is OK
    if not is_sent_ok(source_sent) or not is_sent_ok(target_sent):
        return None
    source_tokens = source_sent.split()
    target_tokens = target_sent.split()
    matcher = SequenceMatcher(None, source_tokens, target_tokens)
    diffs = list(matcher.get_opcodes())  # 利用库包得到了从第一个句子编导第二个句子的4中变换的细节. 4个操作,增, 删, 改, 等
    all_edits = []   # 上面一行得到的是 op, a1,a2,  b1, b2 这样的数据 后面的编号表示的是切片.[a1:a2]   [b1:b2]   7,7 insert就表示 7后面insert
    for diff in diffs:
        tag, i1, i2, j1, j2 = diff
        source_part = _split(" ".join(source_tokens[i1:i2]))
        target_part = _split(" ".join(target_tokens[j1:j2]))
        if tag == 'equal': # ------------这3中操作: keep,删除,插入这些都是直接建立变换即可. 后续的replace需要复杂讨论.目标是尽可能用g-变换来降低打tag的数量.从而增强模型的鲁棒性.
            continue
        elif tag == 'delete':
            # delete all words separatly
            for j in range(i2 - i1):
                edit = [(i1 + j, i1 + j + 1), '$DELETE']  # 把标识配置到edit数组里面.
                all_edits.append(edit)
        elif tag == 'insert':
            # append to the previous word
            for target_token in target_part:
                edit = ((i1 - 1, i1), f"$APPEND_{target_token}")
                all_edits.append(edit)
        else: # 对于replace 需要进行后续的合并操作. 也就是把replace 替换为g-变换. 降低分类的数量.提高精准度.降低学习难度.
            # check merge first of all
            edits = apply_merge_transformation(source_part, target_part,
                                               shift_idx=i1)  # 返回3中: # merge space, merge hyphen ,$MERGE_SWAP
            if edits:
                all_edits.extend(edits)
                continue
# 进行对齐.
            # normalize alignments if need (make them singleton)        # 处理其他变化------也就是g变换.
            _, alignments = perfect_align(source_part, target_part,
                                          insertions_allowed=0)
            for alignment in alignments:
                new_shift = alignment[2][0]
                edits = convert_alignments_into_edits(alignment,
                                                      shift_idx=i1 + new_shift)
                all_edits.extend(edits)

    # get labels
    labels = convert_edits_into_labels(source_tokens, all_edits)
    # match tags to source tokens
    sent_with_tags = add_labels_to_the_tokens(source_tokens, labels)
    return sent_with_tags


def convert_edits_into_labels(source_tokens, all_edits):
    # make sure that edits are flat
    flat_edits = []
    for edit in all_edits:
        (start, end), edit_operations = edit
        if isinstance(edit_operations, list):
            for operation in edit_operations:
                new_edit = [(start, end), operation]
                flat_edits.append(new_edit)
        elif isinstance(edit_operations, str):
            flat_edits.append(edit)
        else:
            raise Exception("Unknown operation type")
    all_edits = flat_edits[:]
    labels = []
    total_labels = len(source_tokens) + 1
    if not all_edits:
        labels = [["$KEEP"] for x in range(total_labels)]
    else:
        for i in range(total_labels):
            edit_operations = [x[1] for x in all_edits if x[0][0] == i - 1
                               and x[0][1] == i]
            if not edit_operations:
                labels.append(["$KEEP"])
            else:
                labels.append(edit_operations)
    return labels


def convert_alignments_into_edits(alignment, shift_idx):
    edits = []
    action, target_tokens, new_idx = alignment
    source_token = action.replace("REPLACE_", "")

    # check if delete
    if not target_tokens:
        edit = [(shift_idx, 1 + shift_idx), "$DELETE"]
        return [edit]

    # check splits
    for i in range(1, len(target_tokens)):
        target_token = " ".join(target_tokens[:i + 1]) # 把后续的拼接起来,看整体是不是可以一起变换,如果整体一下就过去了,那么我们就使用整体变化, 这里面是贪心的原则!!!!!!!!!!
        transform = apply_transformation(source_token, target_token)
        if transform:# 如果这步找到了变换就可以进入return 逻辑
            edit = [(shift_idx, shift_idx + 1), transform]
            edits.append(edit)
            target_tokens = target_tokens[i + 1:]
            for target in target_tokens:
                edits.append([(shift_idx, shift_idx + 1), f"$APPEND_{target}"])
            return edits

    transform_costs = []
    transforms = []
    # 这里面是单独匹配, 不是上面的整体概念,所以优先级放后面.
    for target_token in target_tokens:
        transform = apply_transformation(source_token, target_token)
        if transform:
            cost = 0
            transforms.append(transform)
        else:
            cost = Levenshtein.distance(source_token, target_token)
            transforms.append(None)
        transform_costs.append(cost)
    min_cost_idx = transform_costs.index(min(transform_costs))
    # append to the previous word
    for i in range(0, min_cost_idx):
        target = target_tokens[i]
        edit = [(shift_idx - 1, shift_idx), f"$APPEND_{target}"]
        edits.append(edit)
    # replace/transform target word
    transform = transforms[min_cost_idx]
    target = transform if transform is not None \
        else f"$REPLACE_{target_tokens[min_cost_idx]}"  # 从这行代码知道, 能用g-变换的尽量用g-变换,否则用replace, 这样就会最大程度上降低tag的数量!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    edit = [(shift_idx, 1 + shift_idx), target]
    edits.append(edit)
    # append to this word
    for i in range(min_cost_idx + 1, len(target_tokens)):
        target = target_tokens[i]
        edit = [(shift_idx, 1 + shift_idx), f"$APPEND_{target}"]
        edits.append(edit)
    return edits


def add_labels_to_the_tokens(source_tokens, labels, delimeters=SEQ_DELIMETERS):
    tokens_with_all_tags = []
    source_tokens_with_start = [START_TOKEN] + source_tokens
    for token, label_list in zip(source_tokens_with_start, labels):
        all_tags = delimeters['operations'].join(label_list)
        comb_record = token + delimeters['labels'] + all_tags
        tokens_with_all_tags.append(comb_record)
    return delimeters['tokens'].join(tokens_with_all_tags)













from utils.set_helper import correct



def convert_data_from_raw_files(source_file, target_file, output_file, chunk_size):
    tagged = []
    source_data, target_data = read_parallel_lines(source_file, target_file)


    source_data=[correct(i) for i in source_data ]
    target_data=[correct(i) for i in target_data ]
    print("补完空格了")











#-----------下面这段是我自己写的. 号补空格算法. 缺陷是对于U.S.A点这种单词没有处理.# 没有,库包都不行,不支持.
    # 把句号前后加上空格.
#     import re
#     for i in range(len(source_data)):
#         tmp = re.sub(r'\.', r' . ', source_data[i]).rstrip() # 先替换.
#         source_data[i] = re.sub(r' +', r' ', tmp).rstrip() # 再替换多余空格
#     for j in range(len(target_data)):
#         # tmp = re.sub(r'\.', r' . ', target_data[i]).rstrip() # 先替换.
#         # target_data[i] = re.sub(r' +', r' ', tmp).rstrip() # 再替换多余空格
# # 还需要控制大小写.
#         old = target_data[j]
#         tmp = re.sub(r'\.', r' . ', old).rstrip()
#         tmp = re.sub(r' +', r' ', tmp).rstrip()
#         old = tmp
#         tmp = re.finditer(r'\. .', tmp)
#         tmp = list(tmp)
#         list3 = []
#         for i in tmp:
#             list3.append(i.span()[-1] - 1)
#         # print(list(tmp))
#         #
#         # print(list3)
#         # print(old)
#         out = ''
#         for i in range(len(old)):
#             if i not in list3:
#                 out += old[i]
#             else:
#                 out += str.upper(old[i])
#         target_data[j]=out
#         # print(out)

# --------------下面开始正式的预处理代码!!!!!!!!!!!!!!!!!!!
    print(f"The size of raw dataset is {len(source_data)}")
    cnt_total, cnt_all, cnt_tp = 0, 0, 0
    for source_sent, target_sent in tqdm(zip(source_data, target_data)): # 耗时的需要做tqdm
        try:
            aligned_sent = align_sequences(source_sent, target_sent)
        except Exception:
            aligned_sent = align_sequences(source_sent, target_sent)
        if source_sent != target_sent:
            cnt_tp += 1
        alignments = [aligned_sent]
        cnt_all += len(alignments)
        try:
            check_sent = convert_tagged_line(aligned_sent)
        except Exception:
            # debug mode
            aligned_sent = align_sequences(source_sent, target_sent)
            check_sent = convert_tagged_line(aligned_sent)

        if "".join(check_sent.split()) != "".join(
                target_sent.split()):
            # do it again for debugging
            aligned_sent = align_sequences(source_sent, target_sent)
            check_sent = convert_tagged_line(aligned_sent)
            print(f"Incorrect pair: \n{target_sent}\n{check_sent}")
            continue
        if alignments:
            cnt_total += len(alignments)
            tagged.extend(alignments)
        if len(tagged) > chunk_size:
            write_lines(output_file, tagged, mode='a')
            tagged = []

    print(f"Overall extracted {cnt_total}. "
          f"Original TP {cnt_tp}."
          f" Original TN {cnt_all - cnt_tp}")
    from pathlib import Path
    output_filedir = Path(__file__).resolve().parent.parent / output_file  # 获取绝对路径的方法
    if tagged:# tagged 就是我们最后需要的文件.
        write_lines(output_filedir, tagged, 'w')


def convert_labels_into_edits(labels):
    all_edits = []
    for i, label_list in enumerate(labels):
        if label_list == ["$KEEP"]:
            continue
        else:
            edit = [(i - 1, i), label_list]
            all_edits.append(edit)
    return all_edits


def get_target_sent_by_levels(source_tokens, labels):
    relevant_edits = convert_labels_into_edits(labels)
    target_tokens = source_tokens[:]
    leveled_target_tokens = {}
    if not relevant_edits:
        target_sentence = " ".join(target_tokens)
        return leveled_target_tokens, target_sentence
    max_level = max([len(x[1]) for x in relevant_edits])
    for level in range(max_level):
        rest_edits = []
        shift_idx = 0
        for edits in relevant_edits:
            (start, end), label_list = edits
            label = label_list[0]
            target_pos = start + shift_idx
            source_token = target_tokens[target_pos] if target_pos >= 0 else START_TOKEN
            if label == "$DELETE":
                del target_tokens[target_pos]
                shift_idx -= 1
            elif label.startswith("$APPEND_"):
                word = label.replace("$APPEND_", "")
                target_tokens[target_pos + 1: target_pos + 1] = [word]
                shift_idx += 1
            elif label.startswith("$REPLACE_"):
                word = label.replace("$REPLACE_", "")
                target_tokens[target_pos] = word
            elif label.startswith("$TRANSFORM"):
                word = apply_reverse_transformation(source_token, label)
                if word is None:
                    word = source_token
                target_tokens[target_pos] = word
            elif label.startswith("$MERGE_"):
                # apply merge only on last stage
                if level == (max_level - 1):
                    target_tokens[target_pos + 1: target_pos + 1] = [label]
                    shift_idx += 1
                else:
                    rest_edit = [(start + shift_idx, end + shift_idx), [label]]
                    rest_edits.append(rest_edit)
            rest_labels = label_list[1:]
            if rest_labels:
                rest_edit = [(start + shift_idx, end + shift_idx), rest_labels]
                rest_edits.append(rest_edit)

        leveled_tokens = target_tokens[:]
        # update next step
        relevant_edits = rest_edits[:]
        if level == (max_level - 1):
            leveled_tokens = replace_merge_transforms(leveled_tokens)
        leveled_labels = convert_edits_into_labels(leveled_tokens,
                                                   relevant_edits)
        leveled_target_tokens[level + 1] = {"tokens": leveled_tokens,
                                            "labels": leveled_labels}

    target_sentence = " ".join(leveled_target_tokens[max_level]["tokens"])
    return leveled_target_tokens, target_sentence


def replace_merge_transforms(tokens):
    if all(not x.startswith("$MERGE_") for x in tokens):
        return tokens
    target_tokens = tokens[:]
    allowed_range = (1, len(tokens) - 1)
    for i in range(len(tokens)):
        target_token = tokens[i]
        if target_token.startswith("$MERGE"):
            if target_token.startswith("$MERGE_SWAP") and i in allowed_range:
                target_tokens[i - 1] = tokens[i + 1]
                target_tokens[i + 1] = tokens[i - 1]
                target_tokens[i: i + 1] = []
    target_line = " ".join(target_tokens)
    target_line = target_line.replace(" $MERGE_HYPHEN ", "-")
    target_line = target_line.replace(" $MERGE_SPACE ", "")
    return target_line.split()


def convert_tagged_line(line, delimeters=SEQ_DELIMETERS):
    label_del = delimeters['labels']
    source_tokens = [x.split(label_del)[0]
                     for x in line.split(delimeters['tokens'])][1:]
    labels = [x.split(label_del)[1].split(delimeters['operations'])
              for x in line.split(delimeters['tokens'])]
    assert len(source_tokens) + 1 == len(labels)
    levels_dict, target_line = get_target_sent_by_levels(source_tokens, labels)
    return target_line


def main(args): # m2 是预处理的核心函数. 输出output.txt
    convert_data_from_raw_files(args.source, args.target, args.output_file, args.chunk_size)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source',
                        help='Path to the source file',
                        required=False)
    parser.add_argument('-t', '--target',
                        help='Path to the target file',
                        required=False)
    parser.add_argument('-o', '--output_file',
                        help='Path to the output file',
                        required=False)
    parser.add_argument('--chunk_size',
                        type=int,
                        help='Dump each chunk size.',
                        default=1000000)

    args = parser.parse_args()



    args.source='wi_loc_src.txt'
    args.target='wi_loc_tgt.txt'
    args.output_file='output.txt'




    main(args)
    '''
    必须先用这个.py, 输入source, target 来提供output, 然后output 再给train.py才行
    其中,source 表示错误句子
    target表示正确句子.
    '''

    '''
    下面说明一下output文件的内容: 以第一个句子为例子:
    
    
    $STARTSEPL|||SEPR$KEEP TwoSEPL|||SEPR$KEEP yearsSEPL|||SEPR$KEEP agoSEPL|||SEPR$KEEP ,SEPL|||SEPR$KEEP PeterSEPL|||SEPR$KEEP 'sSEPL|||SEPR$KEEP fatherSEPL|||SEPR$APPEND_had diedSEPL|||SEPR$APPEND_, soSEPL|||SEPR$KEEP PeterSEPL|||SEPR$KEEP wasSEPL|||SEPR$KEEP theSEPL|||SEPR$KEEP onlySEPL|||SEPR$KEEP oneSEPL|||SEPR$KEEP thatSEPL|||SEPR$KEEP knewSEPL|||SEPR$KEEP whereSEPL|||SEPR$KEEP wasSEPL|||SEPR$DELETE theSEPL|||SEPR$KEEP treehouseSEPL|||SEPR$APPEND_was .SEPL|||SEPR$KEEP
    解释: 第一个$startsepl都是这么写的, 表示句子开始.第二个是keep操作,然后内容是two
    第三个是keep 内容years........低9个是添加操作加had这3个字符,在died前面................在.前面加was, 最后总是写sepr$keep表示句子结尾.
    
    
    
    
    
    
    source:   Two years ago , Peter 's father died so Peter was the only one that knew where was the treehouse .
    
    
    target:  Two years ago , Peter 's father had died , so Peter was the only one that knew where the treehouse was .
    '''