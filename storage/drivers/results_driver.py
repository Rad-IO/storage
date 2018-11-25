import json
import os


class ResultsDriver:
    def __init__(self, location):
        self._location = os.path.abspath(location)

    def _get_path_for_result_file(self, rid):
        return os.path.join(self._location, '{}.json'.format(str(rid)))

    def save_results(self, rid, results):
        path = self._get_path_for_result_file(rid)

        with open(path, 'w') as stream:
            json.dump(results, stream)

    def get_results(self, rid):
        path = self._get_path_for_result_file(rid)

        with open(path) as stream:
            return json.load(path)

