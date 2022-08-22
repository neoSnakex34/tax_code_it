import warnings

from Person import Person

# only activate when distributing 
warnings.filterwarnings('ignore', category=UserWarning)


def main() -> None:
    p = Person()
    p.interactive_person_info_set()
    p.get_tax_code()

main()