import base64

from passlib.hash import sha256_crypt

from .sql_base import PostgresBaseDriver
from .queries import UserDb as Queries
from .queries import Roles as QueriesRoles
from .queries import RequestDb as QueriesRequests
from . import responses
from . import constants as const


class UsersDBDriver(PostgresBaseDriver):
    def __init__(self, **kwargs):
        super(UsersDBDriver, self).__init__(**kwargs)

    def _get_user_by_username(self, email):
        return self.select(Queries.Select.USER_BY_EMAIL, email)

    def _check_pass(self, raw, encrypted):
        return sha256_crypt.verify(raw, encrypted)

    def _get_list_from_requests(self, requests):
        return [
            {
                'name': r[0],
                'cnp': r[1],
            } for r in requests
        ]

    def _encrypt_pass(self, password):
        return sha256_crypt.hash(password)

    def _construct_user_inner_id(self, email, name):
        return base64.b16encode(
            str(abs(hash('{} - {}'.format(email, name)))).encode()
        ).decode()

    def _check_role(self, inner_id, expected_role):
        r = self.get_role(inner_id)
        if isinstance(r, responses.FailResponse):
            return r

        if r.role != expected_role:
            return responses.FailResponse(
                const.ErrorMessages.Users.INVALID_ROLE.format(r.role)
            )

        return True

    def _get_db_id(self, inner_id):
        return self.select(Queries.Select.DB_ID, inner_id)

    def login(self, email, password):
        user = self._get_user_by_username(email)
        if len(user) != 1 or user is None:
            return responses.FailResponse(
                const.ErrorMessages.Users.LOGIN_FAILED
            )
        user = user[0]
        if not self._check_pass(password, user[0]):
            return responses.FailResponse(
                const.ErrorMessages.Users.LOGIN_FAILED
            )

        return responses.SuccessResponse(id=user[1], role=user[2])

    def get_role(self, inner_id):
        data = self.select(Queries.Select.USER_ROLE, inner_id)

        if len(data) != 1 or data is None:
            return responses.FailResponse(
                const.ErrorMessages.Users.CANNOT_FIND_ROLE
            )

        return responses.SuccessResponse(role=data[0][0])

    def get_requests(self, inner_id):
        r = self._check_role(inner_id, 'doctor')
        if isinstance(r, responses.FailResponse):
            return r

        requests = self.select(Queries.Select.FINISHED_REQUESTS, inner_id)

        if len(requests) == 0 or requests is None:
            return responses.FailResponse('No requests found.')

        return responses.SuccessResponse(
            requests=self._get_list_from_requests(requests)
        )

    def add_user(self, name, email, password, role):
        role = self.select(QueriesRoles.Select.ROLE_ID, role)

        if len(role) == 0 or role is None:
            return responses.FailResponse(
                const.ErrorMessages.Users.CANNOT_FIND_ROLE.format(role)
            )

        if len(self._get_user_by_username(email)) != 0:
            return responses.FailResponse(
                const.ErrorMessages.Users.USER_IN_DATABASE.format(email)
            )

        self.insert_upload_delete(
            Queries.Insert.NEW_USER,
            email,
            self._encrypt_pass(password),
            role[0][0],
            self._construct_user_inner_id(email, name),
            name,
        )

        return responses.SuccessResponse()

    def create_request(self, inner_id, patient_id, comment):
        r = self._check_role(inner_id, 'doctor')
        if isinstance(r, responses.FailResponse):
            return r

        db_id = self._get_db_id(inner_id)

        if db_id is None or len(db_id) == 0:
            return responses.FailResponse(
                const.ErrorMessages.Users.INVALID_INNER_ID.format(inner_id)
            )

        self.insert_upload_delete(
            QueriesRequests.Insert.NEW_REQUEST,
            db_id[0][0],
            'WAITING',
            patient_id,
            comment,
        )

        rid = self.select(QueriesRequests.Select.LATEST_REQUEST)[0][0]

        return responses.SuccessResponse(rid=rid)

    def upload_photo(self, inner_id, req_id, photo_data, photo_driver):
        r = self._check_role(inner_id, 'radiolog')
        if isinstance(r, responses.FailResponse):
            return r

        db_id = self._get_db_id(inner_id)

        if db_id is None or len(db_id) == 0:
            return responses.FailResponse(
                const.ErrorMessages.Users.INVALID_INNER_ID.format(inner_id)
            )

        photo_id = photo_driver.save_new_image(photo_data)

        self.insert_upload_delete(
            QueriesRequests.Update.UPLOADED_PHOTO,
            db_id, photo_id, 'UPLOADED', req_id,
        )

    def get_finished_request(self, inner_id, rid, results_driver):
        data = self.select(QueriesRequests.Select.REQUEST_BY_ID, rid)
        if data is None or len(data) != 1:
            return responses.FailResponse(
                const.ErrorMessages.Users.INVALID_INNER_ID.format(inner_id)
            )
        results = results_driver.get_results(rid)

        return responses.SuccessResponse(
            results=results,
            patient_name=data[0][0],
            patient_cnp=data[0][1],
            radiologist=data[0][2],
        )
