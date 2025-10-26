from typing import Any

from database import get_db


class MenuDAL:
    """
    Data Access Layer for Menu operations.
    Handles database interactions for user menu and details.
    """

    def __init__(self):
        self.db = get_db()

    def get_user_details(self, username: str) -> tuple[list[tuple[Any, ...]], list[str]]:
        """
        Get user details from database.

        :param username: Username to get details for
        :return: A tuple containing list of user detail tuples from database and a list of column names
        """
        cursor = self.db.cursor()
        cursor.execute(self._get_user_details_query(), (username,))
        result = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description] if cursor.description else []
        cursor.close()
        return result, column_names

    def _get_user_details_query(self) -> str:
        """
        Creates SQL for getting user details using parameterized query.

        :return: SQL query string with parameter placeholder
        """
        return """
            SELECT
                user.name, company.headquarters, government_agency.jurisdiction,
                municipality.population_size, individual.job_title,
                individual.hired_date
            FROM user
            LEFT JOIN company
                ON company.username = user.username
            LEFT JOIN government_agency
                ON government_agency.username = user.username
            LEFT JOIN municipality
                ON municipality.username = user.username
            LEFT JOIN individual
                ON individual.username = user.username
            WHERE user.username = %s
        """
