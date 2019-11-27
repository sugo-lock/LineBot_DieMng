# -*- coding: utf-8 -*-
# https://qiita.com/mas9612/items/5423c09efd613518a521
# MySQLdbのインポート
import MySQLdb
import os

def start_connect():
    # データベースへの接続とカーソルの生成
    connection = MySQLdb.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        passwd=os.environ['DB_PASS'],
        db=os.environ['DB_NAME']
    cursor = connection.cursor()
    return cursor, connection

def end_connect(connection):
    # 保存を実行
    connection.commit()
    # 接続を閉じる
    connection.close()

#-----------
# # PROFILE テーブルの作成
def make_profile_tbl(cursor):
    try:
        tbl_name = 'PROFILE'
        sql = 'create table '+ tbl_name +' (USER_ID int, SEX varchar(32), AGE int, HEIGHT float)'
        cursor.execute(sql)
        connection.commit()
        print('---PROFILE テーブルを作成---')
    except:
        print("Already Exist -> PROFILE TABLE")

# PROFILEテーブルにレコードを登録
def reg_record_profile_tbl(cursor, user_id, col, record):
    tbl_name = 'PROFILE'
    # user_idがあるか確認
    sql = 'select exists(select * from ' + tbl_name + ' Where USER_ID=%s)'  # http://compute-cucco.hatenablog.com/entry/2017/05/03/170038
    try:
        cursor.execute(sql, user_id)
    except:
        print("Error: "+sql)
        pass
    
    if cursor.fetchone()[0]==0:
        sql = 'insert into ' +  tbl_name + ' (USER_ID, '+col+') values (%s, %s)'
        cursor.execute(sql, (user_id, record))  # 挿入
    else: # すでにUSER_IDが存在する場合
        print('USER_ID:'+str(user_id)+' is already exist.')
        sql = 'update ' +  tbl_name + ' set ' + col + '=%s where USER_ID=%s'
        cursor.execute(sql, (record, user_id))  # 更新

# PROFILEテーブルのレコードの取得
def get_record_profile_tbl(cursor):
    tbl_name = 'PROFILE'
    sql = 'select * from ' + tbl_name
    cursor.execute(sql)
    for row in cursor.fetchall():
        print('USER_ID:', row[0], ', SEX:', row[1], ', AGE:', row[2], ', HEIGHT:', row[3]) 

#-----------
# HISTRICAL_"USER_ID"テーブルの作成
def make_histrical_tbl(cursor, user_id):
    try:
        tbl_name = 'HISTRICAL_' + user_id
        sql = 'create table '+ tbl_name +' (DATE varchar(64), WEIGHT float, CAL_BARNED float, CAL_INTAKE float )'
        cursor.execute(sql)
        connection.commit()
        print('---HISTRICAL テーブルを作成---')
    except:
        print("Already Exist -> HISTRICAL TABLE")

# HISTRICAL_"USER_ID"テーブルにレコードを登録
def reg_record_histrical_tbl(cursor, user_id, date, col, record):
    tbl_name = 'HISTRICAL_' + user_id
    # dateがあるか確認
    sql = 'select exists(select * from ' + tbl_name + ' Where DATE=%s)'  # http://compute-cucco.hatenablog.com/entry/2017/05/03/170038
    try:
        cursor.execute(sql, (date,))
    except:
        print("Error: "+sql)
        pass
    if cursor.fetchone()[0]==0:
        sql = 'insert into ' +  tbl_name + ' (DATE, '+col+') values (%s, %s)'
        cursor.execute(sql, (date, record))  # 挿入
    else: # すでにDATEが存在する場合
        print('DATE:'+str(date)+' is already exist.')
        sql = 'update ' +  tbl_name + ' set ' + col + '=%s where DATE=%s'
        cursor.execute(sql, (record, date))  # 更新

# HISTRICAL_"USER_ID"テーブルのレコードの取得
def get_record_histrical_tbl(cursor, user_id):
    tbl_name = 'HISTRICAL_' + user_id
    sql = 'select * from ' + tbl_name
    cursor.execute(sql)
    for row in cursor.fetchall():
        print('DATE:', row[0], ', WEIGHT:', row[1], ', CAL_BARNED:', row[2], ', CAL_INTAKE:', row[3]) 

# テーブル一覧の取得
def list_tbl(cursor, db_name):
    sql = 'show tables from ' + db_name
    cursor.execute(sql)
    print('===== テーブル一覧 =====')
    print(cursor.fetchall())

# テーブルの削除
def del_tbl(cursor, tbl_name):
    sql = 'drop table '+ tbl_name
    cursor.execute(sql)
    connection.commit()
    print("Complete: " + sql)

#-----------
if __name__ == "__main__":    

    cursor, connection = start_connect()

    # ここに実行したいコードを入力します
    list_tbl(cursor, 'DB_DietMng')
    
    # PROFILEテーブル作成
    make_profile_tbl(cursor)


    user_id = '0'
    col = 'AGE'
    record = '28'
    reg_record_profile_tbl(cursor, user_id, col, record)
    get_record_profile_tbl(cursor)

    # HISTRICAL_"user_id"テーブル作成
    user_id = '0'

    make_histrical_tbl(cursor, user_id)
    date = '2019/11/26'
    col = 'WEIGHT'
    record = '90.1'
    reg_record_histrical_tbl(cursor, user_id, date, col, record)
    get_record_histrical_tbl(cursor, user_id)

    #del_tbl(cursor, "PROFILE")

    end_connect(connection)

