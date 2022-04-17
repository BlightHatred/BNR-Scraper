#!/usr/bin/env python
# coding: utf-8

# In[1]:

from  configparser import ConfigParser
import os
import sys 

filename = os.path.join(sys.path[0], 'config.ini')

def read_config(filename='config.ini', section='mysql'):
    parser = ConfigParser()
    parser.read(filename)

    db_config = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
           db_config[item[0]] = item[1]
    else:
        raise Exception(f'{section} not found in the {filename} file')
    

    
    
    return db_config



# In[ ]:




