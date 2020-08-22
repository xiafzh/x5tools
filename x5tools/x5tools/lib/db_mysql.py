#coding:UTF-8

import pymysql

#可用连接参数
compulsory_param = ("host", "user", "password")
optional_param = ("database", "charset", "port", "charset")

class DBMysql:
    def __init__(self):
        self.db = None
        
    def connect(self, param) :
        conn_param = {}
        for key in compulsory_param:
            if key not in param:
                return False, "%s is compulsory" % key
            conn_param.update({key:param[key]})
        
        for key in optional_param:
            if key not in param:
                continue
            conn_param.update({key:param[key]})
        try:
            self.db = pymysql.connect(**conn_param)
            return True, ""
        except Exception as e:
            return False, e
    
    def execute(self, sql, is_commit=False):
        if None == self.db:
            return False, ()
        try:
            cursor = self.db.cursor()
            cursor.execute(sql);
            if is_commit:
                self.db.commit()
            data = cursor.fetchall()
            return True, data
        except Exception as e:
            print (e)
            return False, (e,)
    
    def insert(self, table_name, map_data, is_replace = False):
        column_names = []
        column_values = []
        for key, value in map_data.items():
            column_names.append(str(key))
            column_values.append("'" + str(value) + "'")
        
        if is_replace:
            sql = "REPLACE INTO " + table_name + " (" + ",".join(column_names) + ") VALUES(" + ",".join(column_values) + ")";
        else:
            sql = "INSERT INTO " + table_name + " (" + ",".join(column_names) + ") VALUES(" + ",".join(column_values) + ")";
        print(sql)
        return self.execute(sql, True)

    def close(self):
        if None != self.db:
            self.db.close()

if __name__ == "__main__":
    db_opt = DBMysql("localhost", "python_data", "root", "hardcore", "UTF8")
    db_opt.connect()
    print(db_opt.execute("select * from user"))


    test_map={"level":"sdfsdf", "id":123123, "follows":3344, "nick":"343432"}
    print(test_map)
    db_opt.insert("moko_info", test_map);
    
    
    db_opt.close()
