import requests


def get_companies() -> list:
    """Получение названия компаний и их ID"""

    companies_data = {
        "тинькофф": 78638,
        "сбербанк": 3529,
        "альфа банк": 80,
        "втб": 4181,
        "газпромбанк": 3388,
        "россельхозбанк": 58320,
        "уралсиб": 89,
        "рнкб": 1521936,
        "кубанькредит": 200524,
        "почтабанк": 1049556,
    }

    data = []

    for company_name, company_id in companies_data.items():
        company_url = f"https://hh.ru/employer/{company_id}"
        company_info = {"company_id": company_id, "company_name": company_name, "company_url": company_url}
        data.append(company_info)
    return data


def get_vacancies(data: list) -> list:
    """Получение вакансий из выбранных компаний"""
    vacancies = []
    for company in data:
        company_id = company["company_id"]
        params = {"page": 0, "per-page": 100}
        url = f"https://api.hh.ru/vacancies?employer_id={company_id}"
        response = requests.get(url=url, params=params)
        if response.status_code == 200:
            vacancy = response.json()["items"]
            vacancies.extend(vacancy)
        else:
            print(f"Ошибка при запросе компании {company["company_name"]}: {response.status_code}")
    return vacancies


def get_vacancy_list(vacancies: list) -> list[dict]:
    """
    Преобразование информации о компаниях для дальнейшей работы с БД
    """
    vacancy_list = []
    for item in vacancies:
        company_name = item["employer"]["name"]
        company_id = item["employer"]["id"]
        company_url = item["employer"]["url"]
        job_title = item["name"]
        link_to_vacancy = item["employer"]["alternate_url"]
        salary = item["salary"]
        salary_from = 0
        currency = " "
        description = item["snippet"]["responsibility"]
        experience = item["experience"]["name"]
        requirement = item["snippet"]["requirement"]
        if salary:
            salary_from = item["salary"]["from"]
            if not salary_from:
                salary_from = 0
            currency = item["salary"]["currency"]
            if not currency:
                currency = " "
        if not experience:
            experience = "Информация отсутсвует"

        vacancy_list.append(
            {
                "company_id": company_id,
                "company_name": company_name,
                "company_url": company_url,
                "job_title": job_title,
                "link_to_vacancy": link_to_vacancy,
                "salary_from": salary_from,
                "salary_to": salary,
                "currency": currency,
                "experience": experience,
                "description": description,
                "requirement": requirement,
            }
        )
    return vacancy_list
