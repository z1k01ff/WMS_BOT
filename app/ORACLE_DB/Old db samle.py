#Импортируем библиотеки
import cx_Oracle
import pandas as pd
import time

#Проверяем версию (должна быть > 3.0)
cx_Oracle.__version__

#Прописываем дескриптор соединения Oracle
ConnectStr = """(DESCRIPTION=(ADDRESS=(PROTOCOL=...)(Host=...)
                   (Port= ... ))(CONNECT_DATA=(SERVICE_NAME= ... )))"""

#Прописываем логин и пароль (При доменной аутентификации оставляем '/')
Login = 'IVANOV/PASSWORD'

#Функция, в которой создается экземпляр класса connect, он обеспечит взаимодействие с сервером Oracle
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
                        print ('Ошибка Oracle ', ers.code)
                        break
                    time.sleep(5)
            return conn

#Функция, в которой создается курсор и выполняется запрос
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
                        #При вызове "cursor1.fetchall()" возвращается список записей, каждая из которых
                        #является кортежем (неизменяемым списком) полей разного типа
                        outDF=pd.DataFrame(cursor1.fetchall())
                        success = 'True'
                        print('Результат получен из базы')
                        us = 1
                    except:
                        trn=trn-1
                        print('Error')
                        time.sleep(60)
            return outheader, outDF, us

#Подключаемся к серверу
getConn(Login, ConnectStr)

#Файл, в котором одна колонка со всеми значениями ИНН
f = open('inn_in_.txt','r',encoding='UTF-8')

#Присваиваем имя файла, в который выгрузится результат
new_file = 'new_file.csv'

r='' #Для собора строк в "with", которые подставим в SQL-запрос
h = 0 #Для проверки наличия заголовков
l = 0 #Счетчик строк для запуска SQL-запроса
ll = 0 #Счетчик строк для проверки на остаток
cnt = 10000 #Количество строк для запуска SQL-запроса

#Цикл для создания и запуска SQL-запросов
    for row in f:
        l += 1
        if r == '': #Формируем "where" - список ИНН для фильтрации
            r = r + 'inn = \'' + row.replace('\n','') + '\''
        else:
            r = r + 'or inn = \'' + row.replace('\n','') + '\''
        if l % cnt == 0: #Проверка на 10 000 строк
            ll += l
            sql = ( 'select * from tabl where' + r ) #Сформированный SQL-запрос

            #Отправляем SQL-запрос и обрабатываем полученную выгрузку
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
            print('Выгружено: '+str(l) )
    if l != ll: #Если последний список менее 10 000 строк
        sql = ( 'select * from tabl where' + r ) #Сформированный SQL-запрос
        with getConn(Login,ConnectStr) as con1:
            _header,result,us = dfFromOracle(con1, sql)
            if h==0:
                header = ';'.join(_header)+'\n'
                myfile=open(new_file, 'w',encoding='UTF-8')
                myfile.writelines(header)
                myfile.close()
                h=1
            result.to_csv(new_file, sep=';',encoding='UTF-8',mode='a',header=None,index=False)
        print('Выгружено: '+str(l) )
    print('Выгрузка завершена')
    f.close()