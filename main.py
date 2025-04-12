from config import config
from src.utils import create_database, add_employers_to_database, add_vacancies_to_database
from src.hh_api import HeadHunterAPI
from src.dbmanager import DBManager


def main():
    """
    Главная функция запуска программы поиска вакансий
    """
    # Запрос пользовательского ввода
    database_name = input("Введите имя базы данных для создания: ")
    search_query = input("Введите поисковую фразу для поиска вакансий по имени: ")
    # Запрос данных с API HH.ru
    params = config()
    api_hh = HeadHunterAPI()
    data_emp = api_hh.get_data_employers()
    data_vac = api_hh.get_data_vacancies()
    # Создание базы данных и таблиц
    create_database(database_name, params)
    # Ввод данных в даблицы БД
    add_employers_to_database(data_emp, database_name, params)
    add_vacancies_to_database(data_vac, database_name, params)
    # Вывод данных поисковых запросов
    output = DBManager(database_name, params)
    print("\nСписок компаний\n")
    output.get_companies_and_vacancies_count()
    print("\nСписок всех вакансий\n")
    output.get_all_vacancies()
    print("\nСредняя зарплата по всем вакансиям:\n")
    output.get_avg_salary()
    print("\nВакансии с зарплатой выше средней:\n")
    output.get_vacancies_with_higher_salary()
    print("\nРезультат поиска вакансий по имени:\n")
    output.get_vacancies_with_keyword(search_query)


if __name__ == "__main__":
    main()
