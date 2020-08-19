"""Tweaked AllenNLP dataset reader."""
import logging
import re
from random import random
from typing import Dict, List

from allennlp.common.file_utils import cached_path
from allennlp.data.dataset_readers.dataset_reader import DatasetReader
from allennlp.data.fields import TextField, SequenceLabelField, MetadataField, Field
from allennlp.data.instance import Instance
from allennlp.data.token_indexers import TokenIndexer, SingleIdTokenIndexer
from allennlp.data.tokenizers import Token
from overrides import overrides

from utils.helpers import SEQ_DELIMETERS, START_TOKEN

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


@DatasetReader.register("seq2labels_datareader")
class Seq2LabelsDatasetReader(DatasetReader):
    """
    Reads instances from a pretokenised file where each line is in the following format:
# 这个文件是
    WORD###TAG [TAB] WORD###TAG [TAB] ..... \n

    and converts it into a ``Dataset`` suitable for sequence tagging. You can also specify
    alternative delimiters in the constructor.

    Parameters
    ----------
    delimiters: ``dict``
        The dcitionary with all delimeters.
    token_indexers : ``Dict[str, TokenIndexer]``, optional (default=``{"tokens": SingleIdTokenIndexer()}``)
        We use this to define the input representation for the text.  See :class:`TokenIndexer`.
        Note that the `output` tags will always correspond to single token IDs based on how they
        are pre-tokenised in the data file.
    max_len: if set than will truncate long sentences
    """
    # fix broken sentences mostly in Lang8
    BROKEN_SENTENCES_REGEXP = re.compile(r'\.[a-zA-RT-Z]')

    def __init__(self,
                 token_indexers: Dict[str, TokenIndexer] = None,
                 delimeters: dict = SEQ_DELIMETERS,
                 skip_correct: bool = False,
                 skip_complex: int = 0,
                 lazy: bool = False,
                 max_len: int = None,
                 test_mode: bool = False,
                 tag_strategy: str = "keep_one",
                 tn_prob: float = 0,
                 tp_prob: float = 0,
                 broken_dot_strategy: str = "keep") -> None:
        super().__init__(lazy) # lazy一般都是true,保证节省内存
        self._token_indexers = token_indexers or {'tokens': SingleIdTokenIndexer()}
        self._delimeters = delimeters
        self._max_len = max_len
        self._skip_correct = skip_correct
        self._skip_complex = skip_complex
        self._tag_strategy = tag_strategy
        self._broken_dot_strategy = broken_dot_strategy
        self._test_mode = test_mode
        self._tn_prob = tn_prob
        self._tp_prob = tp_prob

    @overrides    # 看看这个里面的read如何读取数据,看看到底数据怎么tigong.
    def _read(self, file_path):
        # if `file_path` is a URL, redirect to the cache
        file_path = cached_path(file_path)
        with open(file_path, "r") as data_file:
            logger.info("Reading instances from lines in file at: %s", file_path)
            for line in data_file:
                line = line.strip("\n") # 首先删除最后没用的回车符号
                # skip blank and broken lines
                if not line or (not self._test_mode and self._broken_dot_strategy == 'skip'
                                and self.BROKEN_SENTENCES_REGEXP.search(line) is not None):
                    continue
# 找到X,y
                tokens_and_tags = [pair.rsplit(self._delimeters['labels'], 1)  # 表示符是'SEPL|||SEPR'
                                   for pair in line.split(self._delimeters['tokens'])] # 左边X, 右边y
                try:
                    tokens = [Token(token) for token, tag in tokens_and_tags]
                    tags = [tag for token, tag in tokens_and_tags] #就看做一个多酚类问题.
                except ValueError:
                    tokens = [Token(token[0]) for token in tokens_and_tags]
                    tags = None

                if tokens and tokens[0] != Token(START_TOKEN): # 如果一行的表示缺少了开始标签,那么我们就把他补上.一般来说不会缺.
                    tokens = [Token(START_TOKEN)] + tokens

                words = [x.text for x in tokens]
                if self._max_len is not None:
                    tokens = tokens[:self._max_len] # 做句子截取. 50个单词一个句子够了. 这个50参数后续可以调整.
                    tags = None if tags is None else tags[:self._max_len]
                instance = self.text_to_instance(tokens, tags, words)
                if instance:
                    yield instance

    def extract_tags(self, tags: List[str]):
        op_del = self._delimeters['operations'] # 操作的分隔符

        labels = [x.split(op_del) for x in tags]

        comlex_flag_dict = {}
        # get flags
        for i in range(5):
            idx = i + 1
            comlex_flag_dict[idx] = sum([len(x) > idx for x in labels]) # sum 返回里面有多少个True

        if self._tag_strategy == "keep_one":
            # get only first candidates for r_tags in right and the last for left
            labels = [x[0] for x in labels] # 只保留第一个.
        elif self._tag_strategy == "merge_all":
            # consider phrases as a words
            pass
        else:
            raise Exception("Incorrect tag strategy")

        detect_tags = ["CORRECT" if label == "$KEEP" else "INCORRECT" for label in labels]
        return labels, detect_tags, comlex_flag_dict

    def text_to_instance(self, tokens: List[Token], tags: List[str] = None,
                         words: List[str] = None) -> Instance:  # type: ignore
        """
        We take `pre-tokenized` input here, because we don't have a tokenizer in this class.
        """
        # pylint: disable=arguments-differ
        fields: Dict[str, Field] = {}
        sequence = TextField(tokens, self._token_indexers)
        fields["tokens"] = sequence
        fields["metadata"] = MetadataField({"words": words})
        if tags is not None:
            labels, detect_tags, complex_flag_dict = self.extract_tags(tags)
            if self._skip_complex and complex_flag_dict[self._skip_complex] > 0: # complex_flag_dict 表示迭代第i次,时候还有几个处理不完的token.这行为true, 就表示
                return None
            rnd = random()
            # skip TN
            if self._skip_correct and all(x == "CORRECT" for x in detect_tags): # 跳过正确的例子,按照一定比例不去训练.这里设置为0,1就好了,还是都训练.
                if rnd > self._tn_prob:
                    return None
            # skip TP
            else:
                if rnd > self._tp_prob:
                    return None

            fields["labels"] = SequenceLabelField(labels, sequence,
                                                  label_namespace="labels")
            fields["d_tags"] = SequenceLabelField(detect_tags, sequence,
                                                  label_namespace="d_tags")
        return Instance(fields)
