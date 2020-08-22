#encoding:utf-8
from x5tools.lib.db_mysql import *
from x5tools.src.gen_result import *
from x5tools.conf.database_conf import *
import re

class CCommonTools:
    def __init__(self):
        pass
    @staticmethod
    def entry(param):
        if "sub_type" not in param:
            return gen_responce(CResultCode._Failed)
        if param["sub_type"] == 1:
            return CCommonTools.TransServerGID(param)
    
        return gen_responce(CResultCode._Failed)
    
    @staticmethod
    def TransServerGID(param):
        if "server_gid" not in param:
            return gen_responce(CResultCode._Failed)
        
        server_gid = int(param["server_gid"])
        
        server_id = server_gid & 0xFFFF
        server_type = (server_gid >> 16) & 0xFF
        server_zone = (server_gid >> 24) & 0xFF
        
        ret_data = {"server_id":server_id, "group_id":server_zone, "server_type":server_type}
        return gen_responce(CResultCode._Success, ret_data)