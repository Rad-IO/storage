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
        DB_ID = ('SELECT users.id '
                 'FROM users '
                 'WHERE users.inner_id=%s')

    class Insert:
        NEW_USER = ('INSERT '
                    'INTO users(email,password,role,inner_id,name) '
                    '   VALUES(%s,%s,%d,%s,%s)')


class Roles:
    class Select:
        ROLE_ID = ('SELECT roles.id '
                   'FROM roles '
                   'WHERE roles.name=%s')


class RequestDb:
    class Insert:
        NEW_REQUEST = ('INSERT '
                       'INTO requests(did,sts,pid,comment) '
                       '    VALUES(%d,%s,%d,%s)')

    class Select:
        LATEST_REQUEST = ('SELECT requests.id '
                          'FROM requests '
                          'ORDER BY requests.id DESC LIMIT 1')
        REQUESTS_WITH_PHOTO = ('SELECT requests.id, requests.photo '
                               'FROM requests '
                               "WHERE requests.status='UPLOADED'")
        FINISHED_REQUESTS_FOR_DOCTOR = (
            'SELECT requests.id, patients.name, patients.cnp '
            'FROM requests '
            'INNER JOIN patients'
            '   ON requests.pid=patients.id '
            'INNER JOIN users '
            '   ON requests.id=users.id'
            "WHERE requests.status='DONE' AND users.inner_id=%s"
        )

    class Update:
        UPLOADED_PHOTO = ('UPDATE requests '
                          'SET rid=%d,'
                          '    photo=%s,'
                          '    status=%s,'
                          'WHERE requests.id=%d')
        UPLOADED_RESULT = ('UPDATE requests '
                           "SET status='DONE' "
                           'WHERE requests.id=%d')
