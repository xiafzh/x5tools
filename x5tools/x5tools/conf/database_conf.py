#encoding:utf-8


class CSpecialTableInfo:
    def __init__(self, **param):
        self.param = param
    
    def __str__(self):
        return self.param.__str__()
    
    def IsTrue(self, key):
        if key not in self.param:
            return False
        
        return self.param[key]

#初始化一些特殊的表
# is_hash64: 使用64位整型特殊的hash方式 calc_hash_64
# is_qq_key: 使用QQ作为主键，默认是使用pstid
special_table = {
    "player_activity2017_data":CSpecialTableInfo(is_hash64 = True),
    "accountinfo":CSpecialTableInfo(is_qq_key = True),
    "app_pocket_roleinfo":CSpecialTableInfo(is_qq_key = True),
    "x5app_openidtovqq":CSpecialTableInfo(is_qq_key = True),
}

# 数据库名正则匹配串
dbname_restr = ("star_.*", "global_.*", "video_.*")

db_param = {"user":"hardcore", "password":"111111"}
