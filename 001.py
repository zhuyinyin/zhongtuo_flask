# from utils.common import json2dict

# print(json2dict({"data":123}))
import pandas as pd
import numpy as np
# 特征值 目标值 测试及集比例
from sklearn.model_selection import train_test_split

x_tran, x_test, y_tran, y_test = train_test_split(x, y,test_size=0.25 )
d = train_test_split()