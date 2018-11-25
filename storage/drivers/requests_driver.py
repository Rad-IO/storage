from storage.drivers.queries import RequestDb as Queries
from storage.drivers.sql_base import PostgresBaseDriver
import storage.drivers.responses as responses


class RequestsDbDriver(PostgresBaseDriver):

    def get_requests_with_photo(self):
        results = self.select(Queries.Select.REQUESTS_WITH_PHOTO)

        return responses.SuccessResponse(
            requests=[{'id': r[0], 'photo': r[1]} for r in results]
        )

    def upload_result(self, results, rid, results_driver):
        results_driver.save_results(rid, results)

        self.insert_upload_delete(Queries.Update.UPLOADED_RESULT, rid)

