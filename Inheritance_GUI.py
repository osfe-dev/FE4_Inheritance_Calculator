from GUI_source import *
from Music_Player import *

class StatForm():
    def __init__(self, Name, Type):
        self.Name = Name
        self.Type = Type
        self.Lvl = QLineEdit()
        self.HP = QLineEdit()
        self.Str = QLineEdit()
        self.Mag = QLineEdit()
        self.Skl = QLineEdit()
        self.Spd = QLineEdit()
        self.Lck = QLineEdit()
        self.Def = QLineEdit()
        self.Mdf = QLineEdit()

class Results_Window(QWidget):
    def __init__(self, father, son, daughter):
        super().__init__()
        self.setWindowTitle('Results')
        self.setFixedSize(int(0.6*WIDTH), int(0.6*HEIGHT))
        if(daughter == None):
            self.setFixedSize(int(0.3*WIDTH), int(0.6*HEIGHT))
        layout = QHBoxLayout()
        son_results = create_child_display(self, son, father)
        layout.addLayout(son_results, 10)
        if(daughter != None):
            layout.addWidget(vertical_separator(LINE_WIDTH, getColor(SEP_COL)), 1)
            daughter_results = create_child_display(self, daughter, father)
            layout.addLayout(daughter_results, 10)
        self.setLayout(layout)

class Stats_Window(QWidget):
    def __init__(self, father, son, daughter):
        super().__init__()
        self.setWindowTitle('Stats')
        self.setFixedSize(int(0.5*WIDTH), int(0.6*HEIGHT))
        if(daughter == None):
            self.setFixedSize(int(0.25*WIDTH), int(0.6*HEIGHT))
        layout = QHBoxLayout()
        son_results = create_child_stat_display(self, son, father)
        layout.addLayout(son_results, 10)
        if(daughter != None):
            layout.addWidget(vertical_separator(LINE_WIDTH, getColor(SEP_COL)), 1)
            daughter_results = create_child_stat_display(self, daughter, father)
            layout.addLayout(daughter_results, 10)
        self.setLayout(layout)

class Growths_Window(QWidget):
    def __init__(self, father, son, daughter):
        super().__init__()
        self.setWindowTitle('Stats')
        self.setFixedSize(int(0.5*WIDTH), int(0.6*HEIGHT))
        if(daughter == None):
            self.setFixedSize(int(0.25*WIDTH), int(0.6*HEIGHT))
        layout = QHBoxLayout()
        son_results = create_child_growths_display(self, son, father)
        layout.addLayout(son_results, 10)
        if(daughter != None):
            layout.addWidget(vertical_separator(LINE_WIDTH, getColor(SEP_COL)), 1)
            daughter_results = create_child_growths_display(self, daughter, father)
            layout.addLayout(daughter_results, 10)
        self.setLayout(layout)

class Welcome_Dialog(QDialog):
    def __init__(self, welcome_msg):
        super().__init__()
        layout = QGridLayout()

        # Create welcome message
        self.label = QLabel()
        self.label.setText(welcome_msg)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label, 0, 0, 1, 4)

        # Create confirmation button
        startBtn = QPushButton("Get Started")
        startBtn.clicked.connect(self.close)
        layout.addWidget(startBtn, 1, 1, 1, 2)

        self.setLayout(layout)
        self.setWindowTitle("Welcome")

class InputDialog(QDialog):
    def __init__(self, prompt, btn_lbl):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(prompt))
        self.Lvl = QLineEdit()
        form = QFormLayout()
        form.addRow("", self.Lvl)
        layout.addLayout(form)
        confirmBtn = QPushButton(btn_lbl)
        confirmBtn.clicked.connect(self.checkLvl)
        layout.addWidget(confirmBtn)
        self.setLayout(layout)
        self.exec()
    
    def checkLvl(self):
        try:
            level = int(self.Lvl.text())
        except:
            display_error_msg(LVL_ERROR)
            return
        if((level < 0) or (level > 30)):
            display_error_msg(LVL_ERROR)
        else:
            self.close()

