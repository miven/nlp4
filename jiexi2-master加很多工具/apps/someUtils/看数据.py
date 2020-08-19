import pandas as pd

tmp=pd.read_csv('output.csv')


#
#       )
tmp.drop(['fei','Unnamed: 0_x'],axis=1,inplace=True)



tmp.to_csv('out2.csv')