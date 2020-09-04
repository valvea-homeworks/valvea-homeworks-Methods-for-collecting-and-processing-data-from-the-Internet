from manage_db import Manage_db


class Vacancy:
    def __init__(self):
        self.manage=Manage_db()
        self.db=self.manage.get_db('vacancy')

    def get_names_of_sites(self):
        return self.db.list_collection_names()

    def get_site(self,name):
        return self.db.get_collection(name)

    def update_site_vacancy(self,name_of_site,vacancy):
        self.manage.update_collection(self.get_site(name_of_site),vacancy)

    def seach_vacancy_on_salary(self ,name_of_site,salary):
        return [x for x in self.get_site(name_of_site).
            find({'$or': [{'Зарплата.минимальная': {'$gt': salary}},
                                                  {'Зарплата.максимальная': {'$gt': salary}}]})]



