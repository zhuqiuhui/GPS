import sqlite3


def get_conn(DBLoation):
    return sqlite3.connect(DBLoation)


def get_cursor(conn):
    if conn is not None:
        return conn.cursor()
    else:
        res = 'conn is None, please check the connection!'
        return res


def fetchAll(conn, sql):
    """查询所有记录并返回"""
    if sql is not None and sql != '':
        cu = get_cursor(conn)
        cu.execute(sql)
        r = cu.fetchall()
        if len(r) > 0:
            # for e in range(len(r)):
            #     print(r[e])
            print('get ' + str(len(r)) + ' records!')
        else:
            print('get non record!')
        cu.close()
        # closeDB(conn, cu)
        return r
    else:
        print('sql is None!')
        # closeDB(conn, cu)
        return None


def update(conn, sql, parameters):
    """更新数据记录"""
    if sql is not None and sql != '':
        if parameters is not None:
            cu = get_cursor(conn)
            cu.executemany(sql, parameters)
            conn.commit()
            cu.close()
            print('update ' + str(len(parameters)) + ' successfully!')
        else:
            print('parameters is None, please check parameters!')
    else:
        print('sql is None!')
    # closeDB(conn, cu)


def insert(conn, sql, parameters):
    """插入数据与更新数据一样"""
    if sql is not None and sql != '':
        if parameters is not None:
            cu = get_cursor(conn)
            cu.executemany(sql, parameters)
            conn.commit()
            cu.close()
            print('insert ' + str(len(parameters)) + ' successfully!')
        else:
            print('parameters is None, please check parameters!')
    else:
        print('sql is None!')
    # closeDB(conn, cu)


def closeDB(conn):
    if conn is not None:
        conn.close()


# def closeDB(conn, cu):
#     try:
#         if cu is not None:
#             cu.close()
#     finally:
#         if conn is not None:
#             conn.close()


def main():
    path = '../DB/GPS.db'

    # print('find all records:')
    # fetchall_sql = 'select * from GPS_label_1'
    # conn1 = get_conn(path)
    # r = fetchAll(conn1, fetchall_sql)
    # # print(type(r[0][3]))
    # # print(r[0][3])
    # print(r)

    """遇到数据库锁定，可能在客户端进行操作，只需要关闭客户端重新启动就行了"""
    # print('update the records:')
    # update_sql = 'update GPS_label_1 set is_deleted=? where id=?'
    # parameters = [(2, 2), [3, 3]]
    # conn2 = get_conn(path)
    # update(conn2, update_sql, parameters)

    """插入数据测试"""
    print('insert the records:')
    insert_sql = 'insert into GPS_label_1("start_time", "end_time", "mode") values (?, ?, ?)'
    parameters = [('2007/10/13 15:49:15', '2007/10/13 15:55:53', 'taxi'),
                  ('2007/10/13 15:56:58', '2007/10/13 15:59:15', 'walk'),
                  ('2007/10/15 9:18:22', '2007/10/15 9:25:59', 'bike')]
    conn3 = get_conn(path)
    insert(conn3, insert_sql, parameters)


if __name__ == '__main__':
    main()
