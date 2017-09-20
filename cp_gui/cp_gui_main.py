# -*- coding: utf-8 -*-

from __future__ import print_function

# Info
__author__ = 'Disco Hammer'
__copyright__ = 'Copyright 2017,  Dragon Unit Framestore LDN 2017'
__version__ = '0.1'
__email__ = 'gsorchin@framestore.com'
__status__ = 'Prototype'

import os
import sys

import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw

try:
    from cp_ops import cp_file_ops
except ImportError as e:
    CpPath = 'E:\\dev\\python\\maya\\cranium_post'  # Change to network GIT
    sys.path.append(CpPath)
    from cp_ops import cp_file_ops

reload(cp_file_ops)


# - Globals - #
gDIALOG = None
gPROMPT = None

# ---------------------GUI----------------------------- #


class CpMainWindow(qw.QDialog):
    def __init__(self):  # -- Constructor
        super(CpMainWindow, self).__init__()

        # Attributes
        self.source = None
        self.target = None

        # Main Window
        self.setWindowTitle('Cranium Post 0.1')
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        # self.setFixedHeight(512)
        self.setFixedWidth(300)

        # --- Main Window Layout --- #
        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.layout().setSpacing(10)
        self.layout().setAlignment(qc.Qt.AlignTop)

        # --- SETUP Widget --- #
        setup_widget = qw.QWidget()
        setup_widget.setLayout(qw.QVBoxLayout())
        setup_widget.layout().setContentsMargins(0, 0, 0, 0)
        setup_widget.layout().setSpacing(2)
        setup_widget.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Fixed)

        setup_splitter = Splitter("SET-UP", True, (253, 95, 0))
        setup_widget.layout().addWidget(setup_splitter)  # Widget Splitter

        # --- Setup Fields Start ---#

        # Set as Source
        self.set_source_layout = Picker('Set as Source: ', 'Select source...', 'Set')
        setup_widget.layout().addLayout(self.set_source_layout)

        # Set as Target
        self.set_target_layout = Picker('Set as Target: ', 'Select target...', 'Set')
        setup_widget.layout().addLayout(self.set_target_layout)

        # Splitter
        setup_widget.layout().addLayout(SplitterLayout())

        # Build Help Locators
        self.build_help_locators = ActionButton('Build Help Locators')
        setup_widget.layout().addLayout(self.build_help_locators)

        # Splitter
        setup_widget.layout().addLayout(SplitterLayout())

        # Update and connect joints
        joints_layout = qw.QHBoxLayout()
        self.update_joints = ActionButton('Update Joints')
        self.connect_joints = ActionButton('Connect Joints')

        joints_layout.addLayout(self.update_joints)
        joints_layout.addLayout(self.connect_joints)

        setup_widget.layout().addLayout(joints_layout)

        # Splitter
        setup_widget.layout().addLayout(SplitterLayout())

        self.footer = Footer()
        setup_widget.layout().addLayout(self.footer)

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

        self.layout().addWidget(setup_widget)  ## Add widget to main layout

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

        # - Connections - #

        # Fields
        self.set_source_layout.btn.clicked.connect(self._set_source_mesh)
        self.set_target_layout.btn.clicked.connect(self._set_target_mesh)
        self.build_help_locators.btn.clicked.connect(self._build_help_locators)
        self.update_joints.btn.clicked.connect(self._update_joints)
        self.connect_joints.btn.clicked.connect(self._connect_joints)

    # - Instance Methods - #

    # -------------------------------------------------#

    def _set_source_mesh(self):
        try:
            self.source = cp_file_ops.set_as_source()
        except AttributeError:
            print(cp_file_ops.to_console('Please select a valid source skinned mesh'))
            # print('[Cranium-Post]: Please select a valid source skinned mesh')
        else:
            self.set_source_layout.line_edit.setPlaceholderText(str(self.source.name))
            self._check_requirements()

    def _set_target_mesh(self):
        try:
            self.target = cp_file_ops.set_as_target()
        except AttributeError:
            print(cp_file_ops.to_console('Please select a valid target mesh'))
            # print('[Cranium-Post]: Please select a valid target mesh')
        else:
            self.set_target_layout.line_edit.setPlaceholderText(str(self.target.name))
            self._check_requirements()

    def _check_requirements(self):
        if self.target and self.source:
            self.build_help_locators.btn.setEnabled(True)

        if self.target.locs_and_joints:
            self.update_joints.btn.setEnabled(True)
            self.connect_joints.btn.setEnabled(True)

    def _build_help_locators(self):
        self.target.build_help_locators(self.source.joint_positions)
        self._check_requirements()

    def _update_joints(self):
        self.target.update_joints()

    def _connect_joints(self):
        self.target.connect_joints(self.source.joint_hierarchy)

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