class FE4_Calc(QMainWindow):
    def __init__(self):
        super().__init__()
        self.results = None
        self.initUI()
        self.welcome_dlg = Welcome_Dialog(WELCOME)
        self.initTimer()

    def initUI(self):
        # Initialize window and basic layout
        self.setWindowTitle('FE4 Inheritance Calculator')
        self.setFixedSize(WIDTH, HEIGHT)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)

        logo = QLabel(self)
        logo.setPixmap(QPixmap('Images/FE4_Logo.png'))
        logo.setAlignment(CENTER)
        self.generalLayout.addWidget(logo, 10)

        self.motherImg = create_image(self, DFLT_MOM_IMG, IMG_WIDTH, IMG_HEIGHT)
        self.fatherImg = create_image(self, DFLT_DAD_IMG, IMG_WIDTH, IMG_HEIGHT)

        # Stat forms
        self.forms = [StatForm("Mother", "Parent"), StatForm("Father", "Parent")]
        self.create_forms()

        # Horizontal Separator
        self.generalLayout.addWidget(horizontal_separator(LINE_WIDTH, getColor(SEP_COL)), 1)

        # Buttons for each mode
        soloBtns = QHBoxLayout()
        statBtn = QPushButton("just stats")
        statBtn.setStyleSheet("background-color:{}".format(LTBLUE))
        statBtn.clicked.connect(self.calculate_children_stats)
        soloBtns.addWidget(statBtn)
        growthsBtn = QPushButton("just growths")
        growthsBtn.setStyleSheet("background-color:{}".format(LTBLUE))
        growthsBtn.clicked.connect(self.calculate_children_growths)
        soloBtns.addWidget(growthsBtn)
        self.generalLayout.addLayout(soloBtns, 10)

        bothBtn = QPushButton("stats and growths")
        bothBtn.setStyleSheet("background-color:{}".format(LTBLUE))
        bothBtn.clicked.connect(self.calculate_children_stats_growths)
        self.generalLayout.addWidget(bothBtn)
        
        # Music Player for BGM
        self.music_player = MusicPlayer(BGM)

        self.center()
        self.show()
        self.music_player.play_BGM(BGM_VOL, BGM_LOOPS)

    def initTimer(self):
        # Creates single-shot delay for welcome message
        QTimer.singleShot(DELAY, self.welcome_dlg.exec)

    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

    def create_stat_form(self, title):
        statForm = QVBoxLayout()
        # Add Label for parent ("Mother" or "Father")
        label = QLabel(self)
        label.setText(title)
        label.setFont(QFont('Helvetica', TITLE_SIZE))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create Corresponding Dropdown
        if(title == "Mother"):
            statForm.addWidget(self.motherImg)
            statForm.addWidget(label)
            self.motherDropdown = self.create_mother_dropdown()
            statForm.addWidget(self.motherDropdown)
            self.avg_stat_btns[MOTHER].setStyleSheet("background-color:{}".format(LTBLUE))
            self.avg_stat_btns[MOTHER].clicked.connect(self.fill_avg_stats_mother)
            statForm.addWidget(self.avg_stat_btns[MOTHER])
            form = MOTHER
        else:
            statForm.addWidget(self.fatherImg)
            statForm.addWidget(label)
            self.fatherDropdown = self.create_father_dropdown()
            statForm.addWidget(self.fatherDropdown)
            self.avg_stat_btns[FATHER].setStyleSheet("background-color:{}".format(LTBLUE))
            self.avg_stat_btns[FATHER].clicked.connect(self.fill_avg_stats_father)
            statForm.addWidget(self.avg_stat_btns[FATHER])
            form = FATHER

        # Create form form parent stats
        formLayout = QFormLayout()
        formLayout.addRow("Lvl:", self.forms[form].Lvl)
        formLayout.addRow("HP: ", self.forms[form].HP)
        formLayout.addRow("Str:", self.forms[form].Str)
        formLayout.addRow("Mag:", self.forms[form].Mag)
        formLayout.addRow("Skl:", self.forms[form].Skl)
        formLayout.addRow("Spd:", self.forms[form].Spd)
        formLayout.addRow("Lck:", self.forms[form].Lck)
        formLayout.addRow("Def:", self.forms[form].Def)
        formLayout.addRow("Mdf:", self.forms[form].Mdf)
        statForm.addLayout(formLayout)
        return statForm

    def create_mother_dropdown(self):
        motherDropdown = QComboBox()
        motherDropdown.addItem("Adeen")
        motherDropdown.addItem("Ayra")
        motherDropdown.addItem("Briggid")
        motherDropdown.addItem("Deirdre")
        motherDropdown.addItem("Erinys")
        motherDropdown.addItem("Ethlin")
        motherDropdown.addItem("Lachesis")
        motherDropdown.addItem("Sylvia")
        motherDropdown.addItem("Tiltyu")
        motherDropdown.setCurrentIndex(3)
        motherDropdown.currentTextChanged.connect(self.update_mother_info)
        return motherDropdown

    def create_father_dropdown(self):
        fatherDropdown = QComboBox()
        fatherDropdown.addItem("Alec")
        fatherDropdown.addItem("Arden")
        fatherDropdown.addItem("Azel")
        fatherDropdown.addItem("Beowolf")
        fatherDropdown.addItem("Claude")
        fatherDropdown.addItem("Dew")
        fatherDropdown.addItem("Finn")
        fatherDropdown.addItem("Holyn")
        fatherDropdown.addItem("Jamke")
        fatherDropdown.addItem("Lewyn")
        fatherDropdown.addItem("Lex")
        fatherDropdown.addItem("Midir")
        fatherDropdown.addItem("Noish")
        fatherDropdown.addItem("Quan")
        fatherDropdown.addItem("Sigurd")
        fatherDropdown.setCurrentIndex(14)
        fatherDropdown.currentTextChanged.connect(self.update_father_info)
        return fatherDropdown       

    def create_forms(self):
        formsLayout = QHBoxLayout()

        # Create average stat buttons
        self.avg_stat_btns = [QPushButton("Use Average Stats"), QPushButton("Use Average Stats")]

        # Create stat forms
        self.motherForm = self.create_stat_form("Mother")
        self.fatherForm = self.create_stat_form("Father")
        formsLayout.addLayout(self.motherForm)
        formsLayout.addWidget(vertical_separator(LINE_WIDTH, getColor(SEP_COL)))
        formsLayout.addLayout(self.fatherForm)
        self.generalLayout.addLayout(formsLayout, 10)

    def fill_form(self, parent, Lvl, stats):
        # Determine which form to fill out
        if(parent == "Mother"):
            form = MOTHER
        elif(parent == "Father"):
            form = FATHER
        else:
            return      # Error
        
        # Fill out form
        self.forms[form].Lvl.setText(str(Lvl))
        self.forms[form].HP.setText(str(stats.HP))
        self.forms[form].Str.setText(str(stats.Str))
        self.forms[form].Mag.setText(str(stats.Mag))
        self.forms[form].Skl.setText(str(stats.Skl))
        self.forms[form].Spd.setText(str(stats.Spd))
        self.forms[form].Lck.setText(str(stats.Lck))
        self.forms[form].Def.setText(str(stats.Def))
        self.forms[form].Mdf.setText(str(stats.Mdf))

    def generate_stats(self, form, parent):
        if(parent == MOTHER):
            name = self.motherDropdown.currentText()
        elif(parent == FATHER):
            name = self.fatherDropdown.currentText()
        else:
            print("ERROR GENERATING STATS. NOT MOTHER OR FATHER")
        stats = Stats(
            name, 
            form.Type,
            float(form.HP.text()),
            float(form.Str.text()),
            float(form.Mag.text()),
            float(form.Skl.text()),
            float(form.Spd.text()),
            float(form.Lck.text()),
            float(form.Def.text()),
            float(form.Mdf.text())
        )
        return (int(form.Lvl.text()), stats)

    # Update image of parent when you select new dropdown option
    def update_father_info(self):
        father = self.fatherDropdown.currentText()
        self.fatherImg.setPixmap(QPixmap('Images/Portraits/{}.png'.format(father)).scaled(IMG_WIDTH, IMG_HEIGHT, Qt.AspectRatioMode.KeepAspectRatio))
        self.reset_stat_form(self.forms[FATHER])

    def update_mother_info(self):
        mother = self.motherDropdown.currentText()
        self.motherImg.setPixmap(QPixmap('Images/Portraits/{}.png'.format(mother)).scaled(IMG_WIDTH, IMG_HEIGHT, Qt.AspectRatioMode.KeepAspectRatio))
        self.reset_stat_form(self.forms[MOTHER])

    # Action that occurs in response to pressing "Calculate stats and growths"
    def display_results(self, mode):
        mother = self.motherDropdown.currentText()
        father = self.fatherDropdown.currentText()

        # Check for invalid pairings
        if( (mother == "Ethlin" and father != "Quan")     or
            (father == "Quan" and mother != "Ethlin")     or
            (mother == "Deirdre" and father != "Sigurd")  or
            (father == "Sigurd" and mother != "Deirdre")  ):  
                display_error_msg(PARENT_ERROR)
                return -1

        # Check for valid stat fields if necessary
        if(mode != MODE_GROWTHS):

            # Generate stats from forms
            try:
                mother_info = self.generate_stats(self.forms[MOTHER], MOTHER)
                father_info = self.generate_stats(self.forms[FATHER], FATHER)
            except:
                display_error_msg(STAT_ERROR)
                return

            mother_stats = mother_info[STATS]
            if(mother_info[LEVEL] >= 20):
                mother_promoted = 1
            else:
                mother_promoted = 0

            father_stats = father_info[STATS]
            if(father_info[LEVEL] >= 20):
                father_promoted = 1
            else:
                father_promoted = 0

            if( check_valid_stats(mother_stats, max_stats[unit_classes[mother_stats.Name][mother_promoted]]) == -1   or
                check_valid_stats(father_stats, max_stats[unit_classes[father_stats.Name][father_promoted]]) == -1   ):
                    display_error_msg(STAT_ERROR)
                    return -1

            # Account for the mothers that reverse inheritance role
            if mother_stats.Name in main_mothers:
                son_parent = [mother_promoted, mother_stats]
                daughter_parent = [father_promoted, father_stats]
            else:
                son_parent = [father_promoted, father_stats]
                daughter_parent = [mother_promoted, mother_stats]
        
            # Calculate stats for both children, excluding Sigurd
            son = calc_start_stats(son_parent[STATS], son_parent[PROMO], daughter_parent[STATS], daughter_parent[PROMO], children[mother_stats.Name][SON], father_stats.Name)
            if(father_stats.Name == "Sigurd"): 
                daughter = None
            else: 
                daughter = calc_start_stats(daughter_parent[STATS], daughter_parent[PROMO], son_parent[STATS], son_parent[PROMO], children[mother_stats.Name][DGHTR], father_stats.Name)
            
            if(mode == MODE_BOTH):
                self.results = Results_Window(father_stats.Name, son, daughter)
            elif(mode == MODE_STATS):
                self.results = Stats_Window(father_stats.Name, son, daughter)
        else:   # Growths
            if(father == "Sigurd"):
                daughter = None
            else:
                daughter = children[mother][DGHTR]
            self.results = Growths_Window(father, children[mother][SON], daughter)

        # Display results
        self.results.show()
        return 0
    
    def calculate_children_stats_growths(self):
        self.display_results(MODE_BOTH)

    def calculate_children_stats(self):
        self.display_results(MODE_STATS)
    
    def calculate_children_growths(self):
        self.display_results(MODE_GROWTHS)

    def reset_stat_form(self, form):
        form.Lvl.setText("")
        form.HP.setText("")
        form.Str.setText("")
        form.Mag.setText("")
        form.Skl.setText("")
        form.Spd.setText("")
        form.Lck.setText("")
        form.Def.setText("")
        form.Mdf.setText("")

    # Action that occurs in response to pressing "Use Average Stats"
    def fill_avg_stats(self, parent):
        dlg = InputDialog(LVL_PROMPT, AVG_STAT_BTN)
        try:
            level = int(dlg.Lvl.text())
        except:
            return
        if(parent == MOTHER):
            unit = self.motherDropdown.currentText()
            form = self.forms[MOTHER]
        else:
            unit = self.fatherDropdown.currentText()
            form = self.forms[FATHER]
        
        # Calculate average stats and fill out corresponding form
        avg_stats = calc_avg_stats_par(unit, level)
        form.Lvl.setText(str(level))
        form.HP.setText(str(round(avg_stats.HP, 1)))
        form.Str.setText(str(round(avg_stats.Str, 1)))
        form.Mag.setText(str(round(avg_stats.Mag, 1)))
        form.Skl.setText(str(round(avg_stats.Skl, 1)))
        form.Spd.setText(str(round(avg_stats.Spd, 1)))
        form.Lck.setText(str(round(avg_stats.Lck, 1)))
        form.Def.setText(str(round(avg_stats.Def, 1)))
        form.Mdf.setText(str(round(avg_stats.Mdf, 1)))

    def fill_avg_stats_mother(self):
        self.fill_avg_stats(MOTHER)

    def fill_avg_stats_father(self):
        self.fill_avg_stats(FATHER)

