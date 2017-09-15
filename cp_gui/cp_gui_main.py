from __future__ import print_function

import os
import sys

CpPath = 'E:\\dev\\python\\maya\\cranium_post'  # Change to network GIT

if not CpPath in sys.path:
    sys.path.append(CpPath)

from cp_ops import cp_file_ops; reload(cp_file_ops)

import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw

# Info
__author__   = 'Disco Hammer'
__copyright__ = 'Copyright 2017,  Dragon Unit Framestore LDN 2017'
__version__ = '0.1'
__email__ = 'gsorchin@framestore.com'
__status__ = 'Prototype'

gDIALOG = None
gPROMPT = None


#---------------------GUI-----------------------------#

class CpMainWindow(qw.QDialog):
    def __init__(self): # -- Constructor
        super(CpMainWindow, self).__init__()

        ## Main Window

        self.setWindowTitle('Cranium Post')
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        #self.setFixedHeight(512)
        self.setFixedWidth(300)
        #---Main Window Layout---
        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)
        self.layout().setSpacing(10)
        self.layout().setAlignment(qc.Qt.AlignTop)


        #---SETUP Widget---
        setup_widget = qw.QWidget()
        setup_widget.setLayout(qw.QVBoxLayout())
        setup_widget.layout().setContentsMargins(0,0,0,0)
        setup_widget.layout().setSpacing(2)
        setup_widget.setSizePolicy(qw.QSizePolicy.Minimum,
                                   qw.QSizePolicy.Fixed)

        setup_splitter = Splitter("SET-UP", True,(253,95,0))
        setup_widget.layout().addWidget(setup_splitter) ## Widget Splitter

        #---Active Fields Start---#

        # Set as Source
        set_source_layout = qw.QHBoxLayout()
        set_source_layout.setContentsMargins(2, 0, 2, 0)
        set_source_layout.setSpacing(4)
        set_source_layout.setAlignment(qc.Qt.AlignRight)

        setup_widget.layout().addLayout(set_source_layout)

        set_source_lbl = qw.QLabel()
        set_source_lbl.setText('Set as Source: ')

        self.set_source_le = qw.QLineEdit()
        self.set_source_le.setPlaceholderText('Select source...')
        self.set_source_le.setMaximumWidth(162)
        self.set_source_le.setEnabled(False)

        set_source_txt = 'Set'
        self.set_source_btn = qw.QPushButton()
        self.set_source_btn.setText(set_source_txt)
        self.set_source_btn.setMaximumWidth(self.set_source_btn.fontMetrics().boundingRect(set_source_txt).width() + 24)

        set_source_layout.addWidget(set_source_lbl)
        set_source_layout.addWidget(self.set_source_le)
        set_source_layout.addWidget(self.set_source_btn)

        # Set as Target
        set_target_layout = qw.QHBoxLayout()
        set_target_layout.setContentsMargins(2, 0, 2, 0)
        set_target_layout.setSpacing(4)
        set_target_layout.setAlignment(qc.Qt.AlignRight)

        setup_widget.layout().addLayout(set_target_layout)

        set_target_lbl = qw.QLabel()
        set_target_lbl.setText('Set as Target: ')

        self.set_target_le = qw.QLineEdit()
        self.set_target_le.setPlaceholderText('Select Target...')
        self.set_target_le.setMaximumWidth(162)
        self.set_target_le.setEnabled(False)

        set_target_txt = 'Set'
        self.set_target_btn = qw.QPushButton()
        self.set_target_btn.setText(set_target_txt)
        self.set_target_btn.setMaximumWidth(self.set_target_btn.fontMetrics().boundingRect(set_target_txt).width() + 24)

        set_target_layout.addWidget(set_target_lbl)
        set_target_layout.addWidget(self.set_target_le)
        set_target_layout.addWidget(self.set_target_btn)

        '''
        project = FileOrFolderField('Project Folder', False)
        setup_widget.layout().addLayout(project)
        setup_widget.layout().addLayout(SplitterLayout()) ## Section Splitter
        gOBJDICT[PRJ] = project

        master = FileOrFolderField('Master Scene', True)
        setup_widget.layout().addLayout(master)
        setup_widget.layout().addLayout(SplitterLayout()) ## Section Splitter
        gOBJDICT[MST] = master

        batch = FileOrFolderField('Batch Folder', False)
        setup_widget.layout().addLayout(batch)
        setup_widget.layout().addLayout(SplitterLayout()) ## Section Splitter
        gOBJDICT[BTC] = batch

        output = FileOrFolderField('Output Folder', False)
        setup_widget.layout().addLayout(output)
        setup_widget.layout().addLayout(SplitterLayout()) ## Section Splitter
        gOBJDICT[OUT] = output

        ## Run Button

        run_btn_layout = qg.QHBoxLayout()
        run_btn_layout.setContentsMargins(4,0,4,0)
        run_btn_layout.setSpacing(2)
        setup_widget.layout().addLayout(run_btn_layout)

        self.run_btn = qg.QPushButton('Run')
        self.run_btn.setEnabled(False)

        run_btn_layout.layout().addWidget(self.run_btn)
        setup_widget.layout().addLayout(SplitterLayout())
        
        '''


        ## Add the setup widget to the main layout

        self.layout().addWidget(setup_widget) ## Add widget to main layout

        '''

        #MONITOR - Widget
        monitor_widget = qg.QWidget()
        monitor_widget.setLayout(qg.QVBoxLayout())
        monitor_widget.layout().setContentsMargins(0,0,0,0)
        monitor_widget.layout().setSpacing(2)
        monitor_widget.setSizePolicy(qg.QSizePolicy.Minimum,
                                     qg.QSizePolicy.Fixed)

        self.layout().addWidget(monitor_widget)

        #MONITOR Layout
        monitor_layout = qg.QHBoxLayout()
        monitor_layout.setContentsMargins(4,0,4,0)
        monitor_layout.setSpacing(2)


        monitor_widget.layout().addLayout(monitor_layout)

        self.monitor_multiline = qg.QTextEdit('<< Terminal')
        self.monitor_multiline.setMaximumHeight(100)
        self.monitor_multiline.setDisabled(True)

        monitor_layout.layout().addWidget(self.monitor_multiline)

        #CLEAR Layout
        clear_layout = qg.QHBoxLayout()
        clear_layout.setContentsMargins(4,0,4,0)
        clear_layout.setSpacing(2)
        clear_layout.setAlignment(qc.Qt.AlignRight)

        monitor_widget.layout().addLayout(clear_layout)

        self.clear_btn = qg.QPushButton('Clear')
        self.clear_btn.setFixedWidth(50)

        clear_layout.layout().addWidget(self.clear_btn)

        #COPYRIGHT-Widget
        copyRight_widget = qg.QWidget()
        copyRight_widget.setLayout(qg.QVBoxLayout())
        copyRight_widget.layout().setContentsMargins(0,0,0,0)
        copyRight_widget.layout().setSpacing(2)
        copyRight_widget.layout().setAlignment(qc.Qt.AlignBottom)
        copyRight_widget.setSizePolicy(qg.QSizePolicy.Minimum,
                                       qg.QSizePolicy.Fixed)

        self.layout().addWidget(copyRight_widget)

        #Copyright Layout
        copyRight_layout = qg.QHBoxLayout()
        copyRight_layout.setContentsMargins(4,0,4,0)
        copyRight_layout.setSpacing(2)
        copyRight_widget.layout().addLayout(copyRight_layout)

        copy = u"\u00a9"
        lbl_text = copy + " Dragon Unit - Framestore LDN 2017"
        copyRight_lbl = qg.QLabel()
        copyRight_lbl.setText(lbl_text)
        copyRight_lbl.setAlignment(qc.Qt.AlignRight)

        copyRight_layout.layout().addWidget(copyRight_lbl)
        
        '''

        ### Connections

        #Field Values
        self.set_source_btn.clicked.connect(self._set_source_mesh)

        '''

        #Run Button
        project.fof_le.textChanged.connect(lambda: self._validate_values(gOBJDICT))
        master.fof_le.textChanged.connect(lambda: self._validate_values(gOBJDICT))
        batch.fof_le.textChanged.connect(lambda: self._validate_values(gOBJDICT))
        output.fof_le.textChanged.connect(lambda: self._validate_values(gOBJDICT))

        #Terminal Widget
        self.clear_btn.clicked.connect(self._clearLog)
        
        

    '''
    ## Internal Definitions

    #-------------------------------------------------#

    def _set_source_mesh(self):

        source = cp_file_ops.set_as_source()
        self.set_source_le.setPlaceholderText(source)

    '''
    def _updateTerminal(self, string):

        self.monitor_multiline.append("<< " + string)

    #-------------------------------------------------#

    def _clearLog(self):

        self.monitor_multiline.clear()

    #-------------------------------------------------#

    def _get_field_values(self, fields):

        paths = [i._return_field_value() for i in fields]

        return paths
    #-------------------------------------------------#

    def onClickRun(self, fields):

        field_values = self._get_field_values(fields)
        print field_values

        nFiles = None #ikb_ops.get_files_to_batch(field_values[2],'\\*.c3d')
        mScene = field_values[1].split('\\')
        print mScene[-1]

        report = 'Are you sure you want to process {} motion files on {}?'.format(len(nFiles),mScene[-1])

        user_check = promptToUser(qg.QMessageBox.Warning, report, "Approved")
        user_check.exec_()

        selection = user_check.clickedButton().text() #Gets the user selection

        if selection == 'OK': #If user selection is positive, IK Setup runs
            pass#ikb_ops.build_batch(gPATHDICT)

    #-------------------------------------------------#

    def _validate_values(self, gOBJDICT):

        global gPATHDICT

        for k,v in gOBJDICT.items():
            test_v = v._return_field_value()
            if os.path.isfile(test_v) or os.path.isdir(test_v):
                gPATHDICT[k] = test_v
            else:
                continue


        if len(gOBJDICT.items()) == len(gPATHDICT.items()):

            self.run_btn.setEnabled(True)

        else:

            self.run_btn.setEnabled(False)


#-----------------------------------------------------#

class FileOrFolderField(qw.QHBoxLayout):
    def __init__(self, title = None, file_or_folder = True):
        super(FileOrFolderField, self).__init__()

        ## Folder
        self.setContentsMargins(4,0,4,0)
        self.setSpacing(2)
        #parent.layout().addLayout(self.fof_layout)

        self.fof_lbl = qw.QLabel()
        self.fof_lbl.setText(title)
        self.fof_le = qw.QLineEdit()

        self.fof_le.setPlaceholderText('Path...')
        self.fof_le.setEnabled(False)
        self.fof_le.setMaximumWidth(242)

        self.fof_btn = qw.QPushButton()
        self.fof_btn.setText('Set')
        ktext = self.fof_btn.text()
        kwidth = self.fof_btn.fontMetrics().boundingRect(ktext).width() + 32
        self.fof_btn.setMaximumWidth(kwidth)
        self.fof_btn.setEnabled(True)

        self.layout().addWidget(self.fof_lbl)
        self.layout().addWidget(self.fof_le)
        self.layout().addWidget(self.fof_btn)

        ## Connections

        self.fof_btn.clicked.connect(lambda:self._getPath(title,file_or_folder))

        ## Internal Defs

    def _getPath(self, title, action):

        pPath = None

        if action:

            pPath, terminal = None, None#ikb_ops.get_file(title)

            if os.path.isfile(pPath) and pPath.endswith('.fbx'):

                self.fof_le.setText(pPath)
                gDIALOG._updateTerminal(terminal)

            else:

                print ('Selected file is not valid')
                gDIALOG._updateTerminal(terminal)

        else:

            pPath, terminal = None, None#ikb_ops.get_directory(title)

            if os.path.isdir(pPath):

                self.fof_le.setText(pPath)
                gDIALOG._updateTerminal(terminal)

            else:

                print ('Selected path is not valid')
                gDIALOG._updateTerminal(terminal)

    def _return_field_value(self):

        return self.fof_le.text()

#-----------------------------------------------------#

class promptToUser(qg.QMessageBox):
    def __init__(self, icon, text, op):
        qg.QMessageBox.__init__(self)

        self.setWindowTitle('fBatch Manager is talking!')
        self.setIcon(icon)
        self.setText(text)
        self.setStandardButtons(qg.QMessageBox.Ok | qg.QMessageBox.Cancel)
'''

