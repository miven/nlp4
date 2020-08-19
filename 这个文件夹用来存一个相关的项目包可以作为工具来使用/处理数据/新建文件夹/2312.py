
criterion = lambda row: row['企业名称'] not in tmp2['ent_name']
tmp=tmp.apply(criterion,axis=1)
