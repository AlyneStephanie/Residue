import sys
from urllib import response
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QWidget, QGridLayout,QPushButton, QApplication, QLineEdit, QLabel, QErrorMessage, QGroupBox, QHBoxLayout, QRadioButton)
import alpha_curve
from complex_parser import Complex, calc
import residue

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.grid()
        super(MplCanvas, self).__init__(fig)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Program 4')

        self.showMaximized()

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        # Gamma Curve

        groupbox_gamma = QGroupBox("Gamma Curve")
        grid_layout.addWidget(groupbox_gamma, 0, 0, 1, 0)
        gamma_box = QGridLayout()


        
        # Canonical Equation

        hk_label_1 = QLabel(" ( x - ")
        gamma_box.addWidget(hk_label_1, 3, 0)
        
        self.h_input = QLineEdit("0")
        self.h_input.setDisabled(True)
        gamma_box.addWidget(self.h_input, 3, 1)

        hk_label_2 = QLabel(" )\u00B2 + i ( y - ")
        gamma_box.addWidget(hk_label_2, 3, 2)
        
        self.k_input = QLineEdit("0")
        self.k_input.setDisabled(True)
        gamma_box.addWidget(self.k_input, 3, 3)

        hk_label_3 = QLabel(" )\u00B2 = (")
        gamma_box.addWidget(hk_label_3, 3, 4)


        # r

        self.r_input = QLineEdit("2.5")
        gamma_box.addWidget(self.r_input, 3, 5)

        hk_label_4 = QLabel(" )\u00B2")
        gamma_box.addWidget(hk_label_4, 3, 6)


        groupbox_gamma.setLayout(gamma_box)
        

        # n
        groupbox_n = QGroupBox("n")
        grid_layout.addWidget(groupbox_n, 1, 0)
        n_box = QGridLayout()

        n_label = QLabel("n = ")
        n_box.addWidget(n_label, 0, 0)

        self.n_input = QLineEdit("3")
        n_box.addWidget(self.n_input, 0, 1)

        groupbox_n.setLayout(n_box)


        # m
        groupbox_m = QGroupBox("m")
        grid_layout.addWidget(groupbox_m, 1, 1)
        m_box = QGridLayout()

        m_label = QLabel("m = ")
        m_box.addWidget(m_label, 0, 0)

        self.m_input = QLineEdit("2")
        m_box.addWidget(self.m_input, 0, 1)

        groupbox_m.setLayout(m_box)


        # a
        groupbox_a = QGroupBox("a")
        grid_layout.addWidget(groupbox_a, 1, 2)
        a_box = QGridLayout()

        a_label = QLabel("a = ")
        a_box.addWidget(a_label, 0, 0)

        self.a_input = QLineEdit("-1")
        a_box.addWidget(self.a_input, 0, 1)

        groupbox_a.setLayout(a_box)


        # b
        groupbox_b = QGroupBox("b")
        grid_layout.addWidget(groupbox_b, 1, 3)
        b_box = QGridLayout()

        b_label = QLabel("b = ")
        b_box.addWidget(b_label, 0, 0)

        self.b_input = QLineEdit("-2")
        b_box.addWidget(self.b_input, 0, 1)

        groupbox_b.setLayout(b_box)


        # c
        groupbox_c = QGroupBox("c")
        grid_layout.addWidget(groupbox_c, 1, 4)
        c_box = QGridLayout()

        c_label = QLabel("c = ")
        c_box.addWidget(c_label, 0, 0)

        self.c_input = QLineEdit("-4")
        c_box.addWidget(self.c_input, 0, 1)

        groupbox_c.setLayout(c_box)



        # Buttons
        self.calculateButton = QPushButton("Calculate")
        self.calculateButton.clicked.connect(self.calculate)
        grid_layout.addWidget(self.calculateButton, 2, 2)
        self.calculateButton.resize(150, 50)

        self.resetButton = QPushButton("Reset")
        self.resetButton.clicked.connect(self.reset)
        grid_layout.addWidget(self.resetButton, 2, 3)

        self.closeButton = QPushButton("Close", self)
        self.closeButton.setToolTip("Close Application") #Hover over the button
        self.closeButton.clicked.connect(self.close)
        grid_layout.addWidget(self.closeButton, 2, 4)

        
        # Canvas
        groupbox_canvas = QGroupBox("Canvas")
        grid_layout.addWidget(groupbox_canvas, 3, 0, 1, 4)
        canvas_box = QGridLayout()

        self.canvas = MplCanvas(self, width=5, height=10, dpi=100)
        canvas_box.addWidget(self.canvas, 0, 0)

        groupbox_canvas.setLayout(canvas_box)

        # Reservations
        groupbox_Res = QGroupBox("Res")
        grid_layout.addWidget(groupbox_Res, 4, 0, 1, 0)
        Res_box = QGridLayout()

        self.Res_label = QLabel(" ")
        Res_box.addWidget(self.Res_label, 0, 0)

        groupbox_Res.setLayout(Res_box)


    def calculate(self):
        
        self.canvas.axes.cla()
        # strip -> remueve espacios
        r_value = float(self.r_input.text().strip())
        n_value = abs(int(self.n_input.text().strip()))
        m_value = abs(int(self.m_input.text().strip()))
        a_value = int(self.a_input.text().strip())
        b_value = int(self.b_input.text().strip())
        c_value = int(self.c_input.text().strip())
        
        
        res_circle = alpha_curve.alpha_curve(a_value, b_value, c_value, r_value)

        if res_circle == False:
            self.Res_label.setText("Indeterminate")
        else:
            if m_value == 0:
                self.Res_label.setText("Order of differentiation must be nonnegative")
            else:
                resp = residue.residue(a_value, b_value, c_value, n_value, m_value, r_value)
                result = f"{resp}"
                self.Res_label.setText(result)

        self.canvas.axes.set_aspect( 1 )
        x_lim = max(r_value, abs(b_value))
        y_lim = max(r_value, abs(a_value),abs(c_value))
        self.canvas.axes.set_xlim([- x_lim - 1, x_lim + 1])
        self.canvas.axes.set_ylim([- y_lim - 1, y_lim + 1])
        result_circle = plt.Circle(( 0 , 0 ), r_value, color='g' )
        self.canvas.axes.add_artist( result_circle)
        self.canvas.axes.plot(0, a_value,  marker = 'o',  linewidth=2, color='y')
        self.canvas.axes.plot(b_value, 0,  marker = 'o',  linewidth=2, color='r')
        self.canvas.axes.plot(0, -c_value,  marker = 'o',  linewidth=2, color='b')
        self.canvas.axes.grid()

        self.canvas.draw()

        print(res_circle)

        
    def reset(self):
        self.a_input.setText("")
        self.b_input.setText("")
        self.c_input.setText("")
        self.r_input.setText("")
        self.n_input.setText("")
        self.m_input.setText("")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
