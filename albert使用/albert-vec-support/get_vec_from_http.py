#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import json

# 请求地址
url = "http://127.0.0.1:7777/vector"
# 请求头，务必正确，否则无法返回正确结果
headers = {
    "Content-Type": "application/json"
}

# 根据输入类的要求构建数据
dict_input = dict()
# 要生成向量的文本
dict_input["text"] = "自然语言 处理 后台"
# 设定有效长度，如为负数则按照有效字符个数处理
# 如小于实际长度则截取前validLength个字符，大于实际长度自动补充[PAD]
# 大于510个有效字符，自动截取前510个有效字符
dict_input["validLength"] = 510

# 发送post请求
ret = requests.post(url=url, json=dict_input, headers=headers)
# 获得反馈后json解码为Python词典
dict_ret = json.loads(ret.text)

# 取原始输入文本
raw_text = dict_ret["rawText"]

# 取原始输入有效长度
raw_valid_length = dict_ret["rawValidLength"]

# 取实际处理的有效文本
text = dict_ret["text"]

# 取实际处理有效长度
valid_length = dict_ret["validLength"]

# 取生成向量
vector = dict_ret["vector"]

# 输出结果
print("----------- ")
print("原始输入文本：" + raw_text)
print("原始输入长度：" + str(raw_valid_length))
print("实际处理文本：" + text)
print("实际处理长度：" + str(valid_length))
print("ALBERT 向量 %d 维：\n" % len(vector) + str(vector))
print("-----------")
