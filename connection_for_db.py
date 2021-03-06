import tabulate
import psycopg2

from tabulate import tabulate
from psycopg2 import Error
from config import username, pwd, hostname, db

#tabulate.WIDE_CHARS_MODE = True
tabulate.PRESERVE_WHITESPACE = True

try:
    # Подключение к существующей базе данных
    connection = psycopg2.connect(user=username,
                                  # пароль, который указали при установке PostgreSQL
                                  password=pwd,
                                  host=hostname,
                                  port="5432",
                                  database=db)

    async def bd_last_visit(id, text):
        cursor2 = connection.cursor()
        u_id = id
        text1 = text
        cursor2.execute("UPDATE registration SET last_visit = now(), name_menu = '%s' WHERE user_id = %s" %(text1, u_id))
        connection.commit()


    async def bd_check_id(id):
        cursor2 = connection.cursor()
        t_id = id
        cursor2.execute("SELECT user_id FROM ambassador WHERE user_id = %s" % (t_id))
        table = cursor2.fetchone()
        return table



    async def bd_registration(user_id, name, link_name, link, num, bdate, city_1):
        cursor2 = connection.cursor()
        id = user_id
        nm = name
        lk = link
        ln = link_name
        num_ = num
        date = bdate
        city_0 = city_1
        cursor2.execute("SELECT user_id FROM ambassador WHERE user_id = '%s'" % (id))
        check = cursor2.fetchone()
        if (check is None):
            cursor2.execute("INSERT INTO ambassador (user_id, name, link_name, link_user, number, city, bdate) VALUES (%s, %s, %s, %s, %s, %s, %s)", (id, nm, ln, lk, num_, city_0, date))
            connection.commit()
            cursor2.execute("INSERT INTO registration (user_id, date_reg) VALUES (%s, now())" % (id))
            connection.commit()
            return 1
        else:
            cursor2.execute("SELECT city FROM ambassador WHERE user_id = '%s'" % (id))
            city = cursor2.fetchone()
            check_city = str(city).replace("(", '').replace(")", '').replace(",", '').replace("'", '')
            cursor2.execute("SELECT university FROM ambassador WHERE user_id = '%s'" % (id))
            uni = cursor2.fetchone()
            check_uni = str(uni).replace("(", '').replace(")", '').replace(",", '').replace("'", '')
            cursor2.execute("SELECT info FROM ambassador WHERE user_id = '%s'" % (id))
            info = cursor2.fetchone()
            check_info = str(info).replace("(", '').replace(")", '').replace(",", '').replace("'", '')
            if check_city == 'None' or check_uni == '0' or check_info == 'None':
                return 1
            else:
                return 0


    async def bd_registration_uni(id_1, msg):
        cursor2 = connection.cursor()
        id = id_1
        uni = msg
        cursor2.execute("UPDATE ambassador SET university = %s WHERE user_id = %s", (uni, id))
        connection.commit()
        return 1

    async def bd_registration_continue(userid, msg):
        cursor2 = connection.cursor()
        id = userid
        city = msg
        cursor2.execute("UPDATE ambassador SET city = %s WHERE user_id = %s", (city, id))
        connection.commit()
        return 1

    async def bd_registration_continue_2(userid, msg):
        cursor2 = connection.cursor()
        id = userid
        uni = msg
        cursor2.execute("UPDATE ambassador SET university = %s WHERE user_id = %s", (uni, id))
        connection.commit()
        return 1

    async def bd_registration_continue_info(userid, msg):
        cursor2 = connection.cursor()
        id = userid
        uni = msg
        cursor2.execute("UPDATE ambassador SET info = %s WHERE user_id = %s", (uni, id))
        connection.commit()
        return 1

    async def bd_city_check(temp_msg):
        cursor2 = connection.cursor()
        text_db = temp_msg
        cursor2.execute("SELECT city FROM ambassador WHERE city = '%s'" %(text_db))
        table = cursor2.fetchone()
        return table

    async def bd_city(temp_msg):
        cursor2 = connection.cursor()
        text_db = temp_msg
        cursor2.execute("SELECT link_name, university, info FROM ambassador WHERE city = '%s' order by name" % (text_db))
        table2 = cursor2.fetchall()
        temp_table = (tabulate(table2, tablefmt="plain"))
        return temp_table

    async def bd_number_check(temp_msg):
        cursor2 = connection.cursor()
        text_db = temp_msg
        cursor2.execute("SELECT number FROM ambassador WHERE number = '%s'" %(text_db))
        table = cursor2.fetchone()
        return table

    async def bd_number(temp_msg):
        cursor2 = connection.cursor()
        text_db = temp_msg
        cursor2.execute("SELECT link_name, info FROM ambassador WHERE number = '%s' order by name" % (text_db))
        table2 = cursor2.fetchall()
        temp_table = (tabulate(table2, tablefmt="plain"))
        return temp_table

    async def bd_all_event():
        cursor2 = connection.cursor()
        cursor2.execute("SELECT event_name, guid.link_guid FROM event LEFT JOIN event_type as et ON et.type_code = event.event_type LEFT JOIN guid ON guid.guid_id = event.guid_id order by event_name")
        table = cursor2.fetchall()
        table_1 = str(table).replace("[", '').replace("]", '').replace("'", '').replace("(", '').replace(")",'').replace(",", '\n')
        return table_1

    async def bd_all_guid():
        cursor2 = connection.cursor()
        cursor2.execute("SELECT name_guid, link_guid FROM guid order by guid_id")
        table = cursor2.fetchall()
        table_1 = str(table).replace("[", '').replace("]", '').replace("'", '').replace("(", '').replace(")", '').replace(",", '\n')
        return table_1

    async def bd_online():
        cursor2 = connection.cursor()
        cursor2.execute("SELECT ev.event_name, guid.link_guid FROM event AS ev LEFT JOIN guid ON guid.guid_id = ev.guid_id WHERE event_category like 'online%' order by ev.event_name")
        table = cursor2.fetchall()
        temp_table = str(table).replace("[", '').replace("]", '').replace("'", '').replace("(", '').replace(")",'').replace(",", '\n')
        return temp_table

    async def bd_offline():
        cursor2 = connection.cursor()
        cursor2.execute("SELECT ev.event_name, guid.link_guid FROM event AS ev LEFT JOIN guid ON guid.guid_id = ev.guid_id WHERE event_category like '%offline' order by ev.event_name")
        table = cursor2.fetchall()
        temp_table = str(table).replace("[", '').replace("]", '').replace("'", '').replace("(", '').replace(")",'').replace(",", '\n')
        return temp_table

    async def bd_online_offline():
        cursor2 = connection.cursor()
        cursor2.execute("SELECT ev.event_name, guid.link_guid FROM event AS ev LEFT JOIN guid ON guid.guid_id = ev.guid_id WHERE event_category = 'online/offline' order by ev.event_name")
        table = cursor2.fetchall()
        temp_table = str(table).replace("[", '').replace("]", '').replace("'", '').replace("(", '').replace(")",'').replace(",", '\n')
        return temp_table

    async def bd_type():
        cursor2 = connection.cursor()
        cursor2.execute("SELECT type_info FROM event_type order by type_code")
        table = cursor2.fetchall()
        temp_table = (tabulate(table, tablefmt="simple"))
        return temp_table

    async def bd_user_type(temp_msg):
        cursor2 = connection.cursor()
        text_db = temp_msg
        cursor2.execute("SELECT event_type FROM event WHERE event_type = '%s'" % (text_db))
        table = cursor2.fetchone()
        if (table is not None):
            cursor2.execute("SELECT ev.event_name, ev.event_category, ev.event_text, guid.link_guid FROM event AS ev LEFT JOIN guid ON guid.guid_id = ev.guid_id WHERE event_type = '%s' order by ev.event_name" %(text_db))
            table = cursor2.fetchall()
            temp_table = str(table).replace("[", '').replace("]", '').replace("'", '').replace("(", '').replace(")",'').replace(",", '\n')
            return temp_table
        else:
            return 999999999999

    async def bd_month(bddate):
        month = bddate
        cursor2 = connection.cursor()
        cursor2.execute("SELECT * FROM (SELECT substring(bdate from 4 for 6) AS Month FROM ambassador)t WHERE Month = '%s'" %(month))
        table1 = cursor2.fetchall()
        print(table1)
        return table1

    async def bd_date(bdate):
        date = bdate
        cursor2 = connection.cursor()
        cursor2.execute("SELECT * FROM (SELECT substring(bdate from 1 for 2) AS Date FROM ambassador)t WHERE Date >= '%s'" % (date))
        table2 = cursor2.fetchone()
        if table2 is not None:
            cursor2.execute("SELECT * FROM (SELECT substring(bdate from 1 for 2) AS Date FROM ambassador)t WHERE Date >= '%s'" % (date))
            table3 = cursor2.fetchone()
            return table3
        else:
            return 99

    async def bd_name(bdate_1):
        date = str(bdate_1)
        cursor2 = connection.cursor()
        cursor2.execute("SELECT name FROM (SELECT name, substring(bdate from 1 for 2) AS Date FROM ambassador)t WHERE Date = '%s'" %(date))
        table = cursor2.fetchall()
        return table


    async def bd_token(id, msg):
        id_u = id
        token = msg
        cursor2 = connection.cursor()
        cursor2.execute("INSERT INTO group_t (user_id, token_group, token_time) VALUES ('%s', '%s', now())" % (id_u, token))
        connection.commit()


    def bd_token_take():
        cursor2 = connection.cursor()
        cursor2.execute("SELECT token_group FROM group_t order by max(token_time) over(partition by token_time) desc limit 1")
        table = cursor2.fetchall()
        return table

    # Курсор для выполнения операций с базой данных
    #cursor = connection.cursor()
    # Распечатать сведения о PostgreSQL
    #print("Информация о сервере PostgreSQL")
    #print(connection.get_dsn_parameters(), "\n")
    # Выполнение SQL-запроса
    #cursor.execute("SELECT version();")
    # Получить результат
    #record = cursor.fetchone()
    #print("Вы подключены к - ", record, "\n")

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)

