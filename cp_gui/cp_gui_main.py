# -*- coding: utf-8 -*-

from __future__ import print_function

# Info
__author__ = 'Disco Hammer'
__copyright__ = 'Copyright 2017,  Dragon Unit Framestore LDN 2017'
__version__ = '0.1'
__email__ = 'gsorchin@framestore.com'
__status__ = 'Prototype'

import sys

import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
import shiboken2
import maya.cmds as mc
import maya.OpenMayaUI as mui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

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
gDEBUG = False

# ---------------------GUI----------------------------- #


class CraniumPostWindow(MayaQWidgetDockableMixin, qw.QDialog):
    def __init__(self):
        super(CraniumPostWindow, self).__init__()
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Cranium Post 0.1')
        self.setMinimumWidth(300)
        self.setMinimumHeight(380)

        # Attributes
        self._dock_widget = None
        self._dock_name = None

        # --- Main Window Layout --- #
        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(8)

        scroll_area = qw.QScrollArea()
        scroll_area.setFrameStyle(qw.QFrame.Plain | qw.QFrame.NoFrame)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(qc.Qt.NoFocus)
        scroll_area.setHorizontalScrollBarPolicy(qc.Qt.ScrollBarAlwaysOff)
        self.layout().addWidget(scroll_area)

        main_widget = qw.QWidget()
        main_layout = qw.QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setAlignment(qc.Qt.AlignTop)
        main_widget.setLayout(main_layout)
        scroll_area.setWidget(main_widget)

        new_widget = CraniumPostWidget()
        main_layout.addWidget(new_widget)

        # Footer
        footer_widget = Footer()
        self.layout().addWidget(footer_widget)

    def connect_dock_widget(self, dock_name, dock_widget):  # Unused because using MayaMixin
        self._dock_widget = dock_widget
        self._dock_name = dock_name

    '''    
    # def close(self):
    #     if self._dock_widget:
    #         mc.deleteUI(self._dock_name)
    #     else:
    #         self.qw.QDialog.close()
    #
    #     self._dock_name = None
    #     self._dock_widget = None
    '''


