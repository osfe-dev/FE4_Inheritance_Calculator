from Stat_Calculations import *
from Inheritance_GUI import *

def main():
    app = QApplication([])

    window = FE4_Calc()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()