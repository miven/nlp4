import configparser

config = configparser.ConfigParser()
config.read('properties.conf')
lists_header = config.sections()



tmp=config['ports']['ports']

'''
FROM tenant0202.hub-ark-hn.jdcloud.com/library/centos:7.3 RUN yum -y install centos-release-gluster41 && yum -y install glusterfs-server




'''