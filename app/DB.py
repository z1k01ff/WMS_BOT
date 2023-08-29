import oracledb
import pandas as pd
import dataframe_image as dfi

# CLIENT_DIR = "/Users/admin/Documents/instantclient_19_8/"
CLIENT_DIR = "E:\instantclient_21_11"
oracledb.init_oracle_client(lib_dir=CLIENT_DIR, config_dir=None, error_url=None, driver_name=None)
connection = oracledb.connect(
    user="qguaradm",
    password="quantum",
    dsn="WMSUB1.berta.corp/lc2")
print("Successfully connected to Oracle Database")


def privyazka_DB(product_nr):
    if len(product_nr) != 9:
        print(len(product_nr))
        print("not artikul")
        return "not artikul"
    sql = f"select PRODUCT_NR as Artikul, NAME as Nazva, SP_NR as Misce from QWHV_SPREAD_SP_ASSIGNMENT where product_nr = '{product_nr}' and wh_nr = '1'"
    df = pd.read_sql(sql, connection)
    dfi.export(df, 'cache/PNG/privyazka.png')
    print(product_nr)
    print(df)
    return df


# privyazka("000024774")
def soderzimoe_DB(product_nr):
    if len(product_nr) != 9:
        print(len(product_nr))
        print("not artikul")
        return "not artikul"
    sql = f"select LOADUNIT_NR, PRODUCT_NR, PRODUCT_NAME, SP_NR  from QWHV_SPREAD_WHS_CONTENTS_UB t where product_nr = '{product_nr}'"
    df = pd.read_sql(sql, connection)
    dfi.export(df, 'cache/PNG/soderzimoe.png')
    print(product_nr)
    print(df)
    return df


# soderzimoe_DB("000029666")

def vidpravka_DB():
    sql = "select pzone_nr, COUNT(pzone_nr) as KILKIST " \
          "FROM TRV_SPREAD_TRANS_ORDERS_FAST " \
          "where transport_type_id = 'SH' " \
          "and pzone_nr not in ('Global Підбір', 'Імпорт Косметика', 'Підбір VICHI', 'Підбір ПАККОР', 'Підбір Соломія Сервіс', " \
          "'Підбір Зовнішні чаї', 'Шторк Імпорт', 'Yarych підбір', 'Підбір Белла мезонін', 'Підбір Нестле Тема', " \
          "'Підбір Загальний Нестле М', 'Підбір Кондзона Нестле МК')" \
          "GROUP by pzone_nr"
    df = pd.read_sql(sql, connection)
    dfi.export(df, 'cache/PNG/vidpravka.png')
    # print(df)
    piec_df = df[df['PZONE_NR'].isin(
        ['Нестле шт', 'Спец пуріна шт', 'Підбір ЖуйкаФерреро шт', 'Берта шт', 'Марс шт', 'Болеро шт',
         'Підбір Юнілевер'])]
    pack_df = df[df['PZONE_NR'].isin(['Підбір Болеро 2 ящ', 'Підбір дистрибуція ящ', 'Підбір Болеро ящ', 'Спец пуріна',
                                      'Підбір Нестле ящ', 'Підбір Жуйка ящ', 'Підбір Ферерро ящ Львів',
                                      'Підбір БС Крупи',
                                      'Марс Кондитер ящ', 'Імпорт', 'Підбір Берта_1 ящ', 'Підбір Нестле Prof',
                                      'Підбір ЛСЛ Корма'])]

    sum_pack = {'PZONE_NR': "ЗАГАЛЬНА КІЛЬКІСТЬ ЯЩ", 'KILKIST': pack_df['KILKIST'].sum()}
    sum_piec = {'PZONE_NR': "ЗАГАЛЬНА КІЛЬКІСТЬ ШТ", 'KILKIST': piec_df['KILKIST'].sum()}

    piec_df = piec_df._append(sum_piec, ignore_index=True)
    pack_df = pack_df._append(sum_pack, ignore_index=True)

    pack_df = pack_df.sort_values(by='KILKIST', ascending=True)
    piec_df = piec_df.sort_values(by='KILKIST', ascending=True)

    dfi.export(piec_df, 'cache/PNG/vidpravka_piec.png')
    dfi.export(pack_df, 'cache/PNG/vidpravka_pack.png')

    print(piec_df)

    print(pack_df)

    return df


