from lexrankr import LexRank
import numpy as np

import warnings
warnings.filterwarnings("ignore")

import os
import sys
import jpype
import jaydebeapi as jp
import pandas.io.sql as pd_sql
import pandas as pd
import subprocess

def ora_conn():
    classpath = 'D:/2. program/Python/ojdbc7.jar'
    jpype.startJVM(jpype.getDefaultJVMPath(), '-Djava.class.path=%s' % classpath)
    conn = jp.connect('oracle.jdbc.driver.OracleDriver', 'jdbc:oracle:thin:@localhost:1521:orcl', ['ewpbigdata','ewp~12345'])
    cur = conn.cursor()
    return(conn)

def ora_read_sql(conn, query):
    sql = query
    pd_sql.execute(sql, conn)
    df = pd_sql.read_sql(sql, conn, index_col = None)
    return(df)

def read_txt(dir):
    f = open(dir, 'r')
    text = f.read()
    f.close()
    return(text)

def main():
    conn = ora_conn()
    cur = conn.cursor()

    #STATUS 1(분석 대기중)
    query = "UPDATE TB_EWP_ANLS_SELF_INFO SET REQST_STTUS_CD='1' WHERE (ANALS_SE='2') AND (REQST_STTUS_CD='0')"
    cur.execute(query)

    df = ora_read_sql(conn, query="SELECT * FROM TB_EWP_ANLS_SELF_INFO WHERE (REQST_STTUS_CD='1')")
    ANAL_MODE = df['ANALS_SE']
    REQ_SN = df['ANAL_REQ_SN']

    for i, SN in enumerate(REQ_SN):
        try:
            #STATUS 2(분석 진행중)
#            query = "UPDATE TB_EWP_ANLS_SELF_INFO SET REQST_STTUS_CD='2' WHERE (ANAL_REQ_SN=%.0f)" % SN
#            cur.execute(query)
 
            text = df[df['ANAL_REQ_SN']==SN]['ANALS_TXT'].astype(str)
            text.astype(str).map(lambda x: type(x))
            text = text.str.replace("'", "")

            file_path = 'C:/Users/goan1/source/repos/textAnalysis/text_%s.txt' % SN

            np.savetxt(file_path, text, fmt='%s')

            if ANAL_MODE[i] == '1':
                command = 'python C:/Users/goan1/source/repos/textAnalysis/TextFrequency.py %s' % file_path
                data = os.popen(command).read()

            elif ANAL_MODE[i] == '2':
                command = 'python C:/Users/goan1/source/repos/textAnalysis/TextSummarize.py %s' % file_path
                data = os.popen(command).read()


            print(data)

            #Insert JSON
#            query = "UPDATE TB_EWP_ANLS_SELF_INFO SET ANALS_RESULT='%s' WHERE (ANAL_REQ_SN=%.0f)" % (data, SN)
#            cur.execute(query)

            #STATUS 3(분석 완료)
#            query = "UPDATE TB_EWP_ANLS_SELF_INFO SET REQST_STTUS_CD='3' WHERE (ANAL_REQ_SN=%.0f)" % SN
#            cur.execute(query)


        except ValueError:
            #STATUS 4(분석 실패)
            query = "UPDATE TB_EWP_ANLS_SELF_INFO SET REQST_STTUS_CD='4' WHERE (ANAL_REQ_SN=%.0f)" % SN
            cur.execute(query)

        os.remove(file_path)

    cur.close()
    conn.close()
    jpype.shutdownJVM()

if __name__=='__main__':
    main()

