from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_historiek(DeviceID):
        sql = "SELECT MetingID, Value FROM Coffi.tblHistoriek WHERE DeviceID=%s ORDER BY MetingID DESC limit 1;"
        params = [DeviceID]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_coffeeplanned():
        sql = "SELECT * FROM Coffi.tblHistoriek WHERE DeviceID=3 AND DateTime > now() ORDER BY DateTime LIMIT 1;"
        return Database.get_one_row(sql)
    
    @staticmethod
    def read_totalwater():
        sql = "SELECT sum(Value) FROM Coffi.tblHistoriek WHERE DeviceID = 5;"
        return Database.get_one_row(sql)
    
    @staticmethod
    def read_totalwateravg():
        sql = "SELECT round(sum(Value)/count(Value),2) as 'avg' FROM Coffi.tblHistoriek WHERE DeviceID = 5;"
        return Database.get_one_row(sql)
    
    @staticmethod
    def read_totaltempavg():
        sql = "SELECT round(sum(Value)/count(Value),2) as 'avg' FROM Coffi.tblHistoriek WHERE DeviceID = 4;"
        return Database.get_one_row(sql)

    @staticmethod
    def read_totalwaterall():
        sql = "SELECT * FROM Coffi.tblHistoriek WHERE DeviceID = 5 ORDER BY DateTime;"
        return Database.get_rows(sql)
    
    @staticmethod
    def read_totaltempall():
        sql = "SELECT * FROM Coffi.tblHistoriek WHERE DeviceID = 4 ORDER BY DateTime;"
        return Database.get_rows(sql)

    @staticmethod
    def read_futurecoffees():
        sql = "SELECT * FROM Coffi.tblHistoriek WHERE DeviceID=3 AND DateTime>now() ORDER BY DateTime;"
        return Database.get_rows(sql)

    @staticmethod
    def write_historiek(value, deviceID):
        sql = "INSERT INTO tblHistoriek(DateTime, Value, DeviceID) VALUES (now(), %s, %s)"
        params = [value, deviceID]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def delete_historiek(MetingID):
        sql = "DELETE FROM tblHistoriek WHERE MetingID = %s"
        params = [MetingID]
        return Database.execute_sql(sql, params)

    @staticmethod
    def plan_coffee(date):
        sql = "Insert into tblHistoriek (DateTime, Value, DeviceID) values(%s,1,3)"
        params = [date]
        return Database.execute_sql(sql, params)