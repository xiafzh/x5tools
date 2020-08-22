#encoding:utf-8
from x5tools.lib.db_mysql import *
from x5tools.src.gen_result import *
from x5tools.conf.database_conf import *
import re

class CDBInfoQuerier:
    def __init__(self):
        pass
        
    @staticmethod
    def query_all_database(param):
        param.update(db_param)
        my_conn = DBMysql()
        conn_res, str_res = my_conn.connect(param)
        if not conn_res:
            return gen_responce(CResultCode._ConnectDBFailed)
                
        query_result, all_db = my_conn.execute("show databases");
        my_conn.close()
        
        if not query_result:
            return gen_responce(CResultCode._ExecuteSqlFailed)
        
        res_data = []
        for db_tuple in all_db:
            for db_name in db_tuple:
                if CDBInfoQuerier._is_match(db_name):
                    #print(db_name)
                    res_data.append(db_name)
    
        return gen_responce(CResultCode._Success, res_data)
    
    @staticmethod
    def query_all_table_in_db(param):
        param.update(db_param)
        my_conn = DBMysql()
        conn_res, str_res = my_conn.connect(param)
        if not conn_res:
            return gen_responce(CResultCode._ConnectDBFailed)
        
        query_result, all_table = my_conn.execute("show tables");
        my_conn.close()
        
        res_data = []
        for table_tuple in all_table:
            for table_name in table_tuple:
                re_match = re.search("_[0-9]{1,4}$", table_name)
                #print(table_name, re_match)
                if None == re_match:
                    if table_name not in res_data:
                        res_data.append(table_name)
                else:
                    re_span = re_match.span()
                    table_name = table_name[0:re_span[0]]
                    if table_name not in res_data:
                        res_data.append(table_name)
                        
        return gen_responce(CResultCode._Success, res_data)
    
    def query_all_columns_in_table(param):
        param.update(db_param)
        my_conn = DBMysql()
        conn_res, str_res = my_conn.connect(param)
        if not conn_res:
            return gen_responce(CResultCode._ConnectDBFailed)
        
        # 随便找一张表就可以
        table_res, table_name = CDBInfoQuerier._query_table_name(param, 0)
        if not table_res:
            return gen_responce(CResultCode._NoTargetTable)
        
        col_res, col_data = my_conn.execute("SELECT column_name FROM information_schema.columns WHERE table_name='%s';" % table_name)
        if not col_res:
            return gen_responce(CResultCode._Failed)
            
        ret_data = []
        for key in col_data:
            for col_name in key:
                ret_data.append(col_name)
        
        return gen_responce(CResultCode._Success, ret_data)

    
    @staticmethod
    def _query_table_name(param, value):
        if "table_name" not in param:
            return False, ""        
        param.update(db_param)
        print(param)
        my_conn = DBMysql()
        conn_res, str_res = my_conn.connect(param)
        if not conn_res:
            return False, ""
        
        query_table_name = param["table_name"]
        print("show tables like '%s%%'" % query_table_name)
        query_result, all_table = my_conn.execute("show tables like '%s%%'" % query_table_name);
        my_conn.close()
        if not query_result:
            return False, ""
        
        #print(all_table)
        res_data = []
        for table_tuple in all_table:
            for table_name in table_tuple:
                if table_name == query_table_name:
                    res_data.append(table_name)
                elif None != re.match("^%s_[0-9]{1,4}$" % query_table_name, table_name):
                    res_data.append(table_name)
        
        table_count = len(res_data)
        #print(table_count)
        if table_count <= 1:
            return True, query_table_name
        else:
            if query_table_name in res_data:
                table_count -= 1
            
            if query_table_name in special_table \
                and special_table[query_table_name].IsTrue("is_hash64"):
                return True, "%s_%d" % (query_table_name, CDBInfoQuerier._calc_hash_64(value) % table_count)
            else:
                return True, "%s_%d" % (query_table_name, value % table_count)
        
        return False, ""
    
    @staticmethod
    def _is_match(db_name):
        for str in dbname_restr:
            if re.match(str, db_name):
                return True
        return False
        
    @staticmethod
    def _calc_hash_64(value):
        return ((value >> 32) & 0xFFFFFFFF) ^ (value & 0xFFFFFFFF)
        