from fpdf import FPDF

class PDF(FPDF):

    project = ""
    company = ""
    engineer = ""
    date = ""
    session = ""

    def header(self):
        self.set_font('Arial', size=10)
        self.set_xy(10, 10)
        self.cell(60, 5, self.project, 0, 0, 'L')

        self.set_font('Arial', size=10)
        self.set_xy(10, 15)
        self.cell(60, 5, self.date, 0, 0, 'L')

        self.set_font('Arial', 'B', 15)
        self.set_xy(75, 10)
        self.cell(60, 10, self.session, 0, 0, 'C')

        self.set_font('Arial', size=10)
        self.set_xy(-70, 10)
        self.cell(60, 5, self.company, 0, 0, 'R')
        self.set_xy(-70, 15)
        self.cell(60, 5, self.engineer, 0, 0, 'R')

        # Line break
        self.ln(8)
        self.line(10,23,200,23)

    # Page footer
    def footer(self):
        # Position at 1 cm from bottom
        self.set_y(-10)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def notes(self, noteData):
        self.ln(5)
        self.set_font('Arial', size=10)
        self.multi_cell(w=0, h=5, txt=noteData)
        self.ln(5)

    def taskTitle(self):
        self.set_font('Arial', size=14)
        self.cell(0, 10, 'Tasks:', 0, 0, 'L')
        self.ln()

    def tasks(self, taskTitle, result):
        self.set_font('Arial', size=12)
        self.set_x(15)
        self.multi_cell(w=0, h=5, txt=taskTitle)
        y = self.get_y()
        self.line(15, y, 200, y)
        self.set_font('Arial', size=10)
        self.set_x(15)
        self.multi_cell(w=0, h=5, txt=result)
        br = 5
        if result == "":
            br = 20
        self.ln(br)

    def logTitle(self):
        self.set_font('Arial', size=14)
        self.cell(0, 10, 'Logs:', 0, 0, 'L')
        self.ln()

    def setTitle(self):
        self.set_font('Arial', size=14)
        self.cell(0, 10, 'Sets:', 0, 0, 'L')
        self.ln()

    def set(self, setTitle, note, info):
        self.set_font('Arial', size=12)
        y = self.get_y()
        self.set_xy(15, y)
        self.multi_cell(w=130, h=5, txt=setTitle)

        self.set_font('Arial', size=10)
        self.set_xy(-70, y)
        self.multi_cell(w=60, h=5, txt=info, align='R')
        y = self.get_y()
        self.line(15, y, 200, y)
        self.set_font('Arial', size=10)
        self.set_x(15)
        self.multi_cell(w=0, h=5, txt=note)
        br = 5
        if note == "":
            br = 20
        self.ln(br)

    def setProject(self, project):
        self.project = project

    def setCompany(self, company):
        self.company = company

    def setEngineer(self, engineer):
        self.engineer = engineer

    def setSession(self, session):
        self.session = session

    def setDate(self, date):
        self.date = date

