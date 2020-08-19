# -*- coding:utf-8 -*-
import os
import sys
import json
import xml.dom.minidom
from xml.dom.minidom import parse


def parse_book(book_xml, book_json, book_title = ""):
    """解析主要思想为：将读取到的正文-译文段落暂存为字符串，遇到特殊标签时，存放到列表中，
       若遇到下一个标题时，将完整的篇章(字符串)列表保存到篇章字典中，并最终保存到pages列表中"""
    # 使用minidom解析器打开 XML 文档
    #print(book_json)
    book_title=book_json.split('.')[-2].split('/')[-1]
    #print(888888888,book_title)
    DOMTree = parse(book_xml)
    rootNode = DOMTree.documentElement
    #rootNode = DOMTree.getElementsByTagName("语料")

    page = {} #篇章字典，存放篇章内容
    pages = [] # 存放所有篇章内容

    # 标题类型:卷次、卷标题、章标题、篇标题、节标题（译文标题）
    # 古文、译文段落类型：正文
    volume_id = ""
    volume_title = ""
    page_title = ""
    chapter_title = ""
    section_title = ""
    page_contentParts = [] # 存放正文内容
    content = {"old":"","new":""}
    flush = 0 # 是否将内容保存到字典中
    para_data = "" # 指明是否有内容未存放到列表中
    content_i = 0  # 指明接下来段落是否为要读取的古文或译文
    language_i = 1  # 接下来段落语言类型

    def save_tmp():
        page = {}
        if len(content['new']) > 2:
            if len(content['old']) > 2:
                page_contentParts.append(content)
            elif len(page_contentParts) > 0:
                page_contentParts[-1]['new'] += content['new']
            #content = {"古":"","今":""}
        #print(page_contentParts)
        if len(page_contentParts) != 0:
            page['book_title'] = book_title
            page['volume_id'] = volume_id
            page['volume_title'] = volume_title
            page['chapter_title'] = chapter_title
            page['page_title'] = page_title
            page['section_title'] = section_title
            page['page_contentParts'] = page_contentParts 
            pages.append(page)

    def read_para1():
        nonlocal language_i, content_i, content, para_mode
        # 下一部分的古文没有明确的标签指示开始，将标签<正文>指示开始
        if len(paras) != 0:
            for ii,para in enumerate(paras):
                if para.nodeName == "正文" and para.getAttribute("type") == "":
                    content_i = 1
                    language_i = 0
                    if old_language_i == 1:
                        if len(content['new']) > 2:
                            if len(content['old']) > 2:
                                page_contentParts.append(content)
                            elif len(page_contentParts) > 0:
                                page_contentParts[-1]['new'] += content['new']
                        content = {"old":"","new":""}
                    break
        if content_i < 1:
            return
        para_data = ""
        # 读取“段落-正文”标签下的内容
        for para in paras:
            if para.nodeName == "正文":
                typet = para.getAttribute("type")
                para_data += ''.join([n.data for n in para.childNodes if n.nodeType == 3])
            if para_data == "":
                if para.nodeName == "正文":
                    for para in para.childNodes:
                        para_data += ''.join([n.data for n in para.childNodes if n.nodeType == 3])

        for para in paras:
            para_modes = ["注文", "注释"]
            if (language_i == 1) and (para_mode >1):
                if para.nodeName == para_modes[para_mode-2]:
                    para_data += ''.join([n.data for n in para.childNodes if n.nodeType == 3])
                if para_data == "":
                    if para.nodeName == para_modes[para_mode-2]:
                        for para in para.childNodes:
                            para_data += ''.join([n.data for n in para.childNodes if n.nodeType == 3])
        if language_i == 0:
            content['old'] += para_data
        else:
            content['new'] += para_data

    def read_para2():
        nonlocal language_i, content_i, content, para_mode
        if content_i < 1:
            return
        para_data = ""
        # “古文”和“今问”混用“正文”标签，即<正文>
        for para in paras:
            if para.nodeName == "正文":
                para_data += ''.join([n.data for n in para.childNodes if n.nodeType == 3])
            if para_data == "":
                if para.nodeName == "正文":
                    for para in para.childNodes:
                        para_data += ''.join([n.data for n in para.childNodes if n.nodeType == 3])
        if language_i == 0:
            content['old'] += para_data
        else:
            content['new'] += para_data

    def read_para3():
        nonlocal language_i, content_i, content, para_mode
        # 没有明确的“译文-标题”
        if len(paras) != 0:
            for ii,para in enumerate(paras):
                if para.nodeName == "正文" and para.getAttribute("type") == "2":
                    # "【译文】" in para.childNodes[1].childNodes[0].data
                    #print(para_data,para.getAttribute("type"),para.childNodes[0])
                    if para.childNodes[0].nodeType == 3:
                        if "【" in para.childNodes[0].data[:1]:
                            if ("译文】" in para.childNodes[0].data) :
                                content_i = 1
                                language_i = 1
                            else:
                                content_i = 0
                        break
        if content_i < 1:
            return 
        para_data = ""
        # 读取“段落-正文”标签下的内容
        for para in paras:
            if para.nodeName == "正文":
                para_data += ''.join([n.data for n in para.childNodes if n.nodeType == 3])
            if para_data == "":
                if para.nodeName == "正文":
                    for para in para.childNodes:
                        para_data += ''.join([n.data for n in para.childNodes if n.nodeType == 3])
        if language_i == 0:
            content['old'] += para_data
        else:
            para_data = para_data.replace("【译文】","")
            content['new'] += para_data
    
    # 判断“译文-标题”的标签及“译文-段落”类型
    
    
    
    def parse_jy( book_title = ""):
        """当xml文件中存在“标题-译文”标签且译文段落标签为“正文”时，才进行篇章匹配"""
        # 使用minidom解析器打开 XML 文档

        #rootNode = DOMTree.getElementsByTagName("语料")

        language_i, language_ii, para_tag =0,0,0
        para_mode = 1
        for ci, cnode in enumerate(rootNode.childNodes):
            if cnode.nodeName == "标题":
                typet = cnode.getAttribute("type")
                if typet == "校注标题":
                    tmp = cnode.childNodes[0].data
                    if '译文' in tmp:
                        language_i = 1
                        language_ii = 1
            elif cnode.nodeName == "段落":
                paras = cnode.childNodes
                if (language_ii == 1):
                    if len(paras) > 0:
                        for para in paras:
                            if para.nodeName == "正文" and para.getAttribute("type") == "2":
                                para_tag = 1
                                para_mode = 1             
                                break   
                            if para.nodeName == "注文":
                                para_tag = 1
                                para_mode = 2             
                                break
                            if para.nodeName == "注释":
                                para_tag = 1
                                para_mode = 3             
                                break
       
                    language_ii = 0
        #print("xml文件标签测试：%s，“标题-译文”标签：%s，“标题-译文”标签 + “段落-正文”标签：%s 。"%(book_xml, language_i, para_tag))
        return language_i, para_tag, para_mode
        
        
        
    
    
    
    
    
    
    now_title, para_tag, para_mode = parse_jy()
    if (now_title == 1) and (para_tag == 1):
        read_para = read_para1
    elif (now_title == 1) and (para_tag == 0):
        read_para = read_para2
    else:
        read_para = read_para3
                
    for ci, cnode in enumerate(rootNode.childNodes):
        if cnode.nodeName == "标题":
            typet = cnode.getAttribute("type")
            cnode_data = ''.join([n.data for n in cnode.childNodes if n.nodeType == 3])
            # 若标题类型为:卷次、卷标题、章标题、篇标题、节标题，表明接下来的“段落-正文”为古文
            if typet == "卷次":
                if volume_id != "":
                    save_tmp()
                    content = {"old":"","new":""}
                    page_contentParts = []
                    volume_id = ""
                    volume_title = ""
                    page_title = ""
                    chapter_title = ""
                    section_title = ""
                volume_id = cnode_data
                content_i = 1
                language_i = 0
                flush = 1
            if typet == "卷标题":
                if volume_title != "":
                    save_tmp()
                    content = {"old":"","new":""}
                    page_contentParts = []
                    volume_title = ""
                    page_title = ""
                    chapter_title = ""
                    section_title = ""
                volume_title = cnode_data
                content_i = 1
                language_i = 0
                flush = 1
            if typet == "章标题":
                if chapter_title != "":
                    save_tmp()
                    content = {"old":"","new":""}
                    page_contentParts = []
                    page_title = ""
                    section_title = ""
                chapter_title = cnode_data
                content_i = 1
                language_i = 0
                flush = 1
            if typet == "篇标题":
                if page_title != "":
                    save_tmp()
                    content = {"old":"","new":""}
                    page_contentParts = []
                    section_title = ""
                page_title = cnode_data
                content_i = 1
                language_i = 0
                flush = 1
            if typet == "节标题":
                if section_title != "":
                    save_tmp()
                    content = {"old":"","new":""}
                    page_contentParts = []
                section_title = cnode_data
                content_i = 1
                language_i = 0
                flush = 1
            # 将临时保存的正文内容保存到字典中

            # 若遇到标题为译文标题，指明接下来段落为译文
            # 若遇到其他校注标题，将现有的正文-译文字符串存储到列表中
            if typet == "校注标题":
                tmp = cnode_data
                if ('译文' in tmp) or ('今译' in tmp):
                    language_i = 1
                    content_i = 1
                elif language_i == 1:
                    if len(content['new']) > 2:
                        if len(content['old']) > 2:
                            page_contentParts.append(content)
                        elif len(page_contentParts) > 0:
                            page_contentParts[-1]['new'] += content['new']
                        content_i = 0
                    content = {"old":"","new":""}
        elif cnode.nodeName == "段落":
            paras = cnode.childNodes
            old_language_i = language_i
            # 若遇到特殊标签<段落/>，将现有的正文-译文字符串存储到列表中
            if len(paras) == 0:
                language_i = 0
                content_i = 1
                if len(content['new']) > 2:
                    if len(content['old']) > 2:
                        page_contentParts.append(content)
                    elif len(page_contentParts) > 0:
                        page_contentParts[-1]['new'] += content['new']
                content = {"old":"","new":""}
            read_para()

            
    # 存放最后一个篇章内容
    if len(content['new']) > 2:
        if len(content['old']) > 2:
            page_contentParts.append(content)
        elif len(page_contentParts) > 0:
            page_contentParts[-1]['new'] += content['new']
    page['book_title'] = book_title
    page['volume_id'] = volume_id
    page['volume_title'] = volume_title
    page['page_title'] = page_title
    page['page_contentParts'] = page_contentParts 
    pages.append(page)
    with open(book_json, 'w',encoding='utf-8') as f:
        json.dump(pages, f,ensure_ascii = False)
    return len(pages)
    # json.dump(book_json,pages)
    # fw = open(book_json, 'w', encoding = 'utf8')
    # for page in pages:
    #     fw.write(page + '\n')
    # fw.close()
#
#
#
# parse_book("古文观止.xml","dasfadsfasdf.json")