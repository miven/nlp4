import re
tmp=re.search(r'[\u4e00-\u9fa5]{1,3} *发? *(\〔|\[)[0-9]{4}(\]|〕)[0-9]*? *号', "济经信中小企业字〔2018〕32号")
tmp=re.sub(r'[:[} \f\r\t\v。]', "",  "    dsaf   dsf  dsf\ndsf ")



def chaxunshijian( tmp) :
    tmp1 = re.search(r'自.*年.*月.*日起.*有效期至.*年.*月.*日', tmp)

    if tmp1 :
        res = re.findall(r'[1-2][0-9]{3} *年 *[0-1]?[0-9] *月[0-3]?[0-9] *日', tmp)
        # res = re.findall('日', tmp)

        if len(res) >= 2 :
            return res
    return None








# re.sub(r'[:[}]', '_', testStr)