def create_label(text, alignment, font, size):
    label = QLabel()
    label.setText(text)
    label.setFont(QFont(font, size))
    label.setAlignment(alignment)
    return label

def create_stat_display(self, stats, label):
    # Create stat display (list of all starting stats)
    stat_display = QVBoxLayout()
    stat_display.addWidget(create_label(label, CENTER, TITLE_FONT, HEADING_SZ))
    columns = QHBoxLayout()

    # Create label for each stat (first column)
    lbl_display = QVBoxLayout()
    lbl_display.addWidget(create_label("HP: ", LEFT, LBL_FONT, LBL_SIZE))
    lbl_display.addWidget(create_label("Str:", LEFT, LBL_FONT, LBL_SIZE))
    lbl_display.addWidget(create_label("Mag:", LEFT, LBL_FONT, LBL_SIZE))
    lbl_display.addWidget(create_label("Skl:", LEFT, LBL_FONT, LBL_SIZE))
    lbl_display.addWidget(create_label("Spd:", LEFT, LBL_FONT, LBL_SIZE))
    lbl_display.addWidget(create_label("Lck:", LEFT, LBL_FONT, LBL_SIZE))
    lbl_display.addWidget(create_label("Def:", LEFT, LBL_FONT, LBL_SIZE))
    lbl_display.addWidget(create_label("Mdf:", LEFT, LBL_FONT, LBL_SIZE))

    if(label == "Growths"):
        hp_lbl = str(stats.HP) + "%"
        str_lbl = str(stats.Str) + "%"
        mag_lbl = str(stats.Mag) + "%"
        skl_lbl = str(stats.Skl) + "%"
        spd_lbl = str(stats.Spd) + "%"
        lck_lbl = str(stats.Lck) + "%"
        def_lbl = str(stats.Def) + "%"
        mdf_lbl = str(stats.Mdf) + "%"
    else:
        hp_lbl = str(stats.HP)
        str_lbl = str(stats.Str)
        mag_lbl = str(stats.Mag)
        skl_lbl = str(stats.Skl)
        spd_lbl = str(stats.Spd)
        lck_lbl = str(stats.Lck)
        def_lbl = str(stats.Def)
        mdf_lbl = str(stats.Mdf)

    # Create corresponding value for each stat (second column)
    val_display = QVBoxLayout()
    val_display.addWidget(create_label(hp_lbl, RIGHT, LBL_FONT, LBL_SIZE))
    val_display.addWidget(create_label(str_lbl, RIGHT, LBL_FONT, LBL_SIZE))
    val_display.addWidget(create_label(mag_lbl, RIGHT, LBL_FONT, LBL_SIZE))
    val_display.addWidget(create_label(skl_lbl, RIGHT, LBL_FONT, LBL_SIZE))
    val_display.addWidget(create_label(spd_lbl, RIGHT, LBL_FONT, LBL_SIZE))
    val_display.addWidget(create_label(lck_lbl, RIGHT, LBL_FONT, LBL_SIZE))
    val_display.addWidget(create_label(def_lbl, RIGHT, LBL_FONT, LBL_SIZE))
    val_display.addWidget(create_label(mdf_lbl, RIGHT, LBL_FONT, LBL_SIZE))
    
    # Add both columns to display
    columns.addLayout(lbl_display)
    columns.addLayout(val_display)
    stat_display.addLayout(columns)

    return stat_display

