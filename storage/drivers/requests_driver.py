from .queries import RequestDb as Queries
from .sql_base import PostgresBaseDriver
from .responses import SuccessResponse


class RequestsDbDriver(PostgresBaseDriver):
    def __init__(self, **kwargs):
        super(PostgresBaseDriver, self).__init__(**kwargs)

    def get_requests_with_photo(self):
        results = self.select(Queries.Select.REQUESTS_WITH_PHOTO)

        return SuccessResponse(
            requests=[{'id': r[0], 'photo': r[1]} for r in results]
        )

    def upload_result(self, results, rid, results_driver):
        results_driver.save_results(rid, results)

        self.insert_upload_delete(Queries.Update.UPLOADED_RESULT, rid)

