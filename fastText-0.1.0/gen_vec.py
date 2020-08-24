# -*- coding: utf-8 -*-
import os
import time
import optparse

#root_dir = '/opt/non_patent/data/'
p = optparse.OptionParser()
p.add_option('--root_file', '-r')
p.add_option('--input_file', '-i')
p.add_option('--output_dir', '-o')
options, arguments = p.parse_args()
root_dir = options.root_file
input_dir = root_dir + options.input_file
output_dir = root_dir + options.output_dir


cmd = "./fasttext skipgram -input %s -output %s -lr 0.1 -dim 100 -ws 5 -epoch 5 -minCount 2\
 -neg 5 -wordNgrams 3 -loss 'ns' -bucket 2000000 -minn 0 -maxn 0 -thread 35" %(input_dir, output_dir) 
print(cmd)
os.system(cmd)
