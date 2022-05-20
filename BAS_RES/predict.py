from BAS_RES_test import BASRESpredict
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

predict = BASRESpredict()
# predict.setfilepath("https://wx-miniprogram-picture-1302593558.cos.ap-chengdu.myqcloud.com/146_1.png")
predict.setfilepath(
    "https://wx-miniprogram-picture-1302593558.cos.ap-chengdu.myqcloud.com/%E5%BE%AE%E4%BF%A1%E7%94%A8%E6%88%B7bacd5.png")
print(predict.predict())
