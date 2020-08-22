#encoding:utf-8

from x5tools.src.query_player_info import *
from x5tools.src.query_db_info import *
from x5tools.src.gen_result import *
from x5tools.src.common_tools import *

def entry(param):
    if "opt_type" not in param:
        return gen_responce(CResultCode._Failed)
    if param["opt_type"] == 10000:
        return CCommonTools.entry(param)   
    elif param["opt_type"] == 10001:    
        if "sub_type" not in param:
            return gen_responce(CResultCode._Failed)
        querier = CPlayerInfoQuerier()
        if param["sub_type"] == 1:
            return querier.query_player_info(param)
        elif param["sub_type"] == 2:
            return CPlayerInfoQuerier.query_player_pstid_by_qq(param)
    elif param["opt_type"] == 10002:
        if "sub_type" not in param:
            return gen_responce(CResultCode._Failed)
        if param["sub_type"] == 1:
            return CDBInfoQuerier.query_all_database(param)
        elif param["sub_type"] == 2:
            return CDBInfoQuerier.query_all_table_in_db(param)
        elif param["sub_type"] == 3:
            return CDBInfoQuerier.query_all_columns_in_table(param)
    
    return gen_responce(CResultCode._Failed)
