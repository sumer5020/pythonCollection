from mysql.connector import connect, Error #NO 1: import mysql connector
from deep_translator import GoogleTranslator #NO 2: import GoogleTranslator API

#darabase connection
msg_en = None; query = None; stp= True; counter=0;
try:
    with connect(host="localhost",user="root",port="3306",password="", #NO 3: create connection to mysql
    ) as connection:
        with connection.cursor() as cursor: #NO 4: create cursor to get and set data
            while stp:
                #cursor = connection.cursor()
                query="select * from gathering_db.msg_translate where isnull(msg_translate.msg_en) limit 1000;" #NO 5: quiry
                cursor.execute(query) #NO 6: exicute the quiry
                result = cursor.fetchall() #NO 7: get the data
                stp = bool(result)
                if stp == True: #NO 8: chick is empty
                    for row in result:
                        msg_en = row[1];
                        msg_en = msg_en.replace('"', '').replace('\'', '').replace('`', '')
                        try:
                            msg_en = GoogleTranslator(source='auto', target='en').translate(msg_en) #NO 9: translate data
                        except:
                            #fill in translate
                            msg_en = "-"
                        # if success try
                        query = """ UPDATE gathering_db.msg_translate SET msg_en = "%s" WHERE id = %s; """ % (
                            msg_en,
                            row[0],
                            )
                        cursor.execute(query)
                        connection.commit() #NO 9: commit DB changes
                counter+=1
                print(counter)
except Error as e:
    print(e)