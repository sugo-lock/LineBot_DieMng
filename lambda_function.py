# -*- coding: utf-8 -*-
import json
import datetime 
import re
import pandas as pd
import matplotlib.pyplot as plt

import line_if
import db_if
import s3_if


def lambda_handler(event, context):
    # REPLY_LINE
    msg = event['events'][0]['message']['text']
    user_id = event['events'][0]['source']['userId']
    replyToken = event['events'][0]['replyToken']
#    line_if.reply_msg(user_id, msg, replyToken)
    
    # メニュー
    if(msg == "メニュー") | (msg=="めにゅー") | (msg=="@m") | (msg=="m") | (msg=="M"):
        msg = "メニュー\n@w:体重入力\n@g:グラフ表示\n@i摂取カロリー入力\n@o:消費カロリー入力"
        line_if.quick_reply(user_id)
    
    # プロフィール入力
    elif(msg == "profile"):
        line_if.push_msg(user_id, "プロフィールを入力してください。\nex)\n身長：172.2 -> @h172.2\n体重：65.5kg -> @w65.5\n年齢：25歳 -> @a25\n性別：男->@man")
    
    # 消費カロリー入力
    elif(msg == "cal_burned"):
        line_if.push_msg(user_id, "消費カロリーを入力してください\nex)500kcal消費した場合 -> @b500")
    
    # 摂取カロリー入力
    elif(msg == "cal_intake"):
        line_if.push_msg(user_id, "摂取カロリーを入力してください\nex)500kcal摂取した場合 -> @i500")

    # グラフを表示
    elif(msg == "graph"):
        cursor, connection = db_if.start_connect()
        df = db_if.get_record_histrical_tbl(cursor, user_id)
        db_if.end_connect(connection)
#        df = df.fillna(method='ffill') # 欠損値 0埋め
        if len(df) > 10:
            df = df.iloc[len(df)-10:len(df)]
        fig, ax = plt.subplots(figsize=(5,len(df)))
        ax.axis('off')
        ax.axis('tight')
        ax.table(cellText=df.values,
                colLabels=df.columns,
                loc='center',
                bbox=[0,0,1,1])
        plt.savefig('./tmp/table.png')
        FIG_DIR = './tmp'
        BUCKET_NAME = 'health-maneger-sugo-lock'
        DIR = 'DietManager'
        url_list = upload(FIG_DIR, BUCKET_NAME, DIR)
        line_if.push_fig(user_id, fig_url)
        #line_if.push_msg(user_id, "graph is comming soon.")
        
    # 身長入力
    elif("@h" in msg):
        cursor, connection = db_if.start_connect()
        db_if.make_profile_tbl(cursor)
        db_if.reg_record_profile_tbl(cursor, user_id, col='HEIGHT', record=msg.strip('@h'))
        db_if.end_connect(connection)
        line_if.push_msg(user_id, msg + " Added DataBase.")
    
    # 年齢入力
    elif("@a" in msg):
        cursor, connection = db_if.start_connect()
        db_if.make_profile_tbl(cursor)
        db_if.reg_record_profile_tbl(cursor, user_id, col='AGE', record=msg.strip('@a'))
        db_if.end_connect(connection)
        line_if.push_msg(user_id, msg + " Added DataBase.")

    # 性別入力
    elif("@s" in msg):
        cursor, connection = db_if.start_connect()
        db_if.make_profile_tbl(cursor)
        db_if.reg_record_profile_tbl(cursor, user_id, col='SEX', record=msg.strip('@s'))
        db_if.end_connect(connection)
        line_if.push_msg(user_id, msg + " Added DataBase.")

    # 体重入力
    elif("@w" in msg):
        cursor, connection = db_if.start_connect()
        db_if.make_histrical_tbl(cursor, user_id)
        date = datetime.date.today()
        db_if.reg_record_histrical_tbl(cursor, user_id, date, col='WEIGHT', record=msg.strip('@w'))
        db_if.end_connect(connection)
        line_if.push_msg(user_id, msg + " Added DataBase.")

    # 消費カロリー入力
    elif("@b" in msg):
        cursor, connection = db_if.start_connect()
        db_if.make_histrical_tbl(cursor, user_id)
        date = datetime.date.today()
        db_if.reg_record_histrical_tbl(cursor, user_id, date, col='CAL_BARNED', record=msg.strip('@b'))
        db_if.end_connect(connection)
        line_if.push_msg(user_id, msg + " Added DataBase.")

    # 摂取カロリー入力
    elif("@i" in msg):
        cursor, connection = db_if.start_connect()
        db_if.make_histrical_tbl(cursor, user_id)
        date = datetime.date.today()
        db_if.reg_record_histrical_tbl(cursor, user_id, date, col='CAL_INTAKE', record=msg.strip('@i'))
        db_if.end_connect(connection)
        line_if.push_msg(user_id, msg + " Added DataBase.")
    
    else:
        print(user_id)
        line_if.push_msg(user_id, "\""+msg+"\""+" は無効です。\n\"メニュー\" と入力するとメニューを開きます。")
        
    return {'statusCode': 200, 'body': '{}'}
