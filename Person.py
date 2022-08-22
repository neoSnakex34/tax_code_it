from TaxCode import TaxCode


class Person:
    
    name: str
    surname: str
    gender: int #better enum; using binary genders due to italian law
    birthday: str
    birthmont: str
    birthyear: str
    city: str

    tax: TaxCode    
    tax_code_str: str

    def __init__(self) -> None:
        pass

    def interactive_person_info_set(self) -> None:
        self.tax = TaxCode()
        self.name = input("Inserisci nome: ") 
        self.surname =  input("Inserisci cognome: ") 
        self.gender = input("Inserisci genere (0=M / 1=F): ") 
        self.city = input("Inserisci città di nascita: ") 
        self.birthday = input("Inserisci giorno di nascita (DD): ") 
        self.birthmont = input("Inserisci mese di nascita (MM): ") 
        self.birthyear = input("Inserisci anno di nascita (YYYY): ") 

    def get_tax_code(self):
        self.tax_code_str = self.tax.tax_code_retriever(self.name, self.surname, self.gender, self.birthyear, self.birthmont, self.birthday, self.city)
        print(self.tax_code_str)

