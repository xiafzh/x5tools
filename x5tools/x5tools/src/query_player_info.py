#encoding:UTF-8

from x5tools.lib.db_mysql import *
from x5tools.conf.database_conf import *
from x5tools.src.query_db_info import *
import struct
import datetime


class CPlayerInfoQuerier:
    def __init__(self):
        pass
        
    def query_player_info(self, param):
        param.update(db_param)
        my_conn = DBMysql()
        conn_res, str_res = my_conn.connect(param)
        if not conn_res:
            return gen_responce(CResultCode._ConnectDBFailed)
       
       
        # 默认使用pstid作为hash值，如果是特殊表，用QQ
        value = 0
        if param["table_name"] in special_table \
            and special_table[param["table_name"]].IsTrue("is_qq_key"):
            value = int(param["qq"])
        else:
            pstid_res,pstid = CPlayerInfoQuerier._query_player_pstid_by_qq(param["host"], param["qq"])
            value = pstid
        
        tbres, table_name = CDBInfoQuerier._query_table_name(param, value)
        print(tbres, table_name)
        if not tbres:
            return gen_responce(CResultCode._NoTargetTable)
        
        # 查询主键
        key_res, key_data = my_conn.execute("SELECT column_name FROM INFORMATION_SCHEMA.`KEY_COLUMN_USAGE` WHERE table_name='%s' AND constraint_name='PRIMARY'" % table_name)
        if not key_res:
            return gen_responce(CResultCode._Failed)
        
        if len(key_data) < 1 or len(key_data[0]) != 1:
            return gen_responce(CResultCode._Failed)      
                
        if "columns" in param and len(param["columns"]) > 0:
            qres, qdata = my_conn.execute("select %s from %s where %s=%d" % (",".join(param["columns"]), table_name, key_data[0][0], value))
        else:
            qres, qdata = my_conn.execute("select * from %s where %s=%d" % (table_name, key_data[0][0], value))
        
        res_data = []
        for key in qdata:
            for value in key:
                print(type(value), value)
                if type(value) == bytes:
                    res_data.append(''.join(['%02X' % b for b in value]))
                elif type(value) == datetime:
                    print("datetime", value)
                else:
                    res_data.append(value)
        #print(res_data)
        
        my_conn.close()
        return gen_responce(CResultCode._Success, res_data)
    
    @staticmethod
    def query_player_pstid_by_qq(param):
        param.update(db_param)
        my_conn = DBMysql()
        conn_res, str_res = my_conn.connect(param)
        if not conn_res:
            return gen_responce(CResultCode._ConnectDBFailed)
        
        res, pstid = CPlayerInfoQuerier._query_player_pstid_by_qq(param["host"], param['qq'])
        if not res:
            return gen_responce(CResultCode._Failed)
        
        return gen_responce(CResultCode._Success, pstid)
    
    @staticmethod
    def _query_player_pstid_by_qq(host, qq):
        print(qq)
        my_conn = DBMysql()
        param = {}
        param.update(db_param)
        param.update({"host":host})
        param.update({"database":"star_game"})
        conn_res, str_res = my_conn.connect(param)
        if not conn_res:
            return False, 0
        
        qq_value = int(qq)
        res, account_info = my_conn.execute("select infos from accountinfo_%d where QQ=%d" % (qq_value % 128, qq_value))
        my_conn.close()
        if len(account_info) <= 0 or len(account_info[0]) <= 0 or len(account_info[0][0]) <= 8:
            return False, 0
        #print(account_info)
        (pstid,) = struct.unpack("<Q", bytearray(account_info[0][0][0:8]))
        
        return True, pstid
        


