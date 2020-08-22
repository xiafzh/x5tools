#encoding:utf-8


class CResultCode:
    _NoTargetTable = -4,    # 没有找到目标数据表
    _ExecuteSqlFailed = -3, # 执行sql错误
    _ConnectDBFailed = -2,  # 连接数据库失败
    #############失败的错误码递减，往上边加##############
    _Failed = -1            # 默认的失败
    _Success = 0            # 默认的成功
    #############有特殊含义的成功递增，往下边加###########
    
def gen_responce(code, data = ""):
    return {"res_code":code, "res_data":data}