class CraniumPostWidget(qw.QFrame):
    def __init__(self):  # -- Constructor
        super(CraniumPostWidget, self).__init__()
        # self.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)
        self.setLayout(qw.QVBoxLayout())

        # Attributes
        self.source = None
        self.target = None

        # --- SETUP Widget --- #
        setup_widget = qw.QWidget()
        setup_widget.setLayout(qw.QVBoxLayout())
        setup_widget.layout().setContentsMargins(0, 0, 0, 0)
        setup_widget.layout().setSpacing(4)
        setup_widget.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Fixed)

        # Head Splitter
        setup_splitter = Splitter("SET-UP", True, (253, 95, 0))
        setup_widget.layout().addWidget(setup_splitter)  # Widget Splitter

        # --- Setup Fields Start ---#

        # Set as Source
        self.set_source_layout = Picker('Set as Source:', 'Select source...', 'Set')
        setup_widget.layout().addLayout(self.set_source_layout)

        # Source Actions
        source_actions = qw.QHBoxLayout()
        source_actions.setSpacing(2)
        setup_widget.layout().addLayout(source_actions)

        self.cache_skin_weights = ActionButton('Cache Skin Weights')
        self.export_skin_weights = ActionButton('Export Skin Weights')

        source_actions.addSpacing(12)
        source_actions.addLayout(self.cache_skin_weights)
        source_actions.addLayout(self.export_skin_weights)
        source_actions.addSpacing(12)

        # Splitter
        setup_widget.layout().addLayout(SplitterLayout())

        # Set as Target
        self.set_target_layout = Picker('Set as Target: ', 'Select target...', 'Set')
        setup_widget.layout().addLayout(self.set_target_layout)

        # Build Help Locators

        build_layout = qw.QHBoxLayout()
        build_layout.setSpacing(2)
        setup_widget.layout().addLayout(build_layout)

        self.build_help_locators = ActionButton('Build Help Locators')

        build_layout.addSpacing(12)
        build_layout.addLayout(self.build_help_locators)
        build_layout.addSpacing(12)

        # Update and connect joints
        joints_layout = qw.QHBoxLayout()
        joints_layout.setSpacing(2)
        self.update_joints = ActionButton('Update Joints')
        self.connect_joints = ActionButton('Connect Joints')

        joints_layout.addSpacing(12)
        joints_layout.addLayout(self.update_joints)
        joints_layout.addLayout(self.connect_joints)
        joints_layout.addSpacing(12)

        setup_widget.layout().addLayout(joints_layout)

        # Splitter
        setup_widget.layout().addLayout(SplitterLayout())

        # Add the setup widget to the main layout
        self.layout().addWidget(setup_widget)

        # Log Splitter
        log_splitter = Splitter("LOG", True, (253, 95, 0))
        setup_widget.layout().addWidget(log_splitter)  # Widget Splitter

        # MONITOR - Widget
        self.monitor = Monitor()
        self.layout().addWidget(self.monitor)

        # - Connections - #

        # Fields
        self.set_source_layout.btn.clicked.connect(self._set_source_mesh)
        self.cache_skin_weights.btn.clicked.connect(self._cache_skin_weights)
        # self.export_skin_weights.btn.clicked.connect(self.export_skin_weights)
        self.set_target_layout.btn.clicked.connect(self._set_target_mesh)
        self.build_help_locators.btn.clicked.connect(self._build_help_locators)
        self.update_joints.btn.clicked.connect(self._update_joints)
        self.connect_joints.btn.clicked.connect(self._connect_joints)

    # - Instance Methods - #

    # ------------------------------------------------- #

    def _check_gui_requirements(self):
        if self.source:
            self.cache_skin_weights.btn.setEnabled(True)
            self.export_skin_weights.btn.setEnabled(True)
        else:
            self.cache_skin_weights.btn.setEnabled(False)
            self.export_skin_weights.btn.setEnabled(False)

        if self.target and self.source:
            self.build_help_locators.btn.setEnabled(True)

            if self.target.locs_and_joints:
                self.update_joints.btn.setEnabled(True)
                self.connect_joints.btn.setEnabled(True)
            else:
                self.update_joints.btn.setEnabled(False)
                self.connect_joints.btn.setEnabled(False)
        else:
            self.build_help_locators.btn.setEnabled(False)

    # ------------------------------------------------- #

    def _set_source_mesh(self):
        try:
            self.source = cp_file_ops.set_as_source()
        except AttributeError:
            print(cp_file_ops.to_console('Please select a valid source skinned mesh'))
            # print('[Cranium-Post]: Please select a valid source skinned mesh')
        else:
            self.set_source_layout.line_edit.setPlaceholderText(str(self.source.name))
            self._check_gui_requirements()

    def _cache_skin_weights(self):
        try:
            self.source.build_weights_association()
        except Exception as ce:
            print(ce)
        else:
            print(self.source.vertex_weights)
            self.monitor.update_monitor(cp_file_ops.to_console('Cached skin weights'))

    def _set_target_mesh(self):
        try:
            self.target = cp_file_ops.set_as_target()
        except AttributeError:
            print(cp_file_ops.to_console('Please select a valid target mesh'))
            # print('[Cranium-Post]: Please select a valid target mesh')
        else:
            self.set_target_layout.line_edit.setPlaceholderText(str(self.target.name))
            self._check_gui_requirements()

    def _build_help_locators(self):
        self.target.build_help_locators(self.source.joint_positions)
        self._check_gui_requirements()

    def _update_joints(self):
        self.target.update_joints()

    def _connect_joints(self):
        self.target.connect_joints(self.source.joint_hierarchy)

    def _clear_fields(self):
        self.source = None
        self.target = None

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
        self.setSpacing(6)
        self.setAlignment(qc.Qt.AlignCenter)

        self.lbl = qw.QLabel()
        self.lbl.setText(label)

        self.line_edit = qw.QLineEdit()
        self.line_edit.setPlaceholderText(line)
        # self.line_edit.setMaximumWidth(144)
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

        self.setContentsMargins(2, 1, 2, 1)
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

        self.first_line = qw.QFrame()
        self.first_line.setFrameStyle(qw.QFrame.HLine)
        self.layout().addWidget(self.first_line)

        main_color = 'rgba(%s, %s, %s, 255)' % color
        shadow_color = 'rgba(45, 45, 45, 255)'

        bottom_border = ''

        if shadow:
            bottom_border = 'border-bottom:2px solid %s' % shadow_color

        style_sheet = "border:0px solid rgba(0,0,0,0); \
                       background-color: %s; \
                       max-height:2px; \
                       %s" % (main_color, bottom_border)

        self.first_line.setStyleSheet(style_sheet)

        if text is None:
            return

        self.first_line.setMaximumWidth(5)

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

