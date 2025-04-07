import psycopg2

from config import config
from src.create_db import create_data_base, save_data_to_db
from src.dbmanager import DBManager
from src.hh_api import get_companies, get_vacancies, get_vacancy_list

params = config()
data = get_vacancies(get_companies())
vacancies = get_vacancy_list(data)

create_data_base("homework", params)
conn = psycopg2.connect(dbname="homework", **params)
save_data_to_db(vacancies, "homework", params)


def interfaсe():
    """
    Функция для взаимодейтсвия с пользователем
    """
    db_manager = DBManager("homework", params)
    print(
        "Выберите запрос: \n"
        "1 - Список всех компаний и количество вакансий у каждой компании\n"
        "2 - Cписок всех вакансий с указанием названия компании,"
        " названия вакансии и зарплаты и ссылки на вакансию\n"
        "3 - Средняя зарплата по вакансиям\n"
        "4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
        "5 - Список всех вакансий, в названии которых содержатся запрашиваемое слово\n"
    )
    user_answer = input("Введите номер запроса\n")
    if user_answer == "1":
        companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
        print(f"Список всех компаний и количество вакансий у каждой компании: {companies_and_vacancies_count}\n")
    elif user_answer == "2":
        all_vacancies = db_manager.get_all_vacancies()
        print(
            f"Cписок всех вакансий с указанием названия компании,"
            f" названия вакансии и зарплаты и ссылки на вакансию: {all_vacancies}\n"
        )
    elif user_answer == "3":
        avg_salary = db_manager.get_avg_salary()
        print(f"Средняя зарплата по вакансиям: {avg_salary}\n")
    elif user_answer == "4":
        vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
        print(
            f"Список всех вакансий,"
            f" у которых зарплата выше средней по всем вакансиям: {vacancies_with_higher_salary}\n"
        )
    elif user_answer == "5":
        user_input = input("Введите слово: ")
        vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_input)
        print(f"Список всех вакансий, в названии которых содержатся запрашиваемое слово: {vacancies_with_keyword}")
    else:
        print("Введен неверный запрос")


if __name__ == '__main__':
    interfaсe()
