import os
import sys
import jpype
import jaydebeapi as jp
import pandas.io.sql as pd_sql
from pandas import DataFrame

# sys.argv[1] : select row numbers <int>

def main():
    if len(sys.argv) is 1:
        rownum = 5 # default number of summaries
    elif len(sys.argv) is 2:
        rownum = int(sys.argv[1])
    else:
        print("Usage: oracle_connect.py [rownum <int>]")
        return(0)

    classpath = 'D:/2. program/Python/ojdbc7.jar'
    jpype.startJVM(jpype.getDefaultJVMPath(), '-Djava.class.path=%s' % classpath)

    conn = jp.connect('oracle.jdbc.driver.OracleDriver', 'jdbc:oracle:thin:@localhost:1521:orcl', ['ewpbigdata','ewp~12345'])
    cur = conn.cursor()

    sql = "SELECT * FROM TEST_TABLE"

    pd_sql.execute(sql, conn)

    df = pd_sql.read_sql(sql, conn)
    print(df)

if __name__=="__main__":
    main()