def transport_DB(tip_pocheniya):
    sql = f"select pzone_nr, COUNT(pzone_nr) as KILKIST from TRV_SPREAD_TRANS_ORDERS_FAST " \
          f"where transport_type_id = '{tip_pocheniya}' and wh_from_nr = 1 " \
          f"GROUP by pzone_nr"
    df = pd.read_sql(sql, connection)
    sum_df = {'PZONE_NR': "КІЛЬКІСТЬ ПОПОВНЕНЬ", 'KILKIST': df['KILKIST'].sum()}
    df = df._append(sum_df, ignore_index=True)
    df = df.sort_values(by='KILKIST', ascending=True)
    dfi.export(df, 'cache/PNG/transport.png')
    print(df)


def transport_perep_DB(tip_pocheniya):
    sql = f"select product_nr, COUNT(product_nr) as KILKIST from TRV_SPREAD_TRANS_ORDERS_FAST " \
          f"where transport_type_id = '{tip_pocheniya}' " \
          f"GROUP by product_nr"
    df = pd.read_sql(sql, connection)
    sum_df = {'PRODUCT_NR': "КІЛЬКІСТЬ ПЕРЕПАКОВОК", 'KILKIST': df['KILKIST'].sum()}
    df = df._append(sum_df, ignore_index=True)
    df = df.sort_values(by='KILKIST', ascending=True)
    dfi.export(df, 'cache/PNG/transport_perep.png')
    print(df)


def transport_vidpravka_marshrut():
    sql = f"select sroute_name as MARSHRUT, COUNT(sroute_name) as KILKIST from TRV_SPREAD_TRANS_ORDERS_FAST " \
          f"where transport_type_id = 'SH' and f_firm_nr = 'Компания Берта' and wh_from_nr = 1 " \
          f"GROUP by sroute_name " \
          f"ORDER BY KILKIST ASC"
    df = pd.read_sql(sql, connection)
    dfi.export(df, 'cache/PNG/transport_vidpravka.png')
    print(df)


def vidpravka_red():
    sql = f"select  firm_name, sroute_name as MARSHRUT, COUNT(sroute_name) as KILKIST " \
          f"from SHV_SPREAD_SHIPMENTS t " \
          f"where status_name in ('Заплановано', 'Реалізація') and cf like '<GC><ROW><CLR BC%' and wh_nr = 1 " \
          f"GROUP BY sroute_name, firm_name ORDER by MARSHRUT ASC"
    df = pd.read_sql(sql, connection)
    sum_df = {'FIRM_NAME': 'INFO', 'MARSHRUT': 'НЕ ПОПОВНЕНО НАКЛАДНИХ', 'KILKIST': df['KILKIST'].sum()}
    df = df._append(sum_df, ignore_index=True)
    # dfi.export(df, 'cache/PNG/vidpravka_red.png')
    print(df)


def vidpravka_nabrano(date_started):
    sql = f"select sroute_name as MARSHRUT, COUNT(sroute_name) as KILKIST " \
          f"from SHV_SPREAD_SHIPMENTS t " \
          f"where status_name = 'Завершена комплектація' and wh_nr = 1 and DATE_CREATED >= To_date ('{date_started} 18:30:00', 'DD/MM/YYYY HH24:MI:SS') " \
          f"and firm_name = 'Компания Берта' " \
          f"GROUP BY sroute_name, firm_name ORDER by MARSHRUT ASC"
    df = pd.read_sql(sql, connection)
    sum_df = {'MARSHRUT': "НАБРАНО НАКЛАДНИХ", 'KILKIST': df['KILKIST'].sum()}
    df = df._append(sum_df, ignore_index=True)
    dfi.export(df, 'cache/PNG/vidpravka_nabrano.png')
    print(df)


