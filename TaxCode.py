import requests
from utils.is_vowel import is_vowelf
from utils.is_even import is_evenf
from bs4 import BeautifulSoup


LETTERS = list(map(chr, range(ord('A'), ord('Z')+1)))


class TaxCode:

    surname_str: str
    name_str: str
    born_year_digits: str
    born_month_digit: str
    birthday: str
    city_code: str
    conrol_letter: str
    tax_code: str

    def __init__(self) -> None:
        self.tax_code = ""
        pass

    def tax_code_retriever(self, name, surname, gender, yyyy, mm, dd, city) -> str:

        self.__surname_string_parser(surname)
        self.__name_string_parser(name)
        self.__born_year_parser(yyyy)
        self.__birthday_parser(dd, gender)
        self.__month_parser(mm)
        self.__city_code_parser(city)

        raw_code = self.surname_str +self.name_str + self.born_year_digits + self.born_month_digit + self.birthday + self.city_code
        self.__control_letter(raw_code)
        
        self.tax_code = raw_code + self.control_letter

        return self.tax_code

    def __city_code_parser(self, city: str) -> None:
            
        final_dict = {}

        for lettera in LETTERS:
            url = "https://www1.agenziaentrate.gov.it/servizi/codici/ricerca/VisualizzaTabella.php?iniz="+lettera+"&ArcName=COM-ICI"
            req = requests.get(url)
            
            if req.reason != 'OK':
                continue
            
            temp_dict = {row.find_all('td')[1].text.strip():row.find_all('td')[0].text for row in
                BeautifulSoup(req.content, "html.parser")
                .find('table', class_='table table-striped table-hover table-bordered table-header')
                .tbody
                .find_all('tr')}

            final_dict.update(temp_dict)

        self.city_code = final_dict[city.upper()]



    def __month_parser(self, month: int) -> None:
        url = "https://www.alus.it/pubs/CodiceFiscale/index.php?lang=it"
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html5lib")

        table = soup.find("table")

        month_dict = {row.find_all('td')[0].text:row.find_all('td')[2].text for row in table.tbody.find_all('tr')[1:]}
        
        self.born_month_digit = month_dict[str(int(month))]
       


    def __name_string_parser(self, name: str) -> None:

        name = "".join(name.split())
        name_string = ""
        
        consonants = [letter for letter in name if not is_vowelf(letter)]
        vowels = [letter for letter in name if is_vowelf(letter)]

        if len(consonants) < 4:
            name_string = "".join(c.upper() for c in consonants)

            while True:
                for vowel in vowels:
                    if len(name_string) == 3:
                        break
                    name_string += vowel.upper()
                
                if len(name_string)<3:
                    name_string += "X"
                break

        else:
            name_string = (consonants[0] + consonants[2] + consonants[3]).upper()


        self.name_str = name_string
        


    def __surname_string_parser(self, name: str) -> None:

        name = "".join(name.split())
        surname_string = ""
        
        consonants = [letter for letter in name if not is_vowelf(letter)]
        vowels = [letter for letter in name if is_vowelf(letter)]

        if len(consonants) < 3:
            surname_string = "".join(c.upper() for c in consonants)

            while True:
                for vowel in vowels:
                    if len(surname_string) == 3:
                        break
                    surname_string += vowel.upper()
                
                if len(surname_string)<3:
                    surname_string += "X"
                break

        else:
            surname_string = (consonants[0] + consonants[1] + consonants[2]).upper()


        self.surname_str = surname_string 
        


    def __control_letter(self, raw_code: str) -> None:

        url = "https://www.alus.it/pubs/CodiceFiscale/index.php?lang=it"
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html5lib")

        uneven_position_nums = [row.find_all('td')[2].text for row in soup.find("table", summary="Lettera di controllo").tbody.find_all('tr')[2:]] #2: toglie le scritte itdentificative e stuff like that, tenendomi solo i digits
        even_position_nums = list(range(0,26)) # piu easy 

        uneven_position_table = {LETTERS[i]:int(uneven_position_nums[i]) for i in range(len(LETTERS))}
        even_position_table = {LETTERS[i]:int(even_position_nums[i]) for i in range(len(LETTERS))}
        integration_u = {str(i):int(uneven_position_nums[i]) for i in range(10)}
        integration_e = {str(i):int(even_position_nums[i]) for i in range(10)}

        uneven_position_table.update(integration_u)
        even_position_table.update(integration_e)

        
        #sum all and divide by 26
        raw_list_to_sum = []
        for index, char in enumerate(raw_code):
            idx = index+1 #real index caring of human offset
            ch = char.upper()
            if is_evenf(idx):
                raw_list_to_sum.append(even_position_table[ch])
            else:
                raw_list_to_sum.append(uneven_position_table[ch])
        
        control_num = sum(raw_list_to_sum)%26
        control_dictionary = {i:LETTERS[i] for i in range(len(LETTERS))}

        self.control_letter = control_dictionary[control_num]
        
    

    def __born_year_parser(self, year: str) -> None:
        self.born_year_digits = year[2:]

    def __birthday_parser(self, day, gender) -> None:
        if int(gender) == 0:
            self.birthday = day
        elif int(gender) == 1:
            self.birthday = str(int(day)+40)