#-----------------------------------------------------#

class promptToUser(qg.QMessageBox):
    def __init__(self, icon, text, op):
        qg.QMessageBox.__init__(self)

        self.setWindowTitle('fBatch Manager is talking!')
        self.setIcon(icon)
        self.setText(text)
        self.setStandardButtons(qg.QMessageBox.Ok | qg.QMessageBox.Cancel)
'''


# ----------------------------------------------------- #


class Picker(qw.QHBoxLayout):

    def __init__(self, label, line, btn):
        """
        :param label: Str
        :param line: Str
        :param btn: Str
        """
        super(Picker, self).__init__()
        self.setContentsMargins(2, 0, 2, 0)
        self.setSpacing(4)
        self.setAlignment(qc.Qt.AlignRight)

        self.lbl = qw.QLabel()
        self.lbl.setText(label)

        self.line_edit = qw.QLineEdit()
        self.line_edit.setPlaceholderText(line)
        self.line_edit.setMaximumWidth(162)
        self.line_edit.setEnabled(False)

        self.btn = qw.QPushButton()
        self.btn.setText(btn)
        self.btn.setMaximumWidth(self.btn.fontMetrics().boundingRect(btn).width() + 24)

        self.addWidget(self.lbl)
        self.addWidget(self.line_edit)
        self.addWidget(self.btn)

        # - Connections - #

    '''  # Replaced by instance methods on the GUI Class
    def _pick(self):
        global gSOURCE  # TODO Not entirely in love with using globals for this
        global gTARGET

        if self.source:  # We check if the picked object should be set as source or target
            try:
                gSOURCE = cp_file_ops.set_as_source()
                self.line_edit.setPlaceholderText(str(gSOURCE.name))
            except AttributeError:
                print('[Cranium-Post]: Please select a valid source skinned mesh')

        else:
            gTARGET = cp_file_ops.set_as_target()
            self.line_edit.setPlaceholderText(str(gTARGET.name))
    '''


# ----------------------------------------------------- #


class ActionButton(qw.QHBoxLayout):
    def __init__(self, label):
        super(ActionButton, self).__init__()

        self.setContentsMargins(4, 0, 4, 0)
        self.setSpacing(2)

        self.btn = qw.QPushButton(label)
        self.btn.setEnabled(False)

        self.layout().addWidget(self.btn)


# ----------------------------------------------------- #


class Splitter(qw.QWidget):
    def __init__(self, text=None, shadow=True, color=(150, 150, 150)):
        super(Splitter, self).__init__()

        self.setMinimumHeight(2)
        self.setLayout(qw.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.layout().setAlignment(qc.Qt.AlignVCenter)

        first_line = qw.QFrame()
        first_line.setFrameStyle(qw.QFrame.HLine)
        self.layout().addWidget(first_line)

        main_color = 'rgba(%s, %s, %s, 255)' % color
        shadow_color = 'rgba(45, 45, 45, 255)'

        bottom_border = ''

        if shadow:
            bottom_border = 'border-bottom:2px solid %s' % shadow_color

        style_sheet = "border:0px solid rgba(0,0,0,0); \
                       background-color: %s; \
                       max-height:2px; \
                       %s" % (main_color, bottom_border)

        first_line.setStyleSheet(style_sheet)

        if text is None:
            return

        first_line.setMaximumWidth(5)

        font = qg.QFont()
        font.setBold(True)
        font.setItalic(True)

        text_width = qg.QFontMetrics(font)
        # text_width.inFont(font)
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


# ----------------------------------------------------- #


class SplitterLayout(qw.QHBoxLayout):
    def __init__(self):
        super(SplitterLayout, self).__init__()

        self.setContentsMargins(40, 2, 40, 2)

        layout_line = Splitter(shadow=False, color=(60, 60, 60))
        layout_line.setFixedHeight(1)

        self.addWidget(layout_line)


# ----------------------------------------------------- #

class Footer(qw.QHBoxLayout):
    def __init__(self):
        super(Footer, self).__init__()
        self.setContentsMargins(2, 0, 2, 0)
        self.setSpacing(4)
        self.setAlignment(qc.Qt.AlignRight)

        self.lbl = qw.QLabel()
        self.lbl.setText('© 2017 Framestore Capturelab, __discofocx__')
        self.addWidget(self.lbl)

# ----------------------------------------------------- #

# General Definitions


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
