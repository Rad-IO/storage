import json

from storage.drivers import PhotosStorageDriver
from storage.drivers import ResultsDriver
from storage.drivers import UsersDBDriver
from storage.drivers import responses


class StorageHandler:
    def __init__(self, config):
        with open(config) as stream:
            cnf_data = json.load(stream)

        self._photo_driver = PhotosStorageDriver(cnf_data['photos_path'])
        self._results_driver = ResultsDriver(cnf_data['results_path'])

        self._postgres_credentials = cnf_data['postgres']

    def _get_response(self, func, attrs, *args):
        response = func(*args)
        if isinstance(response, responses.FailResponse):
            return None
        return {x: response.__getattr__(x) for x in attrs}

    def create_request(self, inner_id, patient_id, comment):
        try:
            with UsersDBDriver(**self._postgres_credentials) as driver:
                return self._get_response(driver.create_request, ['rid'],
                                          inner_id, patient_id, comment)
        except:
            return None

    def upload_photo(self, inner_id, rid, data):
        try:
            with UsersDBDriver(**self._postgres_credentials) as driver:
                return self._get_response(driver.upload_photo, [], inner_id,
                                          rid, data, self._photo_driver)
        except:
            return None

    def get_request(self, rid):
        try:
            with UsersDBDriver(**self._postgres_credentials) as driver:
                return self._get_response(driver.get_finished_request,
                                          ['patient_name', 'patient_cnp',
                                           'radiologist'], None,
                                          rid, self._results_driver)
        except:
            return None

    def get_requests_for_doctor(self, inner_id):
        try:
            with UsersDBDriver(**self._postgres_credentials) as driver:
                return self._get_response(driver.get_requests, ['requests'],
                                          inner_id)
        except:
            return None
