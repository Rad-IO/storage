from passlib.hash import sha256_crypt

from storage.drivers.sql_base import PostgresBaseDriver
from storage.drivers.queries import UserDb as Queries
from storage.drivers import responses
import storage.drivers.constants as const


class UsersDBDriver(PostgresBaseDriver):

    def _get_user_by_username(self, email):
        return self.select(Queries.Select.USER_BY_EMAIL, email)

    def _check_pass(self, raw, encrypted):
        return sha256_crypt.verify(raw, encrypted)

    def _get_list_from_requests(self, requests):
        return [
            {
                'patient': r[0],
                'comment': r[1],
            } for r in requests
        ]

    def _encrypt_pass(self, password):
        return sha256_crypt.hash(password)

    def _construct_user_inner_id(self, email, name):
        return abs(hash('{} - {}'.format(email, name))) % (10 ** 8)

    def _check_role(self, inner_id, expected_role):
        r = self.get_role(inner_id)
        if isinstance(r, responses.FailResponse):
            return r

        if r.role != expected_role:
            return responses.FailResponse(
                const.ErrorMessages.Users.INVALID_ROLE.format(r.role)
            )

        return True

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
        role = self.select(Queries.Select.ROLE_ID, role)

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

        # TODO: FINISH THIS

    def upload_photo(self, inner_id, req_id, photo):
        # TODO: FINISH THIS
        pass