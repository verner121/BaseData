import os
from typing import Any, Dict, List

import psycopg2


def create_database(database_name: str, params: dict) -> None:
    """
    Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях
    """
    bd_name = os.getenv("DB_NAME")

    conn = psycopg2.connect(dbname=bd_name, **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()

    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE employers (
                    employer_id TEXT,
                    employer_name VARCHAR(100) NOT NULL,
                    site_url TEXT,
                    open_vacancies INT NOT NULL,
                    CONSTRAINT pk_employers PRIMARY KEY (employer_id)
                )"""
            )

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE vacancies (
                    id SERIAL,
                    vacancy_id TEXT,
                    vacancy_name VARCHAR(100) NOT NULL,
                    employer_id TEXT,
                    salary INT,
                    vacancy_url TEXT,
                    CONSTRAINT pk_vacancies PRIMARY KEY (id),
                    CONSTRAINT fk_employer_id FOREIGN KEY (employer_id) REFERENCES employers(employer_id)
                )"""
            )

    conn.close()


def add_employers_to_database(employers: List[Dict[str, Any]], database_name: str, params: dict) -> None:
    """
    Функция выборки данных по работодателям и записи их в таблицу базы данных
    """
    data_for_add = []
    for employer in employers:
        data_for_add.append(
            {
                "employer_id": employer.get("id"),
                "employer_name": employer.get("name"),
                "site_url": employer.get("site_url"),
                "open_vacancies": employer.get("open_vacancies"),
            }
        )

    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            for data in data_for_add:
                cur.execute(
                    """
                    INSERT INTO employers (employer_id, employer_name, site_url, open_vacancies)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        data.get("employer_id"),
                        data.get("employer_name"),
                        data.get("site_url"),
                        data.get("open_vacancies"),
                    ),
                )

    conn.close()


def add_vacancies_to_database(vacancies: List[Dict[str, Any]], database_name: str, params: dict) -> None:
    """
    Функция выборки данных по вакансиям и записи их в таблицу базы данных
    """
    data_for_add = []
    for vacancy in vacancies:
        salary_data = vacancy.get("salary", {})
        if salary_data is None or salary_data == {}:
            salary = 0
        else:
            salary = salary_data.get("from", {})
        if salary is None or salary_data == {}:
            salary = 0

        data_for_add.append(
            {
                "vacancy_id": vacancy.get("id"),
                "vacancy_name": vacancy.get("name"),
                "employer_id": vacancy.get("employer", {}).get("id"),
                "salary": salary,
                "vacancy_url": vacancy.get("alternate_url"),
            }
        )

    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            for data in data_for_add:
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_id, vacancy_name, employer_id, salary, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        data.get("vacancy_id"),
                        data.get("vacancy_name"),
                        data.get("employer_id"),
                        data.get("salary"),
                        data.get("vacancy_url"),
                    ),
                )

    conn.close()
