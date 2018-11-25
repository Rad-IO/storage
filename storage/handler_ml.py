import json

from storage.drivers import PhotosStorageDriver
from storage.drivers import ResultsDriver
from storage.drivers import RequestsDbDriver
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

    def get_unused_requests(self):
        try:
            with RequestsDbDriver(**self._postgres_credentials) as driver:
                return self._get_response(driver.get_requests_with_photo,
                                          ['requests'])
        except:
            return None

    def get_photo(self, id):
        return self._photo_driver.get_image_by_id(id, True)

    def upload_result(self, results, rid):
        try:
            with RequestsDbDriver(**self._postgres_credentials) as driver:
                return self._get_response(driver.upload_result, [],
                                          results, rid, self._results_driver)
        except:
            return None
