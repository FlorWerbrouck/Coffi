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
        sql = "SELECT * FROM Coffi.tblHistoriek WHERE DeviceID=3 AND DateTime > now() LIMIT 1;"
        return Database.get_one_row(sql)

    @staticmethod
    def write_historiek(value, deviceID):
        sql = "INSERT INTO tblHistoriek(DateTime, Value, DeviceID) VALUES (now(), %s, %s)"
        params = [value, deviceID]
        return Database.execute_sql(sql, params)