class Monitor(qw.QWidget):
    def __init__(self):
        super(Monitor, self).__init__()
        self.setSizePolicy(qw.QSizePolicy.Minimum,
                           qw.QSizePolicy.Fixed)
        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(2, 0, 2, 0)
        self.layout().setSpacing(4)

        self.monitor_multi_line = qw.QTextEdit()
        self.monitor_multi_line.setMaximumHeight(100)
        self.monitor_multi_line.setDisabled(True)
        self._startup_monitor()

        clear_layout = qw.QHBoxLayout()
        clear_layout.setContentsMargins(0, 0, 1, 0)
        clear_layout.setAlignment(qc.Qt.AlignRight)

        self.clear_btn = qw.QPushButton()
        self.clear_btn.setText('Clear')
        self.clear_btn.setMaximumWidth(self.clear_btn.fontMetrics().boundingRect(self.clear_btn.text()).width() + 12)

        clear_layout.addWidget(self.clear_btn)

        self.layout().addWidget(self.monitor_multi_line)
        self.layout().addLayout(clear_layout)

        # - Connections - #
        self.clear_btn.clicked.connect(self._clear_monitor)

    def _startup_monitor(self):
        self.monitor_multi_line.setText(cp_file_ops.to_console('Monitor'))

    def update_monitor(self, message):
        self.monitor_multi_line.append(message)

    def _clear_monitor(self):
        self.monitor_multi_line.clear()
        self._startup_monitor()


# ----------------------------------------------------- #

class Footer(qw.QWidget):
    def __init__(self):
        super(Footer, self).__init__()
        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(4, 4, 16, 4)
        self.layout().setSpacing(2)
        self.layout().setAlignment(qc.Qt.AlignRight)
        self.setSizePolicy(qw.QSizePolicy.Minimum,
                           qw.QSizePolicy.Fixed)

        self.lbl = qw.QLabel()
        self.lbl.setText('© 2017 Dragon Unit - Framestore LDN')
        self.layout().addWidget(self.lbl)


class SFooter(Splitter):
    def __init__(self, *args, **kwargs):
        super(SFooter, self).__init__(*args, **kwargs)

        self.first_line.setMaximumWidth(50)


# ----------------------------------------------------- #

# General Definitions

def create(docked=True):
    global gDIALOG
    print(gDIALOG)
    if gDIALOG is None:
        gDIALOG = CraniumPostWindow()
        print(gDIALOG)

    print(gDIALOG)
    if docked is True:
        gDIALOG.show(dockable=True,
                     area='right',
                     allowedArea=['right', 'left'])

        '''
        # ptr = mui.MQtUtil.mainWindow()
        # main_window = shiboken2.wrapInstance(long(ptr), qw.QWidget)
        #
        # gDIALOG.setParent(main_window)
        # size = gDIALOG.size()
        #
        # print(shiboken2.getCppPointer(gDIALOG))
        #
        # name = mui.MQtUtil.fullName(long(shiboken2.getCppPointer(gDIALOG)[0]))
        # name = 'MayaWindow'
        # print('name' + name)
        # dock = mc.dockControl(
        #     allowedArea=['right', 'left'],
        #     area='right',
        #     content=name,
        #     floating=False,
        #     width=size.width(),
        #     height=size.height(),
        #     label='Cranium Post 0.1'
        # )
        #
        # # widget = mui.MQtUtil.findControl(dock)
        # # dock_widget = shiboken2.wrapInstance(long(widget), qw.QWidget)
        # # gDIALOG.connectDockWidget(dock, dock_widget)
        '''
    else:
        gDIALOG.show(dockable=False,
                     floating=True)


def delete():
    global gDIALOG
    if gDIALOG is None:
        return

    gDIALOG.deleteLater()
    gDIALOG = None
