from typing import Any, Dict, List

import requests
from requests import Response

from src.exceptions import RequestsAPIError
from user_settings import LIST_OF_EMPLOYERS


class HeadHunterAPI:
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self) -> None:
        self.__headers: dict[str, str] = {"User-Agent": "HH-User-Agent"}
        self.vacancies: List[Dict[str, Any]] = []
        self.employers: List[Dict[str, Any]] = []

    def __connect_api(self, url: str, params: Dict[str, Any]) -> Response:
        """
        Метод для подключения к API
        """
        return requests.get(url, headers=self.__headers, params=params)

    def get_data_vacancies(self) -> List[Dict[str, Any]]:
        """
        Метод получения списка вакансий работодателей указанных в модуле user_settings.py
        """
        url = "https://api.hh.ru/vacancies"
        for item in LIST_OF_EMPLOYERS:
            params: dict[str, Any] = {"page": 0, "per_page": 100, "employer_id": item}

            while True:
                try:
                    response = self.__connect_api(url, params)
                    if response.status_code != 200:
                        raise RequestsAPIError(f"Ошибка при запросе к API: {response.status_code}")
                except RequestsAPIError:
                    print("Ошибка при запросе к API")
                    return self.vacancies
                else:
                    vacancies = response.json().get("items", [])
                    if len(vacancies) == 0:
                        break
                    self.vacancies.extend(vacancies)
                    params["page"] += 1
        return self.vacancies

    def get_data_employers(self) -> List[Dict[str, Any]]:
        """
        Метод получения информации о работодателях указанных в модуле user_settings.py
        """
        for item in LIST_OF_EMPLOYERS:
            url: str = f"https://api.hh.ru/employers/{item}"
            params: dict[str, Any] = {}

            try:
                response = self.__connect_api(url, params)
                if response.status_code != 200:
                    raise RequestsAPIError(f"Ошибка при запросе к API: {response.status_code}")
            except RequestsAPIError:
                print("Ошибка при запросе к API")
                return self.employers
            else:
                self.employers.extend([response.json()])
        return self.employers