def create_image(self, img_filename, width, height):
    portrait = QLabel(self)
    portrait.setPixmap(QPixmap(img_filename).scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio))
    portrait.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return portrait

# Create stat display for child's starting stats/growths
def create_child_display(self, stats, father):
    child_display = QVBoxLayout()

    # Add portrait Icon and Name of Child
    
    child_display.addWidget(create_image(self, 'Images/Portraits/{}.png'.format(stats.Name), IMG_WIDTH, IMG_HEIGHT))
    child_display.addWidget(create_label(str(stats.Name), CENTER, TITLE_FONT, TITLE_SIZE))
    
    # Add stats and growths columns
    stats_and_growths = QHBoxLayout()
    stats_and_growths.addLayout(create_stat_display(self, stats, "Stats"), 10)
    stats_and_growths.addWidget(vertical_separator(LINE_WIDTH, getColor(SEP_COL)), 1)
    stats_and_growths.addLayout(create_stat_display(self, convert_growths(child_growths[stats.Name][father]), "Growths"), 10)
    child_display.addLayout(stats_and_growths)
    return child_display

def create_child_stat_display(self, stats, father):
    child_display = QVBoxLayout()

    # Add portrait Icon and Name of Child
    child_display.addWidget(create_image(self, 'Images/Portraits/{}.png'.format(stats.Name), IMG_WIDTH, IMG_HEIGHT))
    child_display.addWidget(create_label(str(stats.Name), CENTER, TITLE_FONT, TITLE_SIZE))
    
    # Add stats and growths columns
    stats_display = create_stat_display(self, stats, "Stats")
    child_display.addLayout(stats_display)
    return child_display

