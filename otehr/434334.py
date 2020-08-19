#!/usr/bin/python3
# -*- coding: UTF-8 -*-

__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'

import re
from w3lib.html import *


def go_remove_tag(value):
    # 移除标签
    content = remove_tags_with_content(value,'script')
    # 移除空格 换行
    return re.sub(r'[\t\r\n\s]', '', content)


if __name__ == '__main__':
    html = """<div class="text"><script></script>
    <p>“感谢大家，因为有了你们才使我重回这激情燃烧的时代。”<br></p>
    <p>在加盟数梦工场的发言中，吴敬传首先向这支年轻的创业团队致谢。正是这样一群志同道合的人唤醒了她的数据强国梦，一同踏上新的征程。而此时，身着牛仔裤、T恤衫的吴敬传一改昔日“铁娘子”的庄重，多了几分仗剑闯天涯的洒脱。</p>
    <p>吴敬传的新身份是数梦工场董事长兼CEO。“新”是这个时代的特征，从IT到DT，从商业互联网到新型互联网，从“互联网+”到数字经济……在万象更新中，当人与时代同处变革潮头的时候，梦想和激情的碰撞也就成了必然。</p><h5>
    <strong>十二年一个轮回，创业者回归初心</strong></h5>
    <p>2004年，吴敬传从深圳来到杭州。当时，这一代人肩负打破国外网络厂商垄断市场的重任，成为中国网络基础设施领域的拓荒者。</p>
    <p>“十二年过后，当我再一次踏上杭州这块热土——我称之为我的第二故乡，我的使命，我的愿景，是希望引领着一群逐梦的人，在这个世界留下我们的印记，为社会做一点有意义和有价值的事情——用数据服务世界。”吴敬传说。</p>
    <p>
        有时候，使命是个略显宏大而飘渺的词。这些由使命感驱动的创业者被称为梦想家，他们身上的理想主义光环总会吸引很多人，但创业者本身如果沉迷于被关注、记录和颂扬，或者沉迷于过往的人脉、地位和成就，往往难负使命与担当。吴敬传用“初学之心”来引导自己和团队的心态，意味着不管你过去积累了多少经验，不管过去有多么辉煌，但是在今天，都要学会摒弃，要有一颗能够承载得住未来所学东西的“初学之心”。</p>
    <p>
        当然，回归初心并不意味着摒弃一切，对吴敬传而言，她需要做的是通过认知和管理的革新，将IT时代的实践经验科学地转化成符合DT时代所需的领导力，领导数梦工场通过组织架构和流程的变革，生产资料的转换，成为DT时代的领航者。这里包含两个核心变化：首先，数据将成为DT时代新的生产资料、新的能源；其次，IT是有中心的，而DT架构恰恰是去中心化。吴敬传认为，IT是以垂直内部管理为主，从某种意义上讲，IT横向打通和升级是相当困难的。</p>
    <p>
        有了这两个基本认识，吴敬传给数梦工场的定位便清晰起来——做一家新型互联网公司，在政务互联网、产业互联网、城市互联网三大领域持续创新和实践。为了保持公司创新的氛围，她选择更加扁平化、年轻化的管理方式，“互联网企业是一种敏捷的文化，是一种快速迭代，共享、共通、共融的文化。我要改变过去一些传统企业或者过去的IT企业里面层级过多，层层汇报的情况。”她笑称，“创业自动减龄12岁。”另一方面，吴敬传要求自己的工程师深入到一线场景、用户场景中，针对每个领域的痛点提供全栈式解决方案，围绕用户需求挖掘背后的数据价值。很多时候，惯性思维甚至会成为创新的障碍。离开舒适区，以归零心态拥抱变化，探索者才能保持创新的敏锐性，激发创新的潜能。吴敬传在办公室放置梁启超的话以自勉——不惮以今日之我挑战昔日之我，便是这种心境的真实写照。</p>
    <p><img class="picture" src="http://images.enet.com.cn/i/2017/0609/100919866.jpg" title="i/2017/0609/100919866.jpg"
            alt="人物-目录.jpg"></p><h5><strong>蓄势兴业宏图展，满园鋆色尽朝晖</strong></h5>"""

    content = go_remove_tag(html)
    print(content)