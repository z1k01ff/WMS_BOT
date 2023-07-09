#����������� ����������
import cx_Oracle
import pandas as pd
import time

#��������� ������ (������ ���� > 3.0)
cx_Oracle.__version__

#����������� ���������� ���������� Oracle
ConnectStr = """(DESCRIPTION=(ADDRESS=(PROTOCOL=...)(Host=...)
                   (Port= ... ))(CONNECT_DATA=(SERVICE_NAME= ... )))"""

#����������� ����� � ������ (��� �������� �������������� ��������� '/')
Login = 'IVANOV/PASSWORD'

#�������, � ������� ��������� ��������� ������ connect, �� ��������� �������������� � �������� Oracle
        def getConn(Login, ConnectStr):
            conn=None
            nn=0
            while conn==None:
                try:
                    conn=cx_Oracle.connect(Login + '@' + ConnectStr)
                except cx_Oracle.DatabaseError as e:
                    ers,=e.args
                    nn=nn+1
                    print (nn,end='\r')
                    if ers.code!=2391:
                        print ('������ Oracle ', ers.code)
                        break
                    time.sleep(5)
            return conn

#�������, � ������� ��������� ������ � ����������� ������
        def dfFromOracle(connection, sql):
            us=0
            outDF=pd.DataFrame()
            success = 'False'
            with connection.cursor() as cursor1:
                cursor1.execute(sql)
                trn=10
                while success == 'False' and trn>0:
                    try:
                        outheader=[desc[0] for desc in cursor1.description]
                        #��� ������ "cursor1.fetchall()" ������������ ������ �������, ������ �� �������
                        #�������� �������� (������������ �������) ����� ������� ����
                        outDF=pd.DataFrame(cursor1.fetchall())
                        success = 'True'
                        print('��������� ������� �� ����')
                        us = 1
                    except:
                        trn=trn-1
                        print('Error')
                        time.sleep(60)
            return outheader, outDF, us

#������������ � �������
getConn(Login, ConnectStr)

#����, � ������� ���� ������� �� ����� ���������� ���
f = open('inn_in_.txt','r',encoding='UTF-8')

#����������� ��� �����, � ������� ���������� ���������
new_file = 'new_file.csv'

r='' #��� ������ ����� � "with", ������� ��������� � SQL-������
h = 0 #��� �������� ������� ����������
l = 0 #������� ����� ��� ������� SQL-�������
ll = 0 #������� ����� ��� �������� �� �������
cnt = 10000 #���������� ����� ��� ������� SQL-�������

#���� ��� �������� � ������� SQL-��������
    for row in f:
        l += 1
        if r == '': #��������� "where" - ������ ��� ��� ����������
            r = r + 'inn = \'' + row.replace('\n','') + '\''
        else:
            r = r + 'or inn = \'' + row.replace('\n','') + '\''
        if l % cnt == 0: #�������� �� 10 000 �����
            ll += l
            sql = ( 'select * from tabl where' + r ) #�������������� SQL-������

            #���������� SQL-������ � ������������ ���������� ��������
            with getConn(Login,ConnectStr) as con1:
                if h==0:
                    _header,result,us = dfFromOracle(con1, sql)
                    header = ';'.join(_header)+'\n'
                    myfile=open(new_file, 'w',encoding='UTF-8')
                    myfile.writelines(header)
                    myfile.close()
                    h=1
                result.to_csv(new_file, sep=';',encoding='UTF-8',mode='a',header=None,index=False)
            r=''
            print('���������: '+str(l) )
    if l != ll: #���� ��������� ������ ����� 10 000 �����
        sql = ( 'select * from tabl where' + r ) #�������������� SQL-������
        with getConn(Login,ConnectStr) as con1:
            _header,result,us = dfFromOracle(con1, sql)
            if h==0:
                header = ';'.join(_header)+'\n'
                myfile=open(new_file, 'w',encoding='UTF-8')
                myfile.writelines(header)
                myfile.close()
                h=1
            result.to_csv(new_file, sep=';',encoding='UTF-8',mode='a',header=None,index=False)
        print('���������: '+str(l) )
    print('�������� ���������')
    f.close()