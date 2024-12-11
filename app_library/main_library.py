from library_manager import *

lib = Library("Ленинская")
print(lib)

lib.add_book("Остров", "Верн", "Приключения")
lib.add_book("Мир", "Толстой", "Драма")
lib.add_book("Мцыри", "Лермонтов", "Поэзия")
print(lib)
lib.catalog(verbose=True)
lib.delete_book("Мцыри1")
lib.delete_book("Мцыри")
print(generate_report(lib))
lib.add_book("Мцыри", "Лермонтов", "Поэзия")
lib.add_book("Таинственный Остров", "Верн", "Приключения")

print(generate_report(lib))
print(lib.search_book(query="Остр"))
