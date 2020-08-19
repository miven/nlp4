#!/bin/sh
##需要再项目中建立这个文件,来进行云翼上线.
#set -x
#
#mkdir output
#mkdir output/logs
#mkdir output/conf
#echo 'cp file'
#ls
#pwd
##python 代码的编译过程就是复制代码到一个目录.
#cp -r ./skywing output/
#cp -r ./ /output
##cp -r ./skywing output/
#
#







{ # try
rm -rf output
    mkdir -p output
    #save your output

} || { echo "mkdir"
}


{ # try
rm -rf output
cp -r ./bin/* output/bin/
    #save your output

} || { echo "1"
}


{ # try

  cp -r . output/
    #save your output

} || { echo "2"
}