#-----------------------------------------------------#

class Splitter(qw.QWidget):
    def __init__(self, text = None, shadow = True, color = (150,150,150)):
        super(Splitter, self).__init__()

        self.setMinimumHeight(2)
        self.setLayout(qw.QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)
        self.layout().setAlignment(qc.Qt.AlignVCenter)

        first_line = qw.QFrame()
        first_line.setFrameStyle(qw.QFrame.HLine)
        self.layout().addWidget(first_line)

        main_color   = 'rgba(%s, %s, %s, 255)' %color
        shadow_color = 'rgba(45, 45, 45, 255)'

        bottom_border = ''

        if shadow:
            bottom_border = 'border-bottom:2px solid %s' %shadow_color

        style_sheet = "border:0px solid rgba(0,0,0,0); \
                       background-color: %s; \
                       max-height:2px; \
                       %s" %(main_color, bottom_border)

        first_line.setStyleSheet(style_sheet)

        if text is None:
            return

        first_line.setMaximumWidth(5)

        font = qg.QFont()
        font.setBold(True)
        font.setItalic(True)

        text_width = qg.QFontMetrics(font)
        #text_width.inFont(font)
        width = text_width.width(text) + 16

        label = qw.QLabel()
        label.setText(text)
        label.setFont(font)
        label.setMaximumWidth(width)
        label.setAlignment(qc.Qt.AlignCenter | qc.Qt.AlignVCenter)

        self.layout().addWidget(label)

        second_line = qw.QFrame()
        second_line.setFrameStyle(qw.QFrame.HLine)
        self.layout().addWidget(second_line)

        second_line.setStyleSheet(style_sheet)

#-----------------------------------------------------#

class SplitterLayout(qw.QHBoxLayout):
    def __init__(self):
        super(SplitterLayout, self).__init__()

        self.setContentsMargins(40,2,40,2)

        layout_line = Splitter(shadow = False, color = (60,60,60))
        layout_line.setFixedHeight(1)

        self.addWidget(layout_line)

#-----------------------------------------------------#

#General Definitions

def create():
    global gDIALOG
    if gDIALOG is None:
        gDIALOG = CpMainWindow()
    gDIALOG.show()

def delete():
    global gDIALOG
    if gDIALOG is None:
        return

    gDIALOG.deleteLater()
    gDIALOG = None

create()
