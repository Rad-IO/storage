class UserDb:
    class Select:
        USER_BY_EMAIL = ('SELECT users.password, users.inner_id, users.role '
                         'FROM users '
                         'WHERE users.email=%s')
        USER_ROLE = ('SELECT roles.role FROM users '
                     '  INNER JOIN roles on users.rid=roles.id '
                     ' WHERE users.inner_id=%s')
        FINISHED_REQUESTS = ('SELECT p.name, r.comment '
                             'FROM requests AS r '
                             '  INNER JOIN patients AS p '
                             '      ON r.pid=p.id '
                             '  INNER JOIN users AS d '
                             '      ON r.did=d.id '
                             'WHERE r.status="DONE" AND d.inner_id=%s')
        ROLE_ID = ('SELECT roles.id '
                   'FROM roles '
                   'WHERE roles.name=%s')

    class Insert:
        NEW_USER = ('INSERT '
                    'INTO users(email,password,role,inner_id,name) '
                    '   VALUES(%s,%s,%d,%s,%s)')