def transport_peremish_in():
    sql = f"select sp_to_nr as MISCE, COUNT(sp_to_nr) as KILKIST from TRV_SPREAD_TRANS_ORDERS_FAST " \
          f"where transport_type_id = 'MV' and sp_to_nr like 'IN-%' and sp_from_nr != 'BUFFER'" \
          f"GROUP by sp_to_nr"
    df = pd.read_sql(sql, connection)
    dfi.export(df, 'cache/PNG/transport_perem_IN.png')
    print(df)


def transport_peremish_st():
    sql = f"select sp_to_nr as MISCE, COUNT(sp_to_nr) as KILKIST from TRV_SPREAD_TRANS_ORDERS_FAST " \
          f"where transport_type_id = 'MV' and sp_to_nr like 'STO%' and sp_from_nr != 'BUFFER'" \
          f"GROUP by sp_to_nr"
    df = pd.read_sql(sql, connection)
    dfi.export(df, 'cache/PNG/transport_perem_ST.png')
    print(df)


def transport_vidpravka_bl():
    sql = f"select sroute_name as MARSHRUT, COUNT(sroute_name) as KILKIST from TRV_SPREAD_TRANS_ORDERS_FAST " \
          f"where transport_type_id = 'SH' and f_firm_nr = 'Близенько' " \
          f"GROUP by sroute_name"
    df = pd.read_sql(sql, connection)
    dfi.export(df, 'cache/PNG/transport_vidpravka_bl.png')
    print(df)


# LOADUNIT_ID номер носителя без букв
# PRODUCT_NR номер артикула
# PRODUCT_NAME Назва товару
def soderzimoe_full_DB(input_data, input_type):
    sql = f"select LOADUNIT_NR, PRODUCT_NR, PRODUCT_NAME, BU_QUANTITY as kilkist, QUANTITY_PACK as kilkist_PACK, BU_QUANTITY_MOD as kilkist_sht, SP_NR  " \
          f"from QWHV_SPREAD_WHS_CONTENTS_UB t where {input_type} = '{input_data}' " \
          f"and wh_nr = 1 and SA_NR BETWEEN 'A' and 'B'"
    df = pd.read_sql(sql, connection)

    dfi.export(df, 'cache/PNG/soderzimoe_full.png')
    df.to_excel('exel/soderzimoe_full.xlsx')
    print(df.head())
    return df

def soderzimoe_full_DB_t(input_data, input_type):
    sql = f'select LOADUNIT_NR, PRODUCT_NR, PRODUCT_NAME, PRODUCT_CLASS, SERIAL_NR, ' \
          f'DATE_EXPIRE, DATE_PROD, BU_QUANTITY, QUANTITY_PACK, BU_QUANTITY_MOD, ABBREV, ' \
          f'SA_NR, SP_NR, STATUS_QUALITY_DESC, EAN_NR  ' \
          f'from QWHV_SPREAD_WHS_CONTENTS_UB where {input_type} like \'{input_data}\' ' \
          f'and wh_nr = 1 and SA_NR BETWEEN \'A\' and \'B\''
    df = pd.read_sql(sql, connection)

    # dfi.export(df, 'PNG/soderzimoe_full.png')
    df.to_excel('exel/soderzimoe_full_t.xlsx')
    print(df.head())
    return df


if __name__ == '__main__':
    # vidpravka_DB()
    # transport_DB("RP")
    # transport_perep_DB("CP")
    # transport_peremish_in("MV")
    # transport_peremish_st()
    # vidpravka_nabrano("15.06.2023")
    vidpravka_red()
    # soderzimoe_full_DB("000063815", "PRODUCT_NR")