def create_child_growths_display(self, child, father):
    child_display = QVBoxLayout()

    # Add portrait Icon and Name of Child
    child_display.addWidget(create_image(self, 'Images/Portraits/{}.png'.format(child), IMG_WIDTH, IMG_HEIGHT))
    child_display.addWidget(create_label(child, CENTER, TITLE_FONT, TITLE_SIZE))
    
    # Add stats and growths columns
    growths_display = create_stat_display(self, convert_growths(child_growths[child][father]), "Growths")
    child_display.addLayout(growths_display)
    return child_display

def horizontal_separator(width, color):
    separator = QFrame()
    separator.setFrameShape(QFrame.Shape.HLine)
    separator.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    separator.setLineWidth(width)
    palette = separator.palette()
    palette.setColor(palette.ColorRole.Window, color)
    separator.setPalette(palette)
    return separator
    
def vertical_separator(width, color):
    separator = QFrame()
    separator.setFrameShape(QFrame.Shape.VLine)
    separator.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    separator.setLineWidth(width)
    palette = separator.palette()
    palette.setColor(palette.ColorRole.Window, color)
    separator.setPalette(palette)
    return separator

def getColor(COL):
    return QtGui.QColor(COL[0], COL[1], COL[2])

def convert_stat_growth(growth):
        return round(growth*100)

def convert_growths(growths):
    # Converts growths from decimal to %
    converted = Stats(
        "",
        "Converted Growths",
        convert_stat_growth(growths.HP),
        convert_stat_growth(growths.HP),
        convert_stat_growth(growths.Mag),
        convert_stat_growth(growths.Skl),
        convert_stat_growth(growths.Spd),
        convert_stat_growth(growths.Lck),
        convert_stat_growth(growths.Def),
        convert_stat_growth(growths.Mdf)
    )
    return converted

def display_error_msg(error_msg):
        msg_box = QMessageBox()
        msg_box.setText(error_msg)
        msg_box.exec()