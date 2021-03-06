from atp.logger import L
from atp.errcode import ER_INSERT_FAILED, ER_SUCC


def getRecordNumSQL(tableName, **filters):
        QUERY_SQL = "SELECT COUNT(*) FROM {}".format(tableName)
        valueList = []
        filterSize = len(filters)
        if filterSize == 1:
            for key in filters:
                QUERY_SQL += " " + " ".join(("WHERE", key, "=", "%s"))
                valueList.append(filters[key])
        elif filterSize > 1:
            flag = True
            for key in filters:
                if flag:
                    flag = False
                    QUERY_SQL += " " + " ".join(("WHERE", key, "=", "%s"))
                    valueList.append(filters[key])
                else:
                    QUERY_SQL += " " + " ".join(("AND", key, "=", "%s"))
                    valueList.append(filters[key])

        return QUERY_SQL, valueList

def getRecordNum(cursor, QUERY_SQL):
    try:
        cursor.execute(QUERY_SQL[0], QUERY_SQL[1])
        recNum = cursor.fetchone()[0]
    except Exception as e:
        L.error("query record number failed")
        raise e
    finally:
        cursor.close()

    return recNum


class FlightInfo:
    def __init__(self, queryDate, queryTime, flightDate, depCode, arrCode, rec):
        #flightNo, depTime, depAirport, arrTime, arrAirport, elapsedTime, ptyRate, delayTime, ticketPrice)
        self.queryDate = queryDate
        self.queryTime = queryTime
        self.flightDate = flightDate

        self.depCode = depCode
        self.arrCode = arrCode
        self.flightNo, \
        self.depTime, \
        self.depAirport, \
        self.arrTime, \
        self.arrAirport, \
        self.elapsedTime, \
        self.ptyRate, \
        self.delayTime, \
        self.ticketPrice = map(lambda x: '' if not x else x.encode('utf8'), rec)
                
    def asRec(self):
        return (self.queryDate, self.queryTime, self.flightDate, self.depCode, self.arrCode,
                self.flightNo, \
                self.depTime, \
                self.depAirport, \
                self.arrTime, \
                self.arrAirport, \
                self.elapsedTime, \
                self.ptyRate, \
                self.delayTime, \
                self.ticketPrice)
        
class FlightInfoHandler:
    def __init__(self, conn):
        self.conn = conn
    
    INSERT_SQL = "INSERT INTO FLIGHT_INFO (query_date, query_time, flight_date, dep_code, arr_code, flight_number, \
                  dep_time, dep_airport, arr_time, arr_airport, elapsed_time, punctuality_rate, \
                  delay_time, ticket_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                  
    def insertOneRec(self, flightInfo):
        cursor = self.conn.cursor()
        try:
            cursor.execute(self.INSERT_SQL, flightInfo.asRec())
            self.conn.commit()
        except:
            L.error("insert failed")
            self.conn.rollback()
            return ER_INSERT_FAILED
            
        cursor.close()
        
        return ER_SUCC

    def getRecordNum(self, **filters):
        return getRecordNum(self.conn.cursor(), getRecordNumSQL("FLIGHT_INFO", **filters))


            
class FlightLowestPriceInfo:
    def __init__(self, queryDate, queryTime, depCode, arrCode, rec):
        #flightNo, depTime, depAirport, arrTime, arrAirport, elapsedTime, ptyRate, delayTime, ticketPrice)
        self.queryDate = queryDate
        self.queryTime = queryTime
        self.depCode = depCode
        self.arrCode = arrCode
        self.flightDate, \
        self.flightNo, \
        self.depTime, \
        self.arrTime, \
        self.carrier, \
        self.vendorName, \
        self.ticketPrice = map(lambda x: '' if not x else x.encode('utf8'), rec)
        
        self.ticketPrice = str(int(float(self.ticketPrice)))
        
    def asRec(self):
        return (self.queryDate,
                self.queryTime,
                self.depCode,
                self.arrCode,
                self.flightDate, \
                self.flightNo, \
                self.depTime, \
                self.arrTime, \
                self.carrier, \
                self.vendorName, \
                self.ticketPrice)
        
    
class FlightLowestPriceInfoHandler:
    def __init__(self, conn):
        self.conn = conn
    
    INSERT_SQL = "INSERT INTO FLIGHT_LOWEST_PRICE_INFO (query_date, query_time, dep_code, arr_code, flight_date, flight_number, \
                  dep_time, arr_time, carrier, vendor_name, ticket_price) \
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                  
    def insertOneRec(self, info):
        cursor = self.conn.cursor()
        try:
            cursor.execute(self.INSERT_SQL, info.asRec())
            self.conn.commit()
        except:
            L.error("insert failed")
            self.conn.rollback()
            
        cursor.close()

    def getRecordNum(self, **filters):
        return getRecordNum(self.conn.cursor(), getRecordNumSQL("FLIGHT_LOWEST_PRICE_INFO", **filters))