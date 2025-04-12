import psycopg2
from prettytable import PrettyTable


class DBManager:
    """
    Класс для работы с данными в БД
    """

    def __init__(self, database_name: str, params: dict):
        self.__database_name = database_name
        self.__params = params

    def __connect_to_db(self, query: str) -> None:
        with psycopg2.connect(dbname=self.__database_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                table = PrettyTable()
                table.field_names = [desc[0] for desc in cur.description]

                for row in cur:
                    table.add_row(list(row))
                print(table)

        conn.close()

    def get_vacancies_with_keyword(self, search_query: str) -> None:
        """
        Метод получения списка всех вакансий, в названии которых содержаться переданные в метод слова
        """
        self.__connect_to_db(
            f"""
            SELECT employer_name, vacancy_name, salary, vacancy_url
            FROM vacancies
            JOIN employers using (employer_id)
            WHERE vacancy_name like '%{search_query}%'
            LIMIT 10
            """
        )

    def get_companies_and_vacancies_count(self) -> None:
        """
        Метод получения списка всех компаний и количества вакансий у каждой компании
        """
        self.__connect_to_db(
            """
            SELECT DISTINCT employer_name, open_vacancies
            FROM employers
            JOIN vacancies using (employer_id)
            LIMIT 10
            """
        )

    def get_all_vacancies(self) -> None:
        """
        Метод получения списка всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        self.__connect_to_db(
            """
            SELECT employer_name, vacancy_name, salary, vacancy_url
            FROM vacancies
            JOIN employers using (employer_id)
            LIMIT 10
            """
        )

    def get_avg_salary(self) -> None:
        """
        Метод получения средней зарплаты по вакансиям
        """
        self.__connect_to_db(
            """
            SELECT avg(salary) as avg_salary
            FROM vacancies
            LIMIT 10
            """
        )

    def get_vacancies_with_higher_salary(self) -> None:
        """
        Метод получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        self.__connect_to_db(
            """
            SELECT employer_name, vacancy_name, salary, vacancy_url
            FROM vacancies
            JOIN employers using (employer_id)
            WHERE salary > (SELECT AVG(salary) AS avg_salary FROM vacancies)
            LIMIT 10
            """
        )
