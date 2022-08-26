from threading import Thread
from bs4 import BeautifulSoup
import webbrowser
import urllib.request
import requests
import datetime
import json
import sys
import os
import re
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtGui import QCursor,QIcon,QFont,QFontDatabase,QPalette,QColor,QIntValidator,QPixmap
from PyQt5.QtCore import QEvent,Qt,QPoint,pyqtSignal
from PyQt5.QtWidgets import QMenu,QComboBox,QCheckBox,QFileDialog,QColorDialog
class CTabWindow(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super(CTabWindow, self).__init__(parent)
    def resizeEvent(self, event):
        self.tabBar().setFixedWidth(self.width())
        super(CTabWindow, self).resizeEvent(event)
class HCCheckBox(QtWidgets.QCheckBox):
    entered = pyqtSignal()
    leaved = pyqtSignal()
    def enterEvent(self, event):
        super().enterEvent(event)
        self.entered.emit()
    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.leaved.emit()
class CLineEdit(QtWidgets.QLineEdit):
    def contextMenuEvent(self, event):
        contextMenu=QMenu()
        contextMenu.setFont(QtGui.QFont('Arial',9))
        contextMenu.setStyleSheet('QMenu{background-color:rgb(199,213,224);border-radius:3px;color:rgb(50,53,60)}QMenu::item {background-color: transparent;border-radius: 3px;padding:3px;margin:3px;}QMenu::item:selected {background-color:rgb(50,53,60);color:rgb(199,213,224);}QMenu::separator {border:rgb(50,53,60);border-radius: background:rgb(50,53,60);margin:3px;}')
        undoAction=contextMenu.addAction('Undo')
        redoAction=contextMenu.addAction('Redo')
        contextMenu.addSeparator()
        selectallAction=contextMenu.addAction('Select All')
        contextMenu.addSeparator()
        copyAction=contextMenu.addAction('Copy')
        cutAction=contextMenu.addAction('Cut')
        pasteAction=contextMenu.addAction('Paste')
        action=contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action==undoAction:
            self.undo()
        if action==redoAction:
            self.redo()
        if action==copyAction:
            self.copy()
        if action==cutAction:
            self.cut()
        if action==pasteAction:
            self.paste()
        if action==selectallAction:
            self.selectAll()
class CPlainTextEdit(QtWidgets.QPlainTextEdit):
    def contextMenuEvent(self, event):
        contextMenu=QMenu()
        contextMenu.setFont(QtGui.QFont('Arial',9))
        contextMenu.setStyleSheet('QMenu{background-color:rgb(199,213,224);border-radius:3px;color:rgb(50,53,60)}QMenu::item {background-color: transparent;border-radius: 3px;padding:3px;margin:3px;}QMenu::item:selected {background-color:rgb(50,53,60);color:rgb(199,213,224);}QMenu::separator{border:rgb(50,53,60);border-radius: background:rgb(50,53,60);margin:3px;}')
        undoAction=contextMenu.addAction('Undo')
        redoAction=contextMenu.addAction('Redo')
        contextMenu.addSeparator()
        selectallAction=contextMenu.addAction('Select All')
        contextMenu.addSeparator()
        copyAction=contextMenu.addAction('Copy')
        cutAction=contextMenu.addAction('Cut')
        pasteAction=contextMenu.addAction('Paste')
        action=contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action==undoAction:
            self.undo()
        if action==redoAction:
            self.redo()
        if action==copyAction:
            self.copy()
        if action==cutAction:
            self.cut()
        if action==pasteAction:
            self.paste()
        if action==selectallAction:
            self.selectAll()
class CInfoLine(QtWidgets.QLineEdit):
    def contextMenuEvent(self, event):
        contextMenu=QMenu()
        contextMenu.setFont(QtGui.QFont('Arial',9))
        contextMenu.setStyleSheet('QMenu{background-color:rgb(199,213,224);border-radius:3px;color:rgb(50,53,60)}QMenu::item {background-color: transparent;border-radius: 3px;padding:3px;margin:3px;}QMenu::item:selected {background-color:rgb(50,53,60);color:rgb(199,213,224);}QMenu::separator {border:rgb(50,53,60);border-radius: background:rgb(50,53,60);margin:3px;}')
        selectallAction=contextMenu.addAction('Select All')
        contextMenu.addSeparator()
        copyAction=contextMenu.addAction('Copy')
        action=contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action==copyAction:
            self.copy()
        if action==selectallAction:
            self.selectAll()
class CInfoPlainTextEdit(QtWidgets.QPlainTextEdit):
    def contextMenuEvent(self, event):
        contextMenu=QMenu()
        contextMenu.setFont(QtGui.QFont('Arial',9))
        contextMenu.setStyleSheet('QMenu{background-color:rgb(199,213,224);border-radius:3px;color:rgb(50,53,60)}QMenu::item {background-color: transparent;border-radius: 3px;padding:3px;margin:3px;}QMenu::item:selected {background-color:rgb(50,53,60);color:rgb(199,213,224);}QMenu::separator {border:rgb(50,53,60);border-radius: background:rgb(50,53,60);margin:3px;}')
        selectallAction=contextMenu.addAction('Select All')
        contextMenu.addSeparator()
        copyAction=contextMenu.addAction('Copy')
        action=contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action==copyAction:
            self.copy()
        if action==selectallAction:
            self.selectAll()
class scmdwd(QtWidgets.QMainWindow):
    dInfo=pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setFixedSize(839,354)
        self.setWindowIcon(QIcon('./resources/scmdwd.ico'))
        with open('./data/data.json','r') as f:
            self.data=json.load(f)
        with open('./data/list.json','r') as f:
            self.list=json.load(f)
        App_Font='Arial'
        self.list=self.list["list"]
        self.wdict={}
        self.onlyInt=QIntValidator(0, 999, self)
        self.notallowed0=QtWidgets.QFrame()
        self.notallowed0.setStyleSheet('background-color:None')
        self.notallowed0.setFixedSize(815,260)
        self.notallowed0.setCursor(QCursor(QtCore.Qt.ForbiddenCursor))
        self.notallowed0.move(12,44)
        self.notallowed1=QtWidgets.QFrame()
        self.notallowed1.setStyleSheet('background-color:None')
        self.notallowed1.setFixedSize(40,38)
        self.notallowed1.setCursor(QCursor(QtCore.Qt.ForbiddenCursor))
        self.notallowed1.move(12,304)
        self.notallowed2=QtWidgets.QFrame()
        self.notallowed2.setStyleSheet('background-color:None')
        self.notallowed2.setFixedSize(207,38)
        self.notallowed2.setCursor(QCursor(QtCore.Qt.ForbiddenCursor))
        self.notallowed2.move(620,304)
        self.SCMDWD_Label=QtWidgets.QLabel()
        self.SCMDWD_Label.setObjectName('SCMDWD_Label')
        self.SCMDWD_Label.setText('SCMD Workshop Downloader 2')
        self.SCMDWD_Label.setFont(QtGui.QFont(App_Font,9))
        self.SCMDWD_Label.setFixedSize(278,32)
        self.SCMDWD_Label.move(10,0)
        self.DownloadInfo_Label=QtWidgets.QLabel()
        self.DownloadInfo_Label.setObjectName('DownloadInfo_Label')
        self.DownloadInfo_Label.setFont(QtGui.QFont(App_Font,9))
        self.DownloadInfo_Label.setAlignment(Qt.AlignCenter)
        self.DownloadInfo_Label.setFixedSize(207,32)
        self.DownloadInfo_Label.move(620,307)
        self.DownloadListPreview_Frame=QtWidgets.QFrame()
        self.DownloadListPreview_Frame.setObjectName('DownloadListPreview_Frame')
        self.DownloadListPreview_Frame.setFixedSize(207,298)
        self.DownloadListPreview_Frame.move(620,44)
        self.Info_Frame=QtWidgets.QFrame()
        self.Info_Frame.setObjectName('Info_Frame')
        self.Info_Frame.setFixedSize(556,32)
        self.Info_Frame.move(58,310)
        self.TitleBar_Frame=QtWidgets.QFrame()
        self.TitleBar_Frame.setObjectName('TitleBar_Frame')
        self.TitleBar_Frame.setFixedSize(839,32)
        self.TitleBar_Frame.move(0,0)
        self.DownloadListPreview_Scroll=QtWidgets.QAbstractScrollArea()
        self.DownloadListPreview_Scroll.setObjectName('DownloadListPreview_Scroll')
        self.DownloadListPreview_Scroll.setFixedSize(194,234)
        self.DownloadListPreview_Scroll.move(626,76)
        self.DownloadListPreview_Button=QtWidgets.QPushButton()
        self.DownloadListPreview_Button.setObjectName('DownloadListPreview_Button')
        self.DownloadListPreview_Button.setText('Download List Preview')
        self.DownloadListPreview_Button.setFont(QtGui.QFont(App_Font,9))
        self.DownloadListPreview_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.DownloadListPreview_Button.setFixedSize(207,32)
        self.DownloadListPreview_Button.move(620,44)
        self.SteamCMD_Button=QtWidgets.QPushButton()
        self.SteamCMD_Button.setObjectName('SteamCMD_Button')
        self.SteamCMD_Button.setText('SteamCMD')
        self.SteamCMD_Button.setFont(QtGui.QFont(App_Font,9))
        self.SteamCMD_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.SteamCMD_Button.setFixedSize(65,32)
        self.SteamCMD_Button.move(11,44)
        self.Workshop_Button=QtWidgets.QPushButton()
        self.Workshop_Button.setObjectName('Workshop_Button')
        self.Workshop_Button.setText('Workshop links')
        self.Workshop_Button.setFont(QtGui.QFont(App_Font,9))
        self.Workshop_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.Workshop_Button.setFixedSize(292,32)
        self.Workshop_Button.move(322,44)
        self.Mode_Button=QtWidgets.QPushButton()
        self.Mode_Button.setObjectName('Mode_Button')
        self.Mode_Button.setText('Mode')
        self.Mode_Button.setFont(QtGui.QFont(App_Font,9))
        self.Mode_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.Mode_Button.setFixedSize(36,32)
        self.Mode_Button.move(322,196)
        self.OPENFOLDER_Button=QtWidgets.QPushButton()
        self.OPENFOLDER_Button.setObjectName('OPENFOLDER_Button')
        self.OPENFOLDER_Button.setText('OPEN FOLDER')
        self.OPENFOLDER_Button.setFont(QtGui.QFont(App_Font,9))
        self.OPENFOLDER_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.SAVELIST_Button=QtWidgets.QPushButton()
        self.SAVELIST_Button.setObjectName('SAVELIST_Button')
        self.SAVELIST_Button.setText('SAVE LIST')
        self.SAVELIST_Button.setFont(QtGui.QFont(App_Font,9))
        self.SAVELIST_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.SAVELIST_Button.setFixedSize(143,32)
        self.SAVELIST_Button.move(322,234)
        self.LOADLIST_Button=QtWidgets.QPushButton()
        self.LOADLIST_Button.setObjectName('LOADLIST_Button')
        self.LOADLIST_Button.setText('LOAD LIST')
        self.LOADLIST_Button.setFont(QtGui.QFont(App_Font,9))
        self.LOADLIST_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.LOADLIST_Button.setFixedSize(143,32)
        self.LOADLIST_Button.move(471,234)
        self.EXCEC_Button=QtWidgets.QPushButton()
        self.EXCEC_Button.setObjectName('EXCEC_Button')
        self.EXCEC_Button.setFont(QtGui.QFont(App_Font,9))
        self.EXCEC_Button.setFixedSize(601,32)
        self.EXCEC_Button.move(12,272)
        self.Folder_Button=QtWidgets.QPushButton()
        self.Folder_Button.setObjectName('Folder_Button')
        self.Folder_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.Folder_Button.setIconSize(QtCore.QSize(22, 22))
        self.Folder_Button.setFixedSize(40,32)
        self.Folder_Button.move(83,44)
        self.Config_Button=QtWidgets.QPushButton()
        self.Config_Button.setObjectName('Config_Button')
        self.Config_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.Config_Button.setIconSize(QtCore.QSize(22, 22))
        self.Config_Button.setFixedSize(40,32)
        self.Config_Button.move(12,310)
        self.Minimize_Button=QtWidgets.QPushButton()
        self.Minimize_Button.setObjectName('Minimize_Button')
        self.Minimize_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.Minimize_Button.setFixedSize(32,32)
        self.Minimize_Button.move(743,0)
        self.Close_Button=QtWidgets.QPushButton()
        self.Close_Button.setObjectName('Close_Button')
        self.Close_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.Close_Button.setFixedSize(32,32)
        self.Close_Button.move(807,0)
        self.User_Button=QtWidgets.QPushButton()
        self.User_Button.setObjectName('User_Button')
        self.User_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.User_Button.setFixedSize(22,22)
        self.User_Button.move(17,87)
        self.Password_Button=QtWidgets.QPushButton()
        self.Password_Button.setObjectName('Password_Button')
        self.Password_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.Password_Button.setFixedSize(22,22)
        self.Password_Button.move(17,125)
        self.Guard_Button=QtWidgets.QPushButton()
        self.Guard_Button.setObjectName('Guard_Button')
        self.Guard_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.Guard_Button.setFixedSize(22,22)
        self.Guard_Button.move(17,163)
        self.Info_Button=QtWidgets.QPushButton()
        self.Info_Button.setObjectName('Info_Button')
        self.Info_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.Info_Button.setFixedSize(16,16)
        self.SteamCMD_Line=CLineEdit()
        self.SteamCMD_Line.setObjectName('SteamCMD_Line')
        self.SteamCMD_Line.setFont(QtGui.QFont(App_Font,13))
        self.SteamCMD_Line.setCursor(QCursor(QtCore.Qt.IBeamCursor))
        self.SteamCMD_Line.setFixedSize(187,32)
        self.SteamCMD_Line.move(129,44)
        self.User_Line=CLineEdit()
        self.User_Line.setObjectName('User_Line')
        self.User_Line.setFont(QtGui.QFont(App_Font,13))
        self.User_Line.setPlaceholderText('Account name')
        self.User_Line.setCursor(QCursor(QtCore.Qt.IBeamCursor))
        self.User_Line.setFixedSize(266,32)
        self.User_Line.move(50,82)
        self.Password_Line=CLineEdit()
        self.Password_Line.setObjectName('Password_Line')
        self.Password_Line.setFont(QtGui.QFont(App_Font,13))
        self.Password_Line.setPlaceholderText('Password')
        self.Password_Line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Password_Line.setCursor(QCursor(QtCore.Qt.IBeamCursor))
        self.Password_Line.setFixedSize(266,32)
        self.Password_Line.move(50,120)
        self.Guard_Line=CLineEdit()
        self.Guard_Line.setObjectName('Guard_Line')
        self.Guard_Line.setFont(QtGui.QFont(App_Font,13))
        self.Guard_Line.setPlaceholderText('Steam Guard code')
        self.Guard_Line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Guard_Line.setCursor(QCursor(QtCore.Qt.IBeamCursor))
        self.Guard_Line.setFixedSize(266,32)
        self.Guard_Line.move(50,158)
        self.Workshop_Plain=CPlainTextEdit()
        self.Workshop_Plain.setObjectName('Workshop_Plain')
        self.Workshop_Plain.setFont(QtGui.QFont(App_Font,13))
        self.Workshop_Plain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Workshop_Plain.setCursor(QCursor(QtCore.Qt.ArrowCursor))
        self.Workshop_Plain.setFixedSize(292,108)
        self.Workshop_Plain.move(322,82)
        self.Info_Line=CInfoLine()
        self.Info_Line.setObjectName('Info_Line')
        self.Info_Line.setFont(QtGui.QFont(App_Font,13))
        self.Info_Line.setReadOnly(True)
        self.Info_Line.move(58,310)
        self.RANP_CheckBox=QCheckBox()
        self.RANP_CheckBox.setObjectName('RANP_CheckBox')
        self.RANP_CheckBox.setFont(QtGui.QFont(App_Font,9))
        self.RANP_CheckBox.setLayoutDirection(Qt.RightToLeft)
        self.RANP_CheckBox.setText('Remember my account name and password')
        self.RANP_CheckBox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.RANP_CheckBox.setFixedSize(305,32)
        self.RANP_CheckBox.move(11,196)
        self.Pin_CheckBox=QtWidgets.QCheckBox()
        self.Pin_CheckBox.setObjectName('Pin_CheckBox')
        self.Pin_CheckBox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.Pin_CheckBox.setFixedSize(32,32)
        self.Pin_CheckBox.move(775,0)
        self.Mode_ComboBox=QComboBox()
        self.Mode_ComboBox.setObjectName('Mode_ComboBox')
        self.Mode_ComboBox.setFont(QtGui.QFont(App_Font,9))
        self.Mode_ComboBox.setFixedSize(250,32)
        self.Mode_ComboBox.move(364,196)
        self.Mode_ComboBox.addItem('                   Single-game (Fastest)')
        self.Mode_ComboBox.addItem('              Multiple games & collections')
        self.Mode_ComboBox.addItem(' Generate SteamCMD Script (Single-game)')
        self.Mode_ComboBox.addItem('               Generate SteamCMD Script')
        self.Mode_ComboBox.addItem('                      Both (Single-game)')
        self.Mode_ComboBox.addItem('                                  Both')
        self.Mode_ComboBox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configA_RadioButton=QtWidgets.QRadioButton()
        self.configA_RadioButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configA_RadioButton.setFixedSize(16,16)
        self.configA_RadioButton.move(218,234)
        self.configpA_RadioButton=QtWidgets.QRadioButton()
        self.configpA_RadioButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configpA_RadioButton.setFixedSize(16,16)
        self.configpA_RadioButton.move(218,250)
        self.configD_RadioButton=QtWidgets.QRadioButton()
        self.configD_RadioButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configD_RadioButton.setFixedSize(16,16)
        self.configD_RadioButton.move(240,242)
        self.configR_RadioButton=QtWidgets.QRadioButton()
        self.configR_RadioButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configR_RadioButton.setFixedSize(16,16)
        self.configR_RadioButton.move(262,242)
        self.configGa_RadioButton=QtWidgets.QRadioButton()
        self.configGa_RadioButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configGa_RadioButton.setFixedSize(16,16)
        self.configGa_RadioButton.move(283,234)
        self.configGb_RadioButton=QtWidgets.QRadioButton()
        self.configGb_RadioButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configGb_RadioButton.setFixedSize(16,16)
        self.configGb_RadioButton.move(299,234)
        self.configpGa_RadioButton=QtWidgets.QRadioButton()
        self.configpGa_RadioButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configpGa_RadioButton.setFixedSize(16,16)
        self.configpGa_RadioButton.move(283,250)
        self.configpGb_RadioButton=QtWidgets.QRadioButton()
        self.configpGb_RadioButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configpGb_RadioButton.setFixedSize(16,16)
        self.configpGb_RadioButton.move(299,250)
        self.configB_RadioButton=QtWidgets.QRadioButton()
        self.configB_RadioButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configB_RadioButton.setChecked(True)
        self.configB_RadioButton.setFixedSize(16,16)
        self.configB_RadioButton.move(321,242)
        self.configI_RadioButton=QtWidgets.QRadioButton()
        self.configI_RadioButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configI_RadioButton.setFixedSize(16,16)
        self.configI_RadioButton.move(343,242)
        self.configT_RadioButton=QtWidgets.QRadioButton()
        self.configT_RadioButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configT_RadioButton.setFixedSize(16,16)
        self.configT_RadioButton.move(364,242)
        self.configW_RadioButton=QtWidgets.QRadioButton()
        self.configW_RadioButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configW_RadioButton.setFixedSize(16,16)
        self.configW_RadioButton.move(387,234)
        self.configpW_RadioButton=QtWidgets.QRadioButton()
        self.configpW_RadioButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configpW_RadioButton.setFixedSize(16,16)
        self.configpW_RadioButton.move(387,250)
        self.configBar_Frame=QtWidgets.QFrame()
        self.configBar_Frame.setObjectName('configBar_Frame')
        self.configBar_Frame.setFixedSize(160,322)
        self.configBar_Frame.move(462,32)
        self.configColorPalette_Label=QtWidgets.QLabel()
        self.configColorPalette_Label.setObjectName('configColorPalette_Label')
        self.configColorPalette_Label.setText('Color palette')
        self.configColorPalette_Label.setFont(QtGui.QFont(App_Font,9))
        self.configColorPalette_Label.setAlignment(Qt.AlignCenter)
        self.configColorPalette_Label.setFixedSize(438,32)
        self.configColorPalette_Label.move(12,196)
        self.configES_Button=QtWidgets.QPushButton()
        self.configES_Button.setObjectName('configES_Button')
        self.configES_Button.setText('ERRORS && SOLUTIONS')
        self.configES_Button.setFont(QtGui.QFont(App_Font,9))
        self.configES_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configES_Button.setFixedSize(160,32)
        self.configES_Button.move(462,32)
        self.configIH_Button=QtWidgets.QPushButton()
        self.configIH_Button.setObjectName('configIH_Button')
        self.configIH_Button.setText('INFORMATION && HELP')
        self.configIH_Button.setFont(QtGui.QFont(App_Font,9))
        self.configIH_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configIH_Button.setFixedSize(160,32)
        self.configIH_Button.move(462,64)
        self.configCR_Button=QtWidgets.QPushButton()
        self.configCR_Button.setObjectName('configCR_Button')
        self.configCR_Button.setText('CONTACT && REPORTS')
        self.configCR_Button.setFont(QtGui.QFont(App_Font,9))
        self.configCR_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configCR_Button.setFixedSize(160,32)
        self.configCR_Button.move(462,96)
        self.configOPTIONS_Button=QtWidgets.QPushButton()
        self.configOPTIONS_Button.setObjectName('configOPTIONS_Button')
        self.configOPTIONS_Button.setText('OPTIONS')
        self.configOPTIONS_Button.setFont(QtGui.QFont(App_Font,9))
        self.configOPTIONS_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configOPTIONS_Button.setFixedSize(160,32)
        self.configOPTIONS_Button.move(462,290-24)
        self.configUPDATES_Button=QtWidgets.QPushButton()
        self.configUPDATES_Button.setObjectName('configUPDATES_Button')
        self.configUPDATES_Button.setText('UPDATES')
        self.configUPDATES_Button.setFont(QtGui.QFont(App_Font,9))
        self.configUPDATES_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configUPDATES_Button.setFixedSize(160-24,32)
        self.configUPDATES_Button.move(462+12,322-12)
        self.configRGB_Button=QtWidgets.QPushButton()
        self.configRGB_Button.setObjectName('configRGB_Button')
        self.configRGB_Button.setText('RGB')
        self.configRGB_Button.setFont(QtGui.QFont(App_Font,9))
        self.configRGB_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configRGB_Button.setFixedSize(40,32)
        self.configRGB_Button.move(58,234)
        self.configCustom_Button=QtWidgets.QPushButton()
        self.configCustom_Button.setObjectName('configCustom_Button')
        self.configCustom_Button.setText('Custom')
        self.configCustom_Button.setFont(QtGui.QFont(App_Font,9))
        self.configCustom_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configCustom_Button.setFixedSize(142,32)
        self.configCustom_Button.move(12,272)
        self.configBright_Button=QtWidgets.QPushButton()
        self.configBright_Button.setObjectName('configBright_Button')
        self.configBright_Button.setText('Scarlet')
        self.configBright_Button.setFont(QtGui.QFont(App_Font,9))
        self.configBright_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configBright_Button.setFixedSize(142,32)
        self.configBright_Button.move(160,272)
        self.configDefault_Button=QtWidgets.QPushButton()
        self.configDefault_Button.setObjectName('configDefault_Button')
        self.configDefault_Button.setText('Default')
        self.configDefault_Button.setFont(QtGui.QFont(App_Font,9))
        self.configDefault_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configDefault_Button.setFixedSize(142,32)
        self.configDefault_Button.move(308,272)
        self.configSandE_Button=QtWidgets.QPushButton()
        self.configSandE_Button.setObjectName('configSandE_Button')
        self.configSandE_Button.setText('SAVE && EXIT')
        self.configSandE_Button.setFont(QtGui.QFont(App_Font,9))
        self.configSandE_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configSandE_Button.setFixedSize(438,32)
        self.configSandE_Button.move(12,311)
        self.configDefault0_Button=QtWidgets.QPushButton()
        self.configDefault0_Button.setObjectName('configDefault0_Button')
        self.configDefault0_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configDefault0_Button.setFixedSize(22,22)
        self.configDefault0_Button.move(424,48)
        self.configDefault1_Button=QtWidgets.QPushButton()
        self.configDefault1_Button.setObjectName('configDefault1_Button')
        self.configDefault1_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configDefault1_Button.setFixedSize(22,22)
        self.configDefault1_Button.move(424,126)
        self.configRepeat_Label=QtWidgets.QLabel()
        self.configRepeat_Label.setText('Repetitions')
        self.configRepeat_Label.setFont(QtGui.QFont(App_Font,9))
        self.configRepeat_Label.setFixedSize(64,32)
        self.configRepeat_Label.move(350,120)
        self.configRepeat_Line=CLineEdit()
        self.configRepeat_Line.setFont(QtGui.QFont(App_Font,9))
        self.configRepeat_Line.setAlignment(QtCore.Qt.AlignCenter)
        self.configRepeat_Line.setValidator(self.onlyInt)
        self.configRepeat_Line.setFixedSize(32,32)
        self.configRepeat_Line.move(312,120)
        self.configDefault2_Button=QtWidgets.QPushButton()
        self.configDefault2_Button.setObjectName('configDefault2_Button')
        self.configDefault2_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configDefault2_Button.setFixedSize(22,22)
        self.configDefault2_Button.move(424,163)
        self.configDefault3_Button=QtWidgets.QPushButton()
        self.configDefault3_Button.setObjectName('configDefault3_Button')
        self.configDefault3_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configDefault3_Button.setFixedSize(22,22)
        self.configDefault3_Button.move(424,200)
        self.configDownloadFolder_Line=CLineEdit()
        self.configDownloadFolder_Line.setObjectName('configDownloadFolder_Line')
        self.configDownloadFolder_Line.setFont(QtGui.QFont(App_Font,13))
        self.configDownloadFolder_Line.setPlaceholderText(" App's folder")
        self.configDownloadFolder_Line.setCursor(QCursor(QtCore.Qt.IBeamCursor))
        self.configDownloadFolder_Line.setFixedSize(215,32)
        self.configDownloadFolder_Line.move(12,44)
        self.configR_Line=CInfoLine()
        self.configR_Line.setObjectName('configR_Line')
        self.configR_Line.setFont(QtGui.QFont(App_Font,9))
        self.configR_Line.setCursor(QCursor(QtCore.Qt.IBeamCursor))
        self.configR_Line.setAlignment(QtCore.Qt.AlignCenter)
        self.configR_Line.setValidator(self.onlyInt)
        self.configR_Line.setMaxLength(3)
        self.configR_Line.setFixedSize(32,32)
        self.configR_Line.move(104,234)
        self.configG_Line=CInfoLine()
        self.configG_Line.setObjectName('configG_Line')
        self.configG_Line.setFont(QtGui.QFont(App_Font,9))
        self.configG_Line.setCursor(QCursor(QtCore.Qt.IBeamCursor))
        self.configG_Line.setAlignment(QtCore.Qt.AlignCenter)
        self.configG_Line.setValidator(self.onlyInt)
        self.configG_Line.setMaxLength(3)
        self.configG_Line.setFixedSize(32,32)
        self.configG_Line.move(142,234)
        self.configB_Line=CInfoLine()
        self.configB_Line.setObjectName('configB_Line')
        self.configB_Line.setFont(QtGui.QFont(App_Font,9))
        self.configB_Line.setCursor(QCursor(QtCore.Qt.IBeamCursor))
        self.configB_Line.setAlignment(QtCore.Qt.AlignCenter)
        self.configB_Line.setValidator(self.onlyInt)
        self.configB_Line.setMaxLength(3)
        self.configB_Line.setFixedSize(32,32)
        self.configB_Line.move(180,234)
        self.configInfo_Frame=QtWidgets.QFrame()
        self.configInfo_Frame.setObjectName('configInfo_Frame')
        self.configInfo_Frame.setFont(QtGui.QFont(App_Font,13))
        self.configInfo_Frame.setFixedSize(193,298)
        self.configInfo_Frame.move(634,44)
        self.configInfo_Line=CInfoPlainTextEdit()
        self.configInfo_Line.setObjectName('configInfo_Line')
        self.configInfo_Line.setFont(QtGui.QFont(App_Font,13))
        self.configInfo_Line.setReadOnly(True)
        self.configInfo_Line.setFixedSize(193,298)
        self.configInfo_Line.move(634,44)
        self.configCDF_CheckBox=HCCheckBox()
        self.configCDF_CheckBox.setObjectName('configCDF_CheckBox')
        self.configCDF_CheckBox.setFont(QtGui.QFont(App_Font,9))
        self.configCDF_CheckBox.setText('Change downloads folder')
        self.configCDF_CheckBox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configCDF_CheckBox.setFixedSize(180,32)
        self.configCDF_CheckBox.move(233,44)
        self.configBSCIM_CheckBox=HCCheckBox()
        self.configBSCIM_CheckBox.setObjectName('configBSCIM_CheckBox')
        self.configBSCIM_CheckBox.setFont(QtGui.QFont(App_Font,9))
        self.configBSCIM_CheckBox.setText('Big size items mode')
        self.configBSCIM_CheckBox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configBSCIM_CheckBox.setFixedSize(226,32)
        self.configBSCIM_CheckBox.move(12,120)
        self.configDLP_CheckBox=HCCheckBox()
        self.configDLP_CheckBox.setObjectName('configDLP_CheckBox')
        self.configDLP_CheckBox.setFont(QtGui.QFont(App_Font,9))
        self.configDLP_CheckBox.setText('Download list preview')
        self.configDLP_CheckBox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.configDLP_CheckBox.setFixedSize(166,32)
        self.configDLP_CheckBox.move(12,158)
        self.IHTab=CTabWindow()
        self.IHTab_SteamCMD=QtWidgets.QWidget()
        self.IHTab_Account=QtWidgets.QWidget()
        self.IHTab_Workshop=QtWidgets.QWidget()
        self.IHTab_Mode=QtWidgets.QWidget()
        self.IHTab_DLP=QtWidgets.QWidget()
        self.IHTab.addTab(self.IHTab_SteamCMD,'SteamCMD')
        self.IHTab.addTab(self.IHTab_Account,'Account')
        self.IHTab.addTab(self.IHTab_Workshop,'Workshop')
        self.IHTab.addTab(self.IHTab_Mode,'Mode')
        self.IHTab.addTab(self.IHTab_DLP,'Download List Preview')
        self.IHTab.setFont(QtGui.QFont(App_Font,9))
        self.IHTab.resize(438,254)
        self.IHTab.move(12,44)
        self.IHTab_SteamCMD.layout=QtWidgets.QVBoxLayout(self)
        self.IHTab_SteamCMD.layout.setContentsMargins(12,6,12,12)
        self.IHTab_SteamCMD.layout.setSpacing(6)
        self.IHTab_SteamCMD_Plain=QtWidgets.QPlainTextEdit()
        self.IHTab_SteamCMD_Plain.setPlainText("SteamCMD is a command line version of the Steam client, its main use is to install and update various dedicated servers available on Steam using a command line interface. Works with games that use the SteamPipe content system.\n\nFor SCMD Workshop Downloader to work, you will need to have SteamCMD installed on your computer and indicate its location via the first text box on the left. Remember that the first time you use it, it will download an update to work properly.\nSteamCMD is an official and completely safe tool.")
        self.IHTab_SteamCMD_Plain.setFont(QtGui.QFont(App_Font,9))
        self.IHTab_SteamCMD_Plain.setDisabled(True)
        self.IHTab_SteamCMD_Plain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.IHTab_SteamCMD.layout.addWidget(self.IHTab_SteamCMD_Plain)
        self.IHTab_SteamCMD_Plain.setFixedSize(414,170)
        self.IHTab_SteamCMD_Button=QtWidgets.QPushButton()
        self.IHTab_SteamCMD_Button.setText('DOWLOAD STEAMCMD')
        self.IHTab_SteamCMD_Button.setFont(QtGui.QFont(App_Font,9))
        self.IHTab_SteamCMD_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.IHTab_SteamCMD.layout.addWidget(self.IHTab_SteamCMD_Button)
        self.IHTab_SteamCMD_Button.setFixedSize(414,32)
        self.IHTab_SteamCMD.setLayout(self.IHTab_SteamCMD.layout)
        self.IHTab_Account.layout=QtWidgets.QVBoxLayout(self)
        self.IHTab_Account.layout.setContentsMargins(12,6,12,12)
        self.IHTab_Account.layout.setSpacing(6)
        self.IHTab_Account_Plain=QtWidgets.QPlainTextEdit()
        self.IHTab_Account_Plain.setPlainText("Due to the nature of SCMD Workshop Downloader you can use your account to download items without fear of retaliation since SteamCMD is an official and completely legal tool.\n\nThe personal data that you decide to save in this application is stored only and exclusively on your computer.\n\nIt is recommended to close Steam before logging in with your account in SteamCMD to avoid conflicts between both sessions and to start it correctly.\n\nKeep in mind that if you use Guard on your account, the first time you log in you will have to enter the access code it offers you.")
        self.IHTab_Account_Plain.setFont(QtGui.QFont(App_Font,9))
        self.IHTab_Account_Plain.setDisabled(True)
        self.IHTab_Account_Plain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.IHTab_Account.layout.addWidget(self.IHTab_Account_Plain)
        self.IHTab_Account_Plain.setFixedSize(414,204)
        self.IHTab_Account.setLayout(self.IHTab_Account.layout)
        self.IHTab_Workshop.layout=QtWidgets.QVBoxLayout(self)
        self.IHTab_Workshop.layout.setContentsMargins(12,6,12,12)
        self.IHTab_Workshop.layout.setSpacing(6)
        self.IHTab_Workshop_Plain=QtWidgets.QPlainTextEdit()
        self.IHTab_Workshop_Plain.setPlainText("Enter the links of the articles you want to download in the large text box in the middle of the window.\n\nRemember to separate each link by pressing enter or the space bar so that they are recognized correctly. The links you enter are pre-analyzed to check their operation and notify you of any problem.\n\nWhether or not an item can be downloaded without having purchased the game it belongs to depends on whether the game in question is listed, which Download List Preview will tell you and which you can also check.")
        self.IHTab_Workshop_Plain.setFont(QtGui.QFont(App_Font,9))
        self.IHTab_Workshop_Plain.setDisabled(True)
        self.IHTab_Workshop_Plain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.IHTab_Workshop.layout.addWidget(self.IHTab_Workshop_Plain)
        self.IHTab_Workshop_Plain.setFixedSize(414,170)
        self.IHTab_Workshop_Button=QtWidgets.QPushButton()
        self.IHTab_Workshop_Button.setText('CHECK LIST')
        self.IHTab_Workshop_Button.setFont(QtGui.QFont(App_Font,9))
        self.IHTab_Workshop_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.IHTab_Workshop.layout.addWidget(self.IHTab_Workshop_Button)
        self.IHTab_Workshop_Button.setFixedSize(414,32)
        self.IHTab_Workshop.setLayout(self.IHTab_Workshop.layout)
        self.IHTab_Mode.layout=QtWidgets.QVBoxLayout(self)
        self.IHTab_Mode.layout.setContentsMargins(12,6,12,12)
        self.IHTab_Mode.layout.setSpacing(6)
        self.IHTab_Mode_Plain=QtWidgets.QPlainTextEdit()
        self.IHTab_Mode_Plain.setPlainText("SCMD Workshop Downloader offers a download mode, a generator of Scripts (Generate), which is useful for updating servers easier, and both at the same time (Both).\nEach mode consists of two execution methods for different cases:\n\nSingle: This mode is designed to be fast, it only parses the first link to get the game it belongs to and unsets the rest of the links to wrap them in the final Script that SteamCMD will run to download the items.\n\nMultiple: This mode is able to find collections and their items, it can also download items from different games at the same time, since it analyzes each link individually to find the game they belong to and whether or not they are collections.")
        self.IHTab_Mode_Plain.setFont(QtGui.QFont(App_Font,9))
        self.IHTab_Mode_Plain.setDisabled(True)
        self.IHTab_Mode_Plain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.IHTab_Mode.layout.addWidget(self.IHTab_Mode_Plain)
        self.IHTab_Mode_Plain.setFixedSize(414,204)
        self.IHTab_Mode.setLayout(self.IHTab_Mode.layout)
        self.IHTab_DLP.layout=QtWidgets.QVBoxLayout(self)
        self.IHTab_DLP.layout.setContentsMargins(12,6,12,12)
        self.IHTab_DLP.layout.setSpacing(6)
        self.IHTab_DLP_Plain=QtWidgets.QPlainTextEdit()
        self.IHTab_DLP_Plain.setPlainText("This is a tool that allows you to preview the article that you enter in the corresponding text box.\nIt is able to tell you the name of the article, the game it belongs to, if it is listed or not, and an image of it. If a link is entered incorrectly or is invalid it will also let you know.\n\nAlthough it is a useful tool, it is also somewhat heavy and strange inside, so it may not work very well on less powerful computers or contain bugs that affect its display, although it is usually enough to change the displayed link to fix these problems. However, you can also disable it.")
        self.IHTab_DLP_Plain.setFont(QtGui.QFont(App_Font,9))
        self.IHTab_DLP_Plain.setDisabled(True)
        self.IHTab_DLP_Plain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.IHTab_DLP.layout.addWidget(self.IHTab_DLP_Plain)
        self.IHTab_DLP_Plain.setFixedSize(414,170)
        self.IHTab_DLP_Button=QtWidgets.QPushButton()
        self.IHTab_DLP_Button.setText('OPTIONS')
        self.IHTab_DLP_Button.setFont(QtGui.QFont(App_Font,9))
        self.IHTab_DLP_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.IHTab_DLP.layout.addWidget(self.IHTab_DLP_Button)
        self.IHTab_DLP_Button.setFixedSize(414,32)
        self.IHTab_DLP.setLayout(self.IHTab_DLP.layout)
        self.ESTab=CTabWindow()
        self.ESTab_SteamCMD=QtWidgets.QWidget()
        self.ESTab_SCMDLM=QtWidgets.QWidget()
        self.ESTab_SCMDWD=QtWidgets.QWidget()
        self.ESTab.addTab(self.ESTab_SCMDLM,'SCMD List Manager')
        self.ESTab.addTab(self.ESTab_SCMDWD,'SCMD Workshop Downloader')
        self.ESTab.addTab(self.ESTab_SteamCMD,' SteamCMD')
        self.ESTab.setFont(QtGui.QFont(App_Font,9))
        self.ESTab.resize(438,254)
        self.ESTab.move(12,44)
        self.ESTab_SteamCMD.layout=QtWidgets.QVBoxLayout(self)
        self.ESTab_SteamCMD.layout.setContentsMargins(12,6,12,12)
        self.ESTab_SteamCMD_Plain=QtWidgets.QPlainTextEdit()
        self.ESTab_SteamCMD_Plain.setPlainText("Unfortunately I have no power over the problems that SteamCMD may present, however I have tried to give some solutions to them, such as link duplication (BSIM).\n\nThe list is varied and it is easier to present it in detail in a PDF that you can access with the button below (which will also open the SteamCMD documentation page) or from the resources folder of SCMD Workshop Downloader.")
        self.ESTab_SteamCMD_Plain.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SteamCMD_Plain.setDisabled(True)
        self.ESTab_SteamCMD_Plain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ESTab_SteamCMD.layout.addWidget(self.ESTab_SteamCMD_Plain)
        self.ESTab_SteamCMD_Plain.setFixedSize(414,170)
        self.ESTab_SteamCMD_Button=QtWidgets.QPushButton()
        self.ESTab_SteamCMD_Button.setText('OPEN DOCUMENTATION')
        self.ESTab_SteamCMD_Button.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SteamCMD_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.ESTab_SteamCMD.layout.addWidget(self.ESTab_SteamCMD_Button)
        self.ESTab_SteamCMD_Button.setFixedSize(414,32)
        self.ESTab_SteamCMD.setLayout(self.ESTab_SteamCMD.layout)
        self.ESTab_SCMDLM.layout=QtWidgets.QVBoxLayout(self)
        self.ESTab_SCMDLM.layout.setContentsMargins(0,12,0,0)
        self.ESTab_SCMDLM_subtab=CTabWindow()
        self.ESTab_SCMDLM_subtab_TAB0=QtWidgets.QWidget()
        self.ESTab_SCMDLM_subtab_TAB1=QtWidgets.QWidget()
        self.ESTab_SCMDLM_subtab_TAB2=QtWidgets.QWidget()
        self.ESTab_SCMDLM_subtab_TAB3=QtWidgets.QWidget()
        self.ESTab_SCMDLM_subtab_TAB4=QtWidgets.QWidget()
        self.ESTab_SCMDLM_subtab.addTab(self.ESTab_SCMDLM_subtab_TAB0,'ERROR 0')
        self.ESTab_SCMDLM_subtab.addTab(self.ESTab_SCMDLM_subtab_TAB1,'ERROR 1')
        self.ESTab_SCMDLM_subtab.addTab(self.ESTab_SCMDLM_subtab_TAB2,'ERROR 2')
        self.ESTab_SCMDLM_subtab.addTab(self.ESTab_SCMDLM_subtab_TAB3,'ERROR 3')
        self.ESTab_SCMDLM_subtab.addTab(self.ESTab_SCMDLM_subtab_TAB4,'ERROR 4')
        self.ESTab_SCMDLM_subtab_TAB0.layout=QtWidgets.QVBoxLayout(self)
        self.ESTab_SCMDLM_subtab_TAB0.layout.setContentsMargins(12,12,12,12)
        self.ESTab_SCMDLM_subtab_TAB0.layout.setSpacing(6)
        self.ESTab_SCMDLM_subtab_TAB0_Plain=QtWidgets.QPlainTextEdit()
        self.ESTab_SCMDLM_subtab_TAB0_Plain.setPlainText('This error occurs because the code entered to download items through SteamCMD exceeds the 8191 characters allowed on the command line.\n\nThis usually occurs after over 300 items in download and can be fixed by dividing the number of links and submitting them for download separately or by disabling BSIM duplication in the options tab.\n\nIf any collection exceeds the number of items that can be uploaded , unfortunately it will not be able to be downloaded unless its articles are entered one by one.')
        self.ESTab_SCMDLM_subtab_TAB0_Plain.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SCMDLM_subtab_TAB0_Plain.setDisabled(True)
        self.ESTab_SCMDLM_subtab_TAB0_Plain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ESTab_SCMDLM_subtab_TAB0.layout.addWidget(self.ESTab_SCMDLM_subtab_TAB0_Plain)
        self.ESTab_SCMDLM_subtab_TAB0.setLayout(self.ESTab_SCMDLM_subtab_TAB0.layout)
        self.ESTab_SCMDLM_subtab_TAB1.layout=QtWidgets.QVBoxLayout(self)
        self.ESTab_SCMDLM_subtab_TAB1.layout.setContentsMargins(12,12,12,12)
        self.ESTab_SCMDLM_subtab_TAB1.layout.setSpacing(6)
        self.ESTab_SCMDLM_subtab_TAB1_Plain=QtWidgets.QPlainTextEdit()
        self.ESTab_SCMDLM_subtab_TAB1_Plain.setPlainText('Two things can be happening, the first and most likely is that, as the error indicates; the first link entered is wrong or not available, you can check if a link works or not through the Download List Preview. If this is not your case and the link you entered is correct, it may happen that your internet connection is unstable (because you are downloading something, for example) and SCMD List Manager has problems analyzing the link you entered.\n\nStarting the download again a few times or when your internet connection stabilizes is usually fixed.')
        self.ESTab_SCMDLM_subtab_TAB1_Plain.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SCMDLM_subtab_TAB1_Plain.setDisabled(True)
        self.ESTab_SCMDLM_subtab_TAB1_Plain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ESTab_SCMDLM_subtab_TAB1.layout.addWidget(self.ESTab_SCMDLM_subtab_TAB1_Plain)
        self.ESTab_SCMDLM_subtab_TAB1.setLayout(self.ESTab_SCMDLM_subtab_TAB1.layout)
        self.ESTab_SCMDLM_subtab_TAB2.layout=QtWidgets.QVBoxLayout(self)
        self.ESTab_SCMDLM_subtab_TAB2.layout.setContentsMargins(12,12,12,12)
        self.ESTab_SCMDLM_subtab_TAB2.layout.setSpacing(6)
        self.ESTab_SCMDLM_subtab_TAB2_Plain=QtWidgets.QPlainTextEdit()
        self.ESTab_SCMDLM_subtab_TAB2_Plain.setPlainText('Two things may be going on, first of all; The links entered may be wrong or have been entered incorrectly, this is most likely, although on the other hand; a bad internet connection in the middle of the analysis of the entered links can also affect and cause this problem.\n\nStarting the download again a few times or when your internet connection stabilizes is usually fixed.')
        self.ESTab_SCMDLM_subtab_TAB2_Plain.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SCMDLM_subtab_TAB2_Plain.setDisabled(True)
        self.ESTab_SCMDLM_subtab_TAB2_Plain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ESTab_SCMDLM_subtab_TAB2.layout.addWidget(self.ESTab_SCMDLM_subtab_TAB2_Plain)
        self.ESTab_SCMDLM_subtab_TAB2.setLayout(self.ESTab_SCMDLM_subtab_TAB2.layout)
        self.ESTab_SCMDLM_subtab_TAB3.layout=QtWidgets.QVBoxLayout(self)
        self.ESTab_SCMDLM_subtab_TAB3.layout.setContentsMargins(12,12,12,12)
        self.ESTab_SCMDLM_subtab_TAB3.layout.setSpacing(6)
        self.ESTab_SCMDLM_subtab_TAB3_Plain=QtWidgets.QPlainTextEdit()
        self.ESTab_SCMDLM_subtab_TAB3_Plain.setPlainText("This only happens if SCMD List Manager is started manually and without intervention from SCMD Workshop Downloader.\n\nThis error shouldn't happen for any other reason at all, but if it does, please report it.")
        self.ESTab_SCMDLM_subtab_TAB3_Plain.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SCMDLM_subtab_TAB3_Plain.setDisabled(True)
        self.ESTab_SCMDLM_subtab_TAB3_Plain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ESTab_SCMDLM_subtab_TAB3.layout.addWidget(self.ESTab_SCMDLM_subtab_TAB3_Plain)
        self.ESTab_SCMDLM_subtab_TAB3_Button=QtWidgets.QPushButton()
        self.ESTab_SCMDLM_subtab_TAB3_Button.setText('REPORT')
        self.ESTab_SCMDLM_subtab_TAB3_Button.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SCMDLM_subtab_TAB3_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.ESTab_SCMDLM_subtab_TAB3.layout.addWidget(self.ESTab_SCMDLM_subtab_TAB3_Button)
        self.ESTab_SCMDLM_subtab_TAB3_Button.setFixedSize(414,32)
        self.ESTab_SCMDLM_subtab_TAB3.setLayout(self.ESTab_SCMDLM_subtab_TAB3.layout)
        self.ESTab_SCMDLM_subtab_TAB4.layout=QtWidgets.QVBoxLayout(self)
        self.ESTab_SCMDLM_subtab_TAB4.layout.setContentsMargins(12,12,12,12)
        self.ESTab_SCMDLM_subtab_TAB4.layout.setSpacing(6)
        self.ESTab_SCMDLM_subtab_TAB4_Plain=QtWidgets.QPlainTextEdit()
        self.ESTab_SCMDLM_subtab_TAB4_Plain.setPlainText("This error can happen because SCMD List Manager was removed from the folder where SCMD Workshop Downloader is located or because the name of the folder where it is contained (or some folder that represents its location) contains special characters or letters specific to a language other than English.\n\nIt should be solved by having the aforementioned applications in their corresponding location, changing the name of the folders where they are located so that they meet the requirements mentioned above or moving the program folder to a Windows folder (such as Program Files)")
        self.ESTab_SCMDLM_subtab_TAB4_Plain.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SCMDLM_subtab_TAB4_Plain.setDisabled(True)
        self.ESTab_SCMDLM_subtab_TAB4_Plain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ESTab_SCMDLM_subtab_TAB4.layout.addWidget(self.ESTab_SCMDLM_subtab_TAB4_Plain)
        self.ESTab_SCMDLM_subtab_TAB4.setLayout(self.ESTab_SCMDLM_subtab_TAB4.layout)
        self.ESTab_SCMDLM_subtab.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SCMDLM_subtab.resize(438,210)
        self.ESTab_SCMDLM_subtab.move(12,44)
        self.ESTab_SCMDLM.layout.addWidget(self.ESTab_SCMDLM_subtab)
        self.ESTab_SCMDLM.setLayout(self.ESTab_SCMDLM.layout)
        self.ESTab_SCMDWD.layout=QtWidgets.QVBoxLayout(self)
        self.ESTab_SCMDWD.layout.setContentsMargins(0,12,0,0)
        self.ESTab_SCMDWD_subtab=CTabWindow()
        self.ESTab_SCMDWD_subtab_TAB0=QtWidgets.QWidget()
        self.ESTab_SCMDWD_subtab_TAB1=QtWidgets.QWidget()
        self.ESTab_SCMDWD_subtab_TAB2=QtWidgets.QWidget()
        self.ESTab_SCMDWD_subtab_TAB3=QtWidgets.QWidget()
        self.ESTab_SCMDWD_subtab_TAB4=QtWidgets.QWidget()
        self.ESTab_SCMDWD_subtab.addTab(self.ESTab_SCMDWD_subtab_TAB0,'ERROR 0')
        self.ESTab_SCMDWD_subtab.addTab(self.ESTab_SCMDWD_subtab_TAB1,'ERROR 1')
        self.ESTab_SCMDWD_subtab.addTab(self.ESTab_SCMDWD_subtab_TAB2,'ERROR 2')
        self.ESTab_SCMDWD_subtab.addTab(self.ESTab_SCMDWD_subtab_TAB3,'ERROR 3')
        self.ESTab_SCMDWD_subtab.addTab(self.ESTab_SCMDWD_subtab_TAB4,'ERROR 4')
        self.ESTab_SCMDWD_subtab_TAB0.layout=QtWidgets.QVBoxLayout(self)
        self.ESTab_SCMDWD_subtab_TAB0.layout.setContentsMargins(12,6,12,12)
        self.ESTab_SCMDWD_subtab_TAB0.layout.setSpacing(6)
        self.ESTab_SCMDWD_subtab_TAB0_Plain=QtWidgets.QPlainTextEdit()
        self.ESTab_SCMDWD_subtab_TAB0_Plain.setPlainText("This error is very rare. The most feasible solution is to re-download SCMD Workshop Downloader.\n\nIf the problem persists, try disabling your antivirus, if this doesn't help, please report it.")
        self.ESTab_SCMDWD_subtab_TAB0_Plain.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SCMDWD_subtab_TAB0_Plain.setDisabled(True)
        self.ESTab_SCMDWD_subtab_TAB0_Plain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ESTab_SCMDWD_subtab_TAB0.layout.addWidget(self.ESTab_SCMDWD_subtab_TAB0_Plain)
        self.ESTab_SCMDWD_subtab_TAB0_Button=QtWidgets.QPushButton()
        self.ESTab_SCMDWD_subtab_TAB0_Button.setText('REPORT')
        self.ESTab_SCMDWD_subtab_TAB0_Button.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SCMDWD_subtab_TAB0_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.ESTab_SCMDWD_subtab_TAB0.layout.addWidget(self.ESTab_SCMDWD_subtab_TAB0_Button)
        self.ESTab_SCMDWD_subtab_TAB0_Button.setFixedSize(414,32)
        self.ESTab_SCMDWD_subtab_TAB0.setLayout(self.ESTab_SCMDWD_subtab_TAB0.layout)
        self.ESTab_SCMDWD_subtab_TAB1.layout=QtWidgets.QVBoxLayout(self)
        self.ESTab_SCMDWD_subtab_TAB1.layout.setContentsMargins(12,6,12,12)
        self.ESTab_SCMDWD_subtab_TAB1.layout.setSpacing(6)
        self.ESTab_SCMDWD_subtab_TAB1_Plain=QtWidgets.QPlainTextEdit()
        self.ESTab_SCMDWD_subtab_TAB1_Plain.setPlainText('The folder (or one of the folders) where SCMD Workshop Downloader or SteamCMD is located may have been changed, be on different disks, contains symbols or special characters or letters specific to a language other than English. It may also be that SCMD List Manager has been removed or moved.\n\nTo fix this, change the location of the above programs to match the disk they are located on, or rename the folders that contain them in order to meet the aforementioned conditions.')
        self.ESTab_SCMDWD_subtab_TAB1_Plain.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SCMDWD_subtab_TAB1_Plain.setDisabled(True)
        self.ESTab_SCMDWD_subtab_TAB1_Plain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ESTab_SCMDWD_subtab_TAB1.layout.addWidget(self.ESTab_SCMDWD_subtab_TAB1_Plain)
        self.ESTab_SCMDWD_subtab_TAB1.setLayout(self.ESTab_SCMDWD_subtab_TAB1.layout)
        self.ESTab_SCMDWD_subtab_TAB2.layout=QtWidgets.QVBoxLayout(self)
        self.ESTab_SCMDWD_subtab_TAB2.layout.setContentsMargins(12,6,12,12)
        self.ESTab_SCMDWD_subtab_TAB2.layout.setSpacing(6)
        self.ESTab_SCMDWD_subtab_TAB2_Plain=QtWidgets.QPlainTextEdit()
        self.ESTab_SCMDWD_subtab_TAB2_Plain.setPlainText('This happens if during the execution of SCMD Workshop Downloader the mentioned folders were modified in some way, check that it has not been caused by an external program or your antivirus. Usually this error should not happen unless you manually modify those folders.\n\nIn any case, re-enter the respective locations in the program and retry the operation that showed you the error, if the problem persists, report it.')
        self.ESTab_SCMDWD_subtab_TAB2_Plain.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SCMDWD_subtab_TAB2_Plain.setDisabled(True)
        self.ESTab_SCMDWD_subtab_TAB2_Plain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ESTab_SCMDWD_subtab_TAB2.layout.addWidget(self.ESTab_SCMDWD_subtab_TAB2_Plain)
        self.ESTab_SCMDWD_subtab_TAB2_Button=QtWidgets.QPushButton()
        self.ESTab_SCMDWD_subtab_TAB2_Button.setText('REPORT')
        self.ESTab_SCMDWD_subtab_TAB2_Button.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SCMDWD_subtab_TAB2_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.ESTab_SCMDWD_subtab_TAB2.layout.addWidget(self.ESTab_SCMDWD_subtab_TAB2_Button)
        self.ESTab_SCMDWD_subtab_TAB2_Button.setFixedSize(414,32)
        self.ESTab_SCMDWD_subtab_TAB2.setLayout(self.ESTab_SCMDWD_subtab_TAB2.layout)
        self.ESTab_SCMDWD_subtab_TAB3.layout=QtWidgets.QVBoxLayout(self)
        self.ESTab_SCMDWD_subtab_TAB3.layout.setContentsMargins(12,6,12,12)
        self.ESTab_SCMDWD_subtab_TAB3.layout.setSpacing(6)
        self.ESTab_SCMDWD_subtab_TAB3_Plain=QtWidgets.QPlainTextEdit()
        self.ESTab_SCMDWD_subtab_TAB3_Plain.setPlainText('Probably the link you entered does not belong to any Steam Workshop item or is wrong (Maybe you pressed enter or space bar before entering the link by accident!).\n\nCheck the link, move it and correct it if it is wrong, that will be enough to make it work.')
        self.ESTab_SCMDWD_subtab_TAB3_Plain.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SCMDWD_subtab_TAB3_Plain.setDisabled(True)
        self.ESTab_SCMDWD_subtab_TAB3_Plain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ESTab_SCMDWD_subtab_TAB3.layout.addWidget(self.ESTab_SCMDWD_subtab_TAB3_Plain)
        self.ESTab_SCMDWD_subtab_TAB3.setLayout(self.ESTab_SCMDWD_subtab_TAB3.layout)
        self.ESTab_SCMDWD_subtab_TAB4.layout=QtWidgets.QVBoxLayout(self)
        self.ESTab_SCMDWD_subtab_TAB4.layout.setContentsMargins(12,6,12,12)
        self.ESTab_SCMDWD_subtab_TAB4.layout.setSpacing(6)
        self.ESTab_SCMDWD_subtab_TAB4_Plain=QtWidgets.QPlainTextEdit()
        self.ESTab_SCMDWD_subtab_TAB4_Plain.setPlainText("This is rather a warning: If Download List Preview detects that a link entered belongs to a game that is not registered in the list of games that allow downloads without purchasing the game, this message will appear indicating that when trying to download, probably it will not work. Whether a game is listed and its items can be downloaded by this method (Legally) is entirely up to the creators of the game.\nThis can also happen that the list of the program is out of date (Update the SCMD Workshop Downloader!)")
        self.ESTab_SCMDWD_subtab_TAB4_Plain.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SCMDWD_subtab_TAB4_Plain.setDisabled(True)
        self.ESTab_SCMDWD_subtab_TAB4_Plain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ESTab_SCMDWD_subtab_TAB4.layout.addWidget(self.ESTab_SCMDWD_subtab_TAB4_Plain)
        self.ESTab_SCMDWD_subtab_TAB4_Button=QtWidgets.QPushButton()
        self.ESTab_SCMDWD_subtab_TAB4_Button.setText('CHECK LIST')
        self.ESTab_SCMDWD_subtab_TAB4_Button.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SCMDWD_subtab_TAB4_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.ESTab_SCMDWD_subtab_TAB4.layout.addWidget(self.ESTab_SCMDWD_subtab_TAB4_Button)
        self.ESTab_SCMDWD_subtab_TAB4_Button.setFixedSize(414,32)
        self.ESTab_SCMDWD_subtab_TAB4.setLayout(self.ESTab_SCMDWD_subtab_TAB4.layout)
        self.ESTab_SCMDWD_subtab.setFont(QtGui.QFont(App_Font,9))
        self.ESTab_SCMDWD_subtab.resize(438,210)
        self.ESTab_SCMDWD_subtab.move(12,44)
        self.ESTab_SCMDWD.layout.addWidget(self.ESTab_SCMDWD_subtab)
        self.ESTab_SCMDWD.setLayout(self.ESTab_SCMDWD.layout)
        self.CRPixmap = QtGui.QPixmap()
        self.CRPixmap.load('./resources/scmd.png')
        self.CRPixmap = self.CRPixmap.scaled(150,150)
        self.CRLabel=QtWidgets.QLabel()
        self.CRLabel.setPixmap(self.CRPixmap)
        self.CRLabel.setFixedSize(150,150)
        self.CRLabel.move(240,99)
        self.CRButton0=QtWidgets.QPushButton()
        self.CRButton0.setText("Application Discord")
        self.CRButton0.setFont(QtGui.QFont(App_Font,9))
        self.CRButton0.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.CRButton0.setIcon(QIcon('./resources/discord.png'))
        self.CRButton0.setIconSize(QtCore.QSize(42, 42))
        self.CRButton0.setFixedSize(151,42)
        self.CRButton0.move(72,115)
        self.CRButton1=QtWidgets.QPushButton()
        self.CRButton1.setText("GitHub Project")
        self.CRButton1.setFont(QtGui.QFont(App_Font,9))
        self.CRButton1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.CRButton1.setIcon(QIcon('./resources/github.png'))
        self.CRButton1.setIconSize(QtCore.QSize(42, 42))
        self.CRButton1.setFixedSize(123,42)
        self.CRButton1.move(72,152)
        self.CRButton2=QtWidgets.QPushButton()
        self.CRButton2.setText("Youtube Channel")
        self.CRButton2.setFont(QtGui.QFont(App_Font,9))
        self.CRButton2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.CRButton2.setIcon(QIcon('./resources/youtube.png'))
        self.CRButton2.setIconSize(QtCore.QSize(42, 42))
        self.CRButton2.setFixedSize(136,42)
        self.CRButton2.move(72,190)
        self.dFrame=QtWidgets.QFrame()
        self.dFrame.setFixedSize(193,194)
        self.dFrame.move(627,77)
        self.dPixmap = QtGui.QPixmap()
        self.dPixmap.load('./resources/berdyalexei.png')
        self.dPixmap = self.dPixmap.scaled(193,134)
        self.dLabel=QtWidgets.QLabel()
        self.dLabel.setPixmap(self.dPixmap)
        self.dLabel.setFixedSize(193,134)
        self.dLabel.move(627,77)
        self.dTextName=QtWidgets.QLabel()
        self.dTextName.setFixedSize(193,16)
        self.dTextName.move(627,217)
        self.dTextName.setFont(QtGui.QFont(App_Font,9))
        self.dTextName.setText('')
        self.dTextName.setAlignment(QtCore.Qt.AlignCenter) 
        self.dTextGame=QtWidgets.QLabel()
        self.dTextGame.setFixedSize(193,16)
        self.dTextGame.move(627,233)
        self.dTextGame.setFont(QtGui.QFont(App_Font,9))
        self.dTextGame.setText('Made by Berdy Alexei')
        self.dTextGame.setAlignment(QtCore.Qt.AlignCenter) 
        self.dTextListed=QtWidgets.QLabel()
        self.dTextListed.setFixedSize(193,16)
        self.dTextListed.move(627,249)
        self.dTextListed.setFont(QtGui.QFont(App_Font,9))
        self.dTextListed.setText('')
        self.dTextListed.setAlignment(QtCore.Qt.AlignCenter) 
        self.dIncrease=QtWidgets.QPushButton()
        self.dIncrease.setFixedSize(16,16)
        self.dIncrease.move(799,285)
        self.dDecrease=QtWidgets.QPushButton()
        self.dDecrease.setFixedSize(16,16)
        self.dDecrease.move(633,285)
        if self.data['steamcmd']!='':
            self.SteamCMD_Line.setText(self.data['steamcmd'])
        if self.data['dfolder']!='':
            self.configDownloadFolder_Line.setText(self.data['dfolder'])
        if self.data['ranp']==True:
            self.RANP_CheckBox.setChecked(True)
            if self.data['account']!='' and self.data['password']!='':
                self.User_Line.setText(self.data['account'])
                self.Password_Line.setText(self.data['password'])
        if self.data['bscim']==True:
            self.configBSCIM_CheckBox.setChecked(True)
        if self.data['cdf']==True:
            self.configCDF_CheckBox.setChecked(True)
        self.Mode_ComboBox.setCurrentIndex(self.data['mode'])
        if self.data["dlp"]==True:
            self.configDLP_CheckBox.setChecked(True)
        if self.data['repeat']!='':
            self.configRepeat_Line.setText(str(self.data['repeat']))
        self.Config_Button.clicked.connect(lambda:self.EnableButtons())
        self.Config_Button.clicked.connect(lambda:self.Config())
        self.configOPTIONS_Button.clicked.connect(lambda:self.EnableButtons())
        self.configOPTIONS_Button.clicked.connect(lambda:self.Config())
        self.configIH_Button.clicked.connect(lambda:self.EnableButtons())
        self.configIH_Button.clicked.connect(lambda:self.IH())
        self.configIH_Button.clicked.connect(lambda:self.IHTab.setCurrentIndex(0))
        self.configES_Button.clicked.connect(lambda:self.EnableButtons())
        self.configES_Button.clicked.connect(lambda:self.ES())
        self.configES_Button.clicked.connect(lambda:self.ESTab.setCurrentIndex(0))
        self.configES_Button.clicked.connect(lambda:self.ESTab_SCMDWD_subtab.setCurrentIndex(0))
        self.configES_Button.clicked.connect(lambda:self.ESTab_SCMDLM_subtab.setCurrentIndex(0))
        self.configCR_Button.clicked.connect(lambda:self.EnableButtons())
        self.configCR_Button.clicked.connect(lambda:self.CR())
        self.ESTab_SCMDLM_subtab_TAB3_Button.clicked.connect(lambda:self.EnableButtons())
        self.ESTab_SCMDLM_subtab_TAB3_Button.clicked.connect(lambda:self.CR())
        self.ESTab_SCMDWD_subtab_TAB0_Button.clicked.connect(lambda:self.EnableButtons())
        self.ESTab_SCMDWD_subtab_TAB0_Button.clicked.connect(lambda:self.CR())
        self.ESTab_SCMDWD_subtab_TAB2_Button.clicked.connect(lambda:self.EnableButtons())
        self.ESTab_SCMDWD_subtab_TAB2_Button.clicked.connect(lambda:self.CR())
        self.configUPDATES_Button.clicked.connect(lambda:webbrowser.open('https://github.com/BerdyAlexei/SCMD-Workshop-Downloader-2/releases'))
        self.SteamCMD_Button.clicked.connect(lambda:self.EnableButtons())
        self.SteamCMD_Button.clicked.connect(lambda:self.IH())
        self.SteamCMD_Button.clicked.connect(lambda:self.IHTab.setCurrentIndex(0))
        self.User_Button.clicked.connect(lambda:self.EnableButtons())
        self.User_Button.clicked.connect(lambda:self.IH())
        self.User_Button.clicked.connect(lambda:self.IHTab.setCurrentIndex(1))
        self.Password_Button.clicked.connect(lambda:self.EnableButtons())
        self.Password_Button.clicked.connect(lambda:self.IH())
        self.Password_Button.clicked.connect(lambda:self.IHTab.setCurrentIndex(1))
        self.Guard_Button.clicked.connect(lambda:self.EnableButtons())
        self.Guard_Button.clicked.connect(lambda:self.IH())
        self.Guard_Button.clicked.connect(lambda:self.IHTab.setCurrentIndex(1))
        self.Workshop_Button.clicked.connect(lambda:self.EnableButtons())
        self.Workshop_Button.clicked.connect(lambda:self.IH())
        self.Workshop_Button.clicked.connect(lambda:self.IHTab.setCurrentIndex(2))
        self.Mode_Button.clicked.connect(lambda:self.EnableButtons())
        self.Mode_Button.clicked.connect(lambda:self.IH())
        self.Mode_Button.clicked.connect(lambda:self.IHTab.setCurrentIndex(3))
        self.DownloadListPreview_Button.clicked.connect(lambda:self.EnableButtons())
        self.DownloadListPreview_Button.clicked.connect(lambda:self.IH())
        self.DownloadListPreview_Button.clicked.connect(lambda:self.IHTab.setCurrentIndex(4))
        self.Minimize_Button.clicked.connect(lambda:self.showMinimized())
        self.Folder_Button.clicked.connect(lambda:self.SteamCMD())
        self.LOADLIST_Button.clicked.connect(lambda:self.LoadList())
        self.Close_Button.clicked.connect(lambda:self.RANP())
        self.Close_Button.clicked.connect(lambda:self.Close())
        self.Pin_CheckBox.clicked.connect(lambda:self.Pin())
        self.RANP_CheckBox.clicked.connect(lambda:self.RANP())
        self.configCDF_CheckBox.clicked.connect(lambda:self.Default0_Activator())
        self.configCDF_CheckBox.clicked.connect(lambda:self.SaveData())
        self.configCDF_CheckBox.clicked.connect(lambda:self.OPENFOLDER_Activator())
        self.configBSCIM_CheckBox.clicked.connect(lambda:self.Default1_Activator())
        self.configBSCIM_CheckBox.clicked.connect(lambda:self.SaveData())
        self.SteamCMD_Line.textChanged.connect(self.EXCEC_Activator)
        self.SteamCMD_Line.textChanged.connect(self.OPENFOLDER_Activator)
        self.SteamCMD_Line.textChanged.connect(self.InfoReset)
        self.configDownloadFolder_Line.textChanged.connect(self.SaveData)
        self.configDownloadFolder_Line.textChanged.connect(self.OPENFOLDER_Activator)
        self.User_Line.textChanged.connect(self.RANP)
        self.Password_Line.textChanged.connect(self.RANP)
        self.Workshop_Plain.textChanged.connect(self.EXCEC_Activator)
        self.Workshop_Plain.textChanged.connect(self.SAVELIST_Activator)
        self.Workshop_Plain.textChanged.connect(self.InfoReset)
        self.Workshop_Plain.textChanged.connect(self.getData_workshop)
        self.Mode_ComboBox.activated[str].connect(self.EXCEC_Activator)
        self.Mode_ComboBox.currentIndexChanged.connect(self.InfoReset)
        self.Mode_ComboBox.currentIndexChanged.connect(self.SaveData)
        self.Mode_ComboBox.currentIndexChanged.connect(self.OPENFOLDER_Activator)
        self.configRepeat_Line.textChanged.connect(self.RepeatFix)
        self.configRepeat_Line.mousePressEvent=lambda _ : self.configRepeat_Line.selectAll()
        self.dIncrease.clicked.connect(lambda:self.Increase())
        self.dDecrease.clicked.connect(lambda:self.Decrease())
        self.configDefault0_Button.clicked.connect(lambda:self.Default0())
        self.configDefault1_Button.clicked.connect(lambda:self.Default1())
        self.configDefault2_Button.clicked.connect(lambda:self.Default2())
        self.configDefault3_Button.clicked.connect(lambda:self.Default3())
        self.configDefault_Button.clicked.connect(lambda:datatozero())
        def datatozero():
            self.data["palette"]=0
            self.PaletteUpdater()
            self.RGB()
        self.configBright_Button.clicked.connect(lambda:datatoone())
        def datatoone():
            self.data["palette"]=1
            self.PaletteUpdater()
            self.RGB()
        self.configCustom_Button.clicked.connect(lambda:datatotwo())
        def datatotwo():
            self.data["palette"]=2
            self.PaletteUpdater()
            self.RGB()
        self.configRGB_Button.clicked.connect(lambda:self.RGBPicker())
        self.configA_RadioButton.clicked.connect(lambda:self.RGB())
        self.configpA_RadioButton.clicked.connect(lambda:self.RGB())
        self.configD_RadioButton.clicked.connect(lambda:self.RGB())
        self.configR_RadioButton.clicked.connect(lambda:self.RGB())
        self.configGa_RadioButton.clicked.connect(lambda:self.RGB())
        self.configGb_RadioButton.clicked.connect(lambda:self.RGB())
        self.configpGa_RadioButton.clicked.connect(lambda:self.RGB())
        self.configpGb_RadioButton.clicked.connect(lambda:self.RGB())
        self.configB_RadioButton.clicked.connect(lambda:self.RGB())
        self.configI_RadioButton.clicked.connect(lambda:self.RGB())
        self.configT_RadioButton.clicked.connect(lambda:self.RGB())
        self.configW_RadioButton.clicked.connect(lambda:self.RGB())
        self.configpW_RadioButton.clicked.connect(lambda:self.RGB())
        self.IHTab_SteamCMD_Button.clicked.connect(lambda:webbrowser.open('https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip'))
        self.IHTab_Workshop_Button.clicked.connect(lambda:webbrowser.open('https://steamdb.info/sub/17906/apps/'))
        self.ESTab_SCMDWD_subtab_TAB4_Button.clicked.connect(lambda:webbrowser.open('https://steamdb.info/sub/17906/apps/'))
        self.ESTab_SteamCMD_Button.clicked.connect(lambda:os.startfile(os.path.realpath('./resources/steamcmd.pdf')))
        self.ESTab_SteamCMD_Button.clicked.connect(lambda:webbrowser.open('https://developer.valvesoftware.com/wiki/SteamCMD'))
        self.CRButton0.clicked.connect(lambda:webbrowser.open('https://discord.com/invite/KZC6e8ZuyF'))
        self.CRButton1.clicked.connect(lambda:webbrowser.open('https://github.com/BerdyAlexei/SCMD-Workshop-Downloader-2'))
        self.CRButton2.clicked.connect(lambda:webbrowser.open('https://www.youtube.com/channel/UCRsJnpxXtoNxTPL00tgfgJw'))
        self.IHTab_DLP_Button.clicked.connect(lambda:self.EnableButtons())
        self.IHTab_DLP_Button.clicked.connect(lambda:self.Config())
        self.configSandE_Button.clicked.connect(lambda:self.HideIH())
        self.configSandE_Button.clicked.connect(lambda:self.HideES())
        self.configSandE_Button.clicked.connect(lambda:self.HideCR())
        self.configSandE_Button.clicked.connect(lambda:self.HideConfig())
        self.configSandE_Button.clicked.connect(lambda:self.Show())
        self.configCDF_CheckBox.entered.connect(lambda:self.configInfo_Line.setPlainText("It allows you to add a new folder where the downloads you make will be saved from now on. This option will add the "+'"force_install_dir"'+" command to the download script wich will cause SteamCMD to download the items to the site you've specified."))
        self.configBSCIM_CheckBox.entered.connect(lambda:self.configInfo_Line.setPlainText('This option activates BSIM link writing duplication, this could solve some "Time Out" type problems in downloading articles larger than 1 gigabyte, however it will also cause smaller articles to be downloaded again, although without taking up additional disk space, since they will replace each other.'))
        self.configDLP_CheckBox.entered.connect(lambda:self.configInfo_Line.setPlainText('You can choose whether to disable the Download List Preview Window on the main screen of SCMD Workshop Downloader, it can be useful if your computer is not very powerful.'))
        self.dLink=CLineEdit()
        self.dLink.setFixedSize(128,32)
        self.dLink.move(660,277)
        self.dLink.setValidator(QIntValidator(0, 999999, self))
        self.dLink.setAlignment(QtCore.Qt.AlignCenter) 
        self.dLink.setFont(QtGui.QFont(App_Font,9))
        self.dLink.setText('0')
        self.dLink.textChanged.connect(self.getData_link)
        self.dLink.textChanged.connect(self.IDManager)
        self.dLink.mousePressEvent=lambda _ : self.dLink.selectAll()
        self.sSS()
        self.Pin()
        self.InfoReset()
        self.ScriptCleaner()
        self.EXCEC_Name()
        self.RGB()
        self.HideES()
        self.HideCR()
        self.HideIH()
        self.HideConfig()
        self.DLP()
        self.DownloadListPreview()
        self.RepeatFix()
        if self.data['dlp']==True:
            self.configDLP_CheckBox.setChecked(True)
            self.DownloadListPreview()
            self.IDManager()
        else:
            self.deactivateDownloadListPreview()
        self.configDLP_CheckBox.clicked.connect(lambda:self.Default2_Activator())
        self.configDLP_CheckBox.clicked.connect(lambda:self.SaveData())
        self.configDLP_CheckBox.clicked.connect(lambda:self.DLP())
        self.layout().addWidget(self.Info_Frame)
        self.layout().addWidget(self.TitleBar_Frame)
        self.layout().addWidget(self.SCMDWD_Label)
        self.layout().addWidget(self.SteamCMD_Button)
        self.layout().addWidget(self.Workshop_Button)
        self.layout().addWidget(self.Mode_Button)
        self.layout().addWidget(self.OPENFOLDER_Button)
        self.layout().addWidget(self.SAVELIST_Button)
        self.layout().addWidget(self.LOADLIST_Button)
        self.layout().addWidget(self.EXCEC_Button)
        self.layout().addWidget(self.Folder_Button)
        self.layout().addWidget(self.Config_Button)
        self.layout().addWidget(self.Minimize_Button)
        self.layout().addWidget(self.Close_Button)
        self.layout().addWidget(self.User_Button)
        self.layout().addWidget(self.Password_Button)
        self.layout().addWidget(self.Guard_Button)
        self.layout().addWidget(self.SteamCMD_Line)
        self.layout().addWidget(self.User_Line)
        self.layout().addWidget(self.Password_Line)
        self.layout().addWidget(self.Guard_Line)
        self.layout().addWidget(self.Workshop_Plain)
        self.layout().addWidget(self.Info_Line)
        self.layout().addWidget(self.Info_Button)
        self.layout().addWidget(self.RANP_CheckBox)
        self.layout().addWidget(self.Pin_CheckBox)
        self.layout().addWidget(self.Mode_ComboBox)
        self.layout().addWidget(self.DownloadInfo_Label)
        self.layout().addWidget(self.DownloadListPreview_Frame)
        self.layout().addWidget(self.DownloadListPreview_Button)
        self.layout().addWidget(self.configA_RadioButton)
        self.layout().addWidget(self.configpA_RadioButton)
        self.layout().addWidget(self.configD_RadioButton)
        self.layout().addWidget(self.configR_RadioButton)
        self.layout().addWidget(self.configGa_RadioButton)
        self.layout().addWidget(self.configGb_RadioButton)
        self.layout().addWidget(self.configpGa_RadioButton)
        self.layout().addWidget(self.configpGb_RadioButton)
        self.layout().addWidget(self.configB_RadioButton)
        self.layout().addWidget(self.configI_RadioButton)
        self.layout().addWidget(self.configT_RadioButton)
        self.layout().addWidget(self.configW_RadioButton)
        self.layout().addWidget(self.configpW_RadioButton)
        self.layout().addWidget(self.configBar_Frame)
        self.layout().addWidget(self.configIH_Button)
        self.layout().addWidget(self.configES_Button)
        self.layout().addWidget(self.configCR_Button)
        self.layout().addWidget(self.configOPTIONS_Button)
        self.layout().addWidget(self.configUPDATES_Button)
        self.layout().addWidget(self.configRGB_Button)
        self.layout().addWidget(self.configCustom_Button)
        self.layout().addWidget(self.configDefault_Button)
        self.layout().addWidget(self.configBright_Button)
        self.layout().addWidget(self.configSandE_Button)
        self.layout().addWidget(self.configInfo_Frame)
        self.layout().addWidget(self.configInfo_Line)
        self.layout().addWidget(self.configR_Line)
        self.layout().addWidget(self.configG_Line)
        self.layout().addWidget(self.configB_Line)
        self.layout().addWidget(self.configRepeat_Line)
        self.layout().addWidget(self.configRepeat_Label)
        self.layout().addWidget(self.configColorPalette_Label)
        self.layout().addWidget(self.configCDF_CheckBox)
        self.layout().addWidget(self.configBSCIM_CheckBox)
        self.layout().addWidget(self.configDLP_CheckBox)
        self.layout().addWidget(self.configDownloadFolder_Line)
        self.layout().addWidget(self.configDefault0_Button)
        self.layout().addWidget(self.configDefault1_Button)
        self.layout().addWidget(self.configDefault2_Button)
        self.layout().addWidget(self.configDefault3_Button)
        self.layout().addWidget(self.IHTab)
        self.layout().addWidget(self.ESTab)
        self.layout().addWidget(self.CRLabel)
        self.layout().addWidget(self.CRButton0)
        self.layout().addWidget(self.CRButton1)
        self.layout().addWidget(self.CRButton2)
        self.layout().addWidget(self.dFrame)
        self.layout().addWidget(self.dTextName)
        self.layout().addWidget(self.dTextGame)
        self.layout().addWidget(self.dTextListed)
        self.layout().addWidget(self.dLabel)
        self.layout().addWidget(self.dIncrease)
        self.layout().addWidget(self.dDecrease)
        self.layout().addWidget(self.notallowed0)
        self.notallowed0.hide()
        self.layout().addWidget(self.notallowed1)
        self.notallowed1.hide()
        self.layout().addWidget(self.notallowed2)
        self.notallowed2.hide()
        self.layout().addWidget(self.dLink)
    def sSS(self):
        if self.data["palette"]==2:
            self.a=self.data["ca"]
            self.d=self.data["cd"]
            self.r=self.data["cr"]
            self.g=self.data["cg"]
            self.b=self.data["cb"]
            self.i=self.data["ci"]
            self.t=self.data["ct"]
            self.w=self.data["cw"]
        elif self.data["palette"]==1:
            self.a=self.data["ba"]
            self.d=self.data["bd"]
            self.r=self.data["br"]
            self.g=self.data["bg"]
            self.b=self.data["bb"]
            self.i=self.data["bi"]
            self.t=self.data["bt"]
            self.w=self.data["bw"]
        else:
            self.a=self.data["a"]
            self.d=self.data["d"]
            self.r=self.data["r"]
            self.g=self.data["g"]
            self.b=self.data["b"]
            self.i=self.data["i"]
            self.t=self.data["t"]
            self.w=self.data["w"]
        self.TabWidget_Properties='QTabWidget:pane{border: 0px;top:0px;background:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');}QTabBar:tab{color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');background:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+');border:0px;padding:6px 12px 6px 12px;}QTabBar::tab:selected{color:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+');background:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');margin-bottom: -1px;}'
        self.subTabWidget_Properties='QTabWidget:pane{border: 0px;top:0px;background:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+');}QTabBar:tab{color:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+');background:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');border:0px;padding:6px 12px 6px 12px;}QTabBar::tab:selected{color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');background:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+');margin-bottom: -1px;}'
        self.Button_Properties_0='QPushButton {color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');border-radius:3px;border:None;background-color:rgb('
        self.Button_Properties_1=');}QPushButton:hover{color:rgb('+f'{self.w[3]},{self.w[4]},{self.w[5]}'+');background-color:rgb('
        self.TextButton_Properties='QPushButton{background-color:transparent;border:None;color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');}QPushButton:hover{color:rgb('+f'{self.w[3]},{self.w[4]},{self.w[5]}'+');}'
        self.iconTextButton_Properties='QPushButton{background-color:transparent;border:None;color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');}QPushButton:hover{color:rgb('+f'{self.w[3]},{self.w[4]},{self.w[5]}'+');icon:url('
        self.configpTB_Properties='QPushButton{background-color:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+');border:None;color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');}QPushButton:hover{color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');}'
        self.GradientButton_Properties='QPushButton{color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');border-radius:3px;border:None;background-color:qlineargradient(spread:pad,x1:1,y1:0,x2:0,y2:0,stop:0 rgb('+f'{self.g[0]},{self.g[1]},{self.g[2]}'+'),stop:1 rgb('+f'{self.g[3]},{self.g[4]},{self.g[5]}'+'));}QPushButton:hover{background-color:qlineargradient(spread:pad,x1:1,y1:0,x2:0,y2:0,stop:0 rgb('+f'{self.g[6]},{self.g[7]},{self.g[8]}'+'),stop:1 rgb('+f'{self.g[9]},{self.g[10]},{self.g[11]}'+'));color:rgb('+f'{self.w[3]},{self.w[4]},{self.w[5]}'+');}'
        self.IconButton_Properties_0='QPushButton{image:url("'
        self.IconButton_Properties_1='");border-radius:3px;border:None;background-color:qlineargradient(spread:pad,x1:1,y1:0,x2:0,y2:0,stop:0 rgb('+f'{self.g[0]},{self.g[1]},{self.g[2]}'+'),stop:1 rgb('+f'{self.g[3]},{self.g[4]},{self.g[5]}'+'));}QPushButton:hover{background-color:qlineargradient(spread:pad,x1:1,y1:0,x2:0,y2:0,stop:0 rgb('+f'{self.g[6]},{self.g[7]},{self.g[8]}'+'),stop:1 rgb('+f'{self.g[9]},{self.g[10]},{self.g[11]}'+'));image:url("'
        self.ImageButton_Properties_0='QPushButton{background-color:transparent;border:None;background-image:url("'
        self.ImageButton_Properties_1='")}QPushButton:hover{background-image:url("'
        self.EditableLineEdit_Properties='QLineEdit{border-radius:3px;border:None;padding:3px;color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');background-color:rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');}QLineEdit:focus{color:rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');background-color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');}'
        self.NonEditableLineEdit_Properties='QLineEdit{background-color:transparent;border-radius:0px;border:None;padding:3px;color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');}'
        self.configNonEditableLineEdit_Properties='QLineEdit{background-color:transparent;border-radius:0px;border:1px solid rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');padding:3px;color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');}'
        self.NonEditablePlain_Properties='QPlainTextEdit{background-color:transparent;border-radius:0px;border:None;padding:3px;color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');}'
        self.TABNonEditablePlain_Properties='QPlainTextEdit{background-color:transparent;border-radius:0px;border:None;padding:3px;color:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+');}'
        self.subTABNonEditablePlain_Properties='QPlainTextEdit{background-color:transparent;border-radius:0px;border:None;padding:3px;color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');}'
        self.ComboBox_Properties_0='QComboBox:drop-down{border:None}QComboBox{border:1px solid rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');background-image:url("'
        self.ComboBox_Properties_1='");background-repeat:no-repeat;background-position:right}QAbstractItemView{outline:0;border:None;selection-background-color:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+');}QListView{padding:3px;border:None;color:rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');background-color:rgb('+f'{self.w[3]},{self.w[4]},{self.w[5]}'+')}QComboBox:hover{border:1px solid rgb('+f'{self.w[3]},{self.w[4]},{self.w[5]}'+');color:rgb('+f'{self.w[3]},{self.w[4]},{self.w[5]}'+');background-image:url("'
        self.CheckBox_Properties='QCheckBox{spacing:16px;color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');}QCheckBox:indicator{width:32px; height:32px;}QCheckBox:indicator:unchecked{image:url("./resources/uncheck.png");}QCheckBox:indicator:unchecked:hover{image:url("./resources/puncheck.png");}QCheckBox:indicator:unchecked:pressed{image:url("./resources/puncheck.png");}QCheckBox:indicator:checked{image:url("./resources/check.png");}QCheckBox:indicator:checked:hover{image:url("./resources/pcheck.png");}QCheckBox:indicator:checked:pressed{image:url("./resources/pcheck.png");}QCheckBox:hover{color:rgb('+f'{self.w[3]},{self.w[4]},{self.w[5]}'+');}'
        self.DeactivatedEditableLineEdit_Properties='QLineEdit{border-radius:3px;border:None;padding:3px;color:rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');background-color:rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');}QLineEdit:focus{color:rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');background-color:rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');}'
        self.DeactivatedButton_Properties='QPushButton{color:rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');border-radius:3px;border:None;background-color:rgb('+f'{self.t[0]},{self.t[1]},{self.t[2]}'+');}'
        self.DeactivatedIconButton_Properties_0='QPushButton{image:url("'
        self.DeactivatedIconButton_Properties_1='");border-radius:3px;border:None;background-color:rgb('+f'{self.t[0]},{self.t[1]},{self.t[2]}'+');}QPushButton:hover{background-color:rgb('+f'{self.t[0]},{self.t[1]},{self.t[2]}'+');image:url("'
        self.DeactivatedTextButton_Properties='QPushButton{background-color:transparent;border:None;color:rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');}QPushButton:hover{color:rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');}'
        self.DeactivatedComboBox_Properties='QComboBox:drop-down{border:None}QComboBox{border:1px solid rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');color:rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');background-image:url("./resources/ddown.png");background-repeat:no-repeat;background-position:right}QAbstractItemView{outline:0;border:None;selection-background-color:rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');}QListView{padding:3px;border:None;color:rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');background-color:rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+')}QComboBox:hover{border:1px solid rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');color:rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');background-image:url("./resources/ddown.png");}'
        self.Label_Properties='QLabel{color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');background-color:transparent;}'
        self.Frame_Properties='QFrame{background-color:transparent;border:1px solid rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');background-color:transparent;}'
        self.DB_Properties=self.ImageButton_Properties_0+'./resources/default.png'+self.ImageButton_Properties_1+'./resources/pdefault.png");}'
        self.dDB_Properties=self.ImageButton_Properties_0+'./resources/ddefault.png'+self.ImageButton_Properties_1+'./resources/ddefault.png");}'
        self.Increase_Properties=self.ImageButton_Properties_0+'./resources/increase.png'+self.ImageButton_Properties_1+'./resources/pincrease.png");}'
        self.dIncrease_Properties=self.ImageButton_Properties_0+'./resources/dincrease.png'+self.ImageButton_Properties_1+'./resources/dincrease.png");}'
        self.Decrease_Properties=self.ImageButton_Properties_0+'./resources/decrease.png'+self.ImageButton_Properties_1+'./resources/pdecrease.png");}'
        self.dDecrease_Properties=self.ImageButton_Properties_0+'./resources/ddecrease.png'+self.ImageButton_Properties_1+'./resources/ddecrease.png");}'
        self.configCheckBox_Properties='QCheckBox{spacing:6px 0px 0px 0px;color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');}QCheckBox:indicator{width:32px; height:32px;}QCheckBox:indicator:unchecked{image:url("./resources/uncheck.png");}QCheckBox:indicator:unchecked:hover{image:url("./resources/puncheck.png");}QCheckBox:indicator:unchecked:pressed{image:url("./resources/puncheck.png");}QCheckBox:indicator:checked{image:url("./resources/check.png");}QCheckBox:indicator:checked:hover{image:url("./resources/pcheck.png");}QCheckBox:indicator:checked:pressed{image:url("./resources/pcheck.png");}QCheckBox:hover{color:rgb('+f'{self.w[3]},{self.w[4]},{self.w[5]}'+');}'
        self.RadioButton_Properties='QRadioButton:indicator:unchecked{image:url("./resources/uncheckRB.png");}QRadioButton:indicator:unchecked:hover{image:url("./resources/uncheckRB.png");}QRadioButton:indicator:checked{image:url("./resources/checkRB.png");}QRadioButton:indicator:unchecked:hover{image:url("./resources/pcheckRB.png");}QRadioButton{border:None;border-radius:0px;background-color:rgb(' 
        self.setStyleSheet(f'background-color:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+');')
        self.SCMDWD_Label.setStyleSheet(self.Label_Properties)
        self.dTextName.setStyleSheet(self.Label_Properties)
        self.dTextGame.setStyleSheet(self.Label_Properties)
        self.dTextListed.setStyleSheet(self.Label_Properties)
        self.DownloadInfo_Label.setStyleSheet(self.Label_Properties)
        self.DownloadListPreview_Frame.setStyleSheet(self.Frame_Properties)
        self.Info_Frame.setStyleSheet(self.Frame_Properties)
        self.TitleBar_Frame.setStyleSheet('QFrame{border:None;background-color:rgb('+f'{self.t[0]},{self.t[1]},{self.t[2]}'+');}')
        self.dFrame.setStyleSheet('QFrame{border:None;background-color:rgb('+f'{self.t[0]},{self.t[1]},{self.t[2]}'+');}')
        self.DownloadListPreview_Button.setStyleSheet(self.TextButton_Properties)
        self.SteamCMD_Button.setStyleSheet(self.TextButton_Properties)
        self.Workshop_Button.setStyleSheet(self.TextButton_Properties)
        self.Mode_Button.setStyleSheet(self.TextButton_Properties)
        self.SAVELIST_Button.setStyleSheet(self.GradientButton_Properties)
        self.LOADLIST_Button.setStyleSheet(self.GradientButton_Properties)
        self.Folder_Button.setStyleSheet(self.IconButton_Properties_0+'./resources/folder.png'+self.IconButton_Properties_1+'./resources/pfolder.png");}')
        self.Config_Button.setStyleSheet(self.IconButton_Properties_0+'./resources/config.png'+self.IconButton_Properties_1+'./resources/pconfig.png");}')
        self.Minimize_Button.setStyleSheet(self.ImageButton_Properties_0+'./resources/minimize.png'+self.ImageButton_Properties_1+'./resources/pminimize.png");}')
        self.Close_Button.setStyleSheet(self.ImageButton_Properties_0+'./resources/close.png'+self.ImageButton_Properties_1+'./resources/pclose.png");}')
        self.User_Button.setStyleSheet(self.ImageButton_Properties_0+'./resources/user.png'+self.ImageButton_Properties_1+'./resources/puser.png");}')
        self.Password_Button.setStyleSheet(self.ImageButton_Properties_0+'./resources/password.png'+self.ImageButton_Properties_1+'./resources/ppassword.png");}')
        self.Guard_Button.setStyleSheet(self.ImageButton_Properties_0+'./resources/guard.png'+self.ImageButton_Properties_1+'./resources/pguard.png");}')
        self.Info_Button.setStyleSheet(self.ImageButton_Properties_0+'./resources/info.png'+self.ImageButton_Properties_1+'./resources/pinfo.png");}')
        self.SteamCMD_Line.setStyleSheet(self.EditableLineEdit_Properties)
        self.User_Line.setStyleSheet(self.EditableLineEdit_Properties)
        self.Password_Line.setStyleSheet(self.EditableLineEdit_Properties)
        self.Guard_Line.setStyleSheet(self.EditableLineEdit_Properties)
        self.Workshop_Plain.setStyleSheet('QPlainTextEdit{border-radius:3px;border:None;padding:3px;color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');background-color:rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');}QPlainTextEdit:focus{color:rgb('+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');background-color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');}')
        self.Info_Line.setStyleSheet(self.NonEditableLineEdit_Properties)
        self.RANP_CheckBox.setStyleSheet(self.CheckBox_Properties)
        self.dLink.setStyleSheet(self.EditableLineEdit_Properties)
        self.Pin_CheckBox.setStyleSheet('QCheckBox{background-color:transparent;spacing:16px;color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');}QCheckBox:indicator{width:32px; height:32px;}QCheckBox:indicator:unchecked{image:url("./resources/unpin.png");}QCheckBox:indicator:unchecked:hover{image:url("./resources/punpin.png");}QCheckBox:indicator:unchecked:pressed{image:url("./resources/punpin.png");}QCheckBox:indicator:checked{image:url("./resources/pin.png");}QCheckBox:indicator:checked:hover{image:url("./resources/ppin.png");}QCheckBox:indicator:checked:pressed{image:url("./resources/ppin.png");}QCheckBox:hover{color:rgb('+f'{self.w[3]},{self.w[4]},{self.w[5]}'+');}')
        self.Mode_ComboBox.setStyleSheet(self.ComboBox_Properties_0+'./resources/down.png'+self.ComboBox_Properties_1+'./resources/pdown.png");}')
        self.configBar_Frame.setStyleSheet('QFrame{border:None;background-color:rgb('+f'{self.t[0]},{self.t[1]},{self.t[2]}'+');}')
        self.configColorPalette_Label.setStyleSheet(self.Label_Properties)
        self.configES_Button.setStyleSheet(self.TextButton_Properties)
        self.configIH_Button.setStyleSheet(self.TextButton_Properties)
        self.configCR_Button.setStyleSheet(self.TextButton_Properties)
        self.configUPDATES_Button.setStyleSheet(self.GradientButton_Properties)
        self.configSandE_Button.setStyleSheet(self.Button_Properties_0+f'{self.a[0]},{self.a[1]},{self.a[2]}'+self.Button_Properties_1+f'{self.a[3]},{self.a[4]},{self.a[5]}'+');}')
        self.configDefault2_Button.setStyleSheet(self.DB_Properties)
        self.configDownloadFolder_Line.setStyleSheet(self.EditableLineEdit_Properties)
        self.configInfo_Frame.setStyleSheet(self.Frame_Properties)
        self.configInfo_Line.setStyleSheet(self.NonEditablePlain_Properties)
        self.configCDF_CheckBox.setStyleSheet(self.configCheckBox_Properties)
        self.configBSCIM_CheckBox.setStyleSheet(self.configCheckBox_Properties)
        self.configDLP_CheckBox.setStyleSheet(self.configCheckBox_Properties)
        self.configA_RadioButton.setStyleSheet(self.RadioButton_Properties+f'{self.a[0]},{self.a[1]},{self.a[2]}'+');}')
        self.configpA_RadioButton.setStyleSheet(self.RadioButton_Properties+f'{self.a[3]},{self.a[4]},{self.a[5]}'+');}')
        self.configD_RadioButton.setStyleSheet(self.RadioButton_Properties+f'{self.d[0]},{self.d[1]},{self.d[2]}'+');}')
        self.configR_RadioButton.setStyleSheet(self.RadioButton_Properties+f'{self.r[0]},{self.r[1]},{self.r[2]}'+');}')
        self.configGa_RadioButton.setStyleSheet(self.RadioButton_Properties+f'{self.g[0]},{self.g[1]},{self.g[2]}'+');}')
        self.configGb_RadioButton.setStyleSheet(self.RadioButton_Properties+f'{self.g[3]},{self.g[4]},{self.g[5]}'+');}')
        self.configpGa_RadioButton.setStyleSheet(self.RadioButton_Properties+f'{self.g[6]},{self.g[7]},{self.g[8]}'+');}')
        self.configpGb_RadioButton.setStyleSheet(self.RadioButton_Properties+f'{self.g[9]},{self.g[10]},{self.g[11]}'+');}')
        self.configB_RadioButton.setStyleSheet(self.RadioButton_Properties+f'{self.b[0]},{self.b[1]},{self.b[2]}'+');}')
        self.configI_RadioButton.setStyleSheet(self.RadioButton_Properties+f'{self.i[0]},{self.i[1]},{self.i[2]}'+');}')
        self.configT_RadioButton.setStyleSheet(self.RadioButton_Properties+f'{self.t[0]},{self.t[1]},{self.t[2]}'+');}')
        self.configW_RadioButton.setStyleSheet(self.RadioButton_Properties+f'{self.w[0]},{self.w[1]},{self.w[2]}'+');}')
        self.configpW_RadioButton.setStyleSheet(self.RadioButton_Properties+f'{self.w[3]},{self.w[4]},{self.w[5]}'+');}')
        self.IHTab_SteamCMD_Plain.setStyleSheet(self.TABNonEditablePlain_Properties)
        self.IHTab_SteamCMD_Button.setStyleSheet(self.GradientButton_Properties)
        self.IHTab_SteamCMD.setStyleSheet('background-color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+')')
        self.IHTab.setStyleSheet(self.TabWidget_Properties)
        self.IHTab_Account.setStyleSheet('background-color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+')')
        self.IHTab_Account_Plain.setStyleSheet(self.TABNonEditablePlain_Properties)
        self.IHTab_Workshop.setStyleSheet('background-color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+')')
        self.IHTab_Workshop_Plain.setStyleSheet(self.TABNonEditablePlain_Properties)
        self.IHTab_Workshop_Button.setStyleSheet(self.GradientButton_Properties)
        self.IHTab_Mode.setStyleSheet('background-color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+')')
        self.IHTab_Mode_Plain.setStyleSheet(self.TABNonEditablePlain_Properties)
        self.IHTab_DLP_Plain.setStyleSheet(self.TABNonEditablePlain_Properties)
        self.IHTab_DLP_Button.setStyleSheet(self.GradientButton_Properties)
        self.IHTab_DLP.setStyleSheet('background-color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+')')
        self.configRepeat_Label.setStyleSheet(self.Label_Properties)
        self.configRepeat_Line.setStyleSheet(self.EditableLineEdit_Properties)
        self.ESTab.setStyleSheet(self.TabWidget_Properties)
        self.ESTab_SCMDLM.setStyleSheet('background-color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+')')
        self.ESTab_SCMDWD.setStyleSheet('background-color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+')')
        self.ESTab_SteamCMD.setStyleSheet('background-color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+')')
        self.ESTab_SCMDLM.setStyleSheet('background-color:rgb('+f'{self.w[0]},{self.w[1]},{self.w[2]}'+')')
        self.ESTab_SCMDLM_subtab.setStyleSheet(self.subTabWidget_Properties)
        self.ESTab_SCMDLM_subtab_TAB0.setStyleSheet('background-color:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+')')
        self.ESTab_SCMDLM_subtab_TAB0_Plain.setStyleSheet(self.subTABNonEditablePlain_Properties)
        self.ESTab_SCMDLM_subtab_TAB1.setStyleSheet('background-color:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+')')
        self.ESTab_SCMDLM_subtab_TAB1_Plain.setStyleSheet(self.subTABNonEditablePlain_Properties)
        self.ESTab_SCMDLM_subtab_TAB2.setStyleSheet('background-color:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+')')
        self.ESTab_SCMDLM_subtab_TAB2_Plain.setStyleSheet(self.subTABNonEditablePlain_Properties)
        self.ESTab_SCMDLM_subtab_TAB3.setStyleSheet('background-color:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+')')
        self.ESTab_SCMDLM_subtab_TAB3_Plain.setStyleSheet(self.subTABNonEditablePlain_Properties)
        self.ESTab_SCMDLM_subtab_TAB3_Button.setStyleSheet(self.GradientButton_Properties)
        self.ESTab_SCMDLM_subtab_TAB4.setStyleSheet('background-color:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+')')
        self.ESTab_SCMDLM_subtab_TAB4_Plain.setStyleSheet(self.subTABNonEditablePlain_Properties)
        
        self.ESTab_SCMDWD_subtab.setStyleSheet(self.subTabWidget_Properties)
        self.ESTab_SCMDWD_subtab_TAB0.setStyleSheet('background-color:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+')')
        self.ESTab_SCMDWD_subtab_TAB0_Button.setStyleSheet(self.GradientButton_Properties)
        self.ESTab_SCMDWD_subtab_TAB0_Plain.setStyleSheet(self.subTABNonEditablePlain_Properties)
        self.ESTab_SCMDWD_subtab_TAB1.setStyleSheet('background-color:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+')')
        self.ESTab_SCMDWD_subtab_TAB1_Plain.setStyleSheet(self.subTABNonEditablePlain_Properties)
        self.ESTab_SCMDWD_subtab_TAB2.setStyleSheet('background-color:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+')')
        self.ESTab_SCMDWD_subtab_TAB2_Button.setStyleSheet(self.GradientButton_Properties)
        self.ESTab_SCMDWD_subtab_TAB2_Plain.setStyleSheet(self.subTABNonEditablePlain_Properties)
        self.ESTab_SCMDWD_subtab_TAB3.setStyleSheet('background-color:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+')')
        self.ESTab_SCMDWD_subtab_TAB3_Plain.setStyleSheet(self.subTABNonEditablePlain_Properties)
        self.ESTab_SCMDWD_subtab_TAB4.setStyleSheet('background-color:rgb('+f'{self.b[0]},{self.b[1]},{self.b[2]}'+')')
        self.ESTab_SCMDWD_subtab_TAB4_Button.setStyleSheet(self.GradientButton_Properties)
        self.ESTab_SCMDWD_subtab_TAB4_Plain.setStyleSheet(self.subTABNonEditablePlain_Properties)
        self.ESTab_SteamCMD_Plain.setStyleSheet(self.TABNonEditablePlain_Properties)
        self.ESTab_SteamCMD_Button.setStyleSheet(self.GradientButton_Properties)
        self.CRButton0.setStyleSheet(self.iconTextButton_Properties+'./resources/pdiscord.png'+')}')
        self.CRButton1.setStyleSheet(self.iconTextButton_Properties+'./resources/pgithub.png'+')}')
        self.CRButton2.setStyleSheet(self.iconTextButton_Properties+'./resources/pyoutube.png'+')}')
        self.PaletteUpdater()
        self.EXCEC_Activator()
        self.SAVELIST_Activator()
        self.OPENFOLDER_Activator()
        self.Default0_Activator()
        self.Default1_Activator()
        self.Default2_Activator()
        self.Default3_Activator()
    def EnableButtons(self):
        self.configES_Button.setDisabled(False)
        self.configIH_Button.setDisabled(False)
        self.configCR_Button.setDisabled(False)
        self.configOPTIONS_Button.setDisabled(False)
        self.configES_Button.setStyleSheet(self.TextButton_Properties)
        self.configIH_Button.setStyleSheet(self.TextButton_Properties)
        self.configCR_Button.setStyleSheet(self.TextButton_Properties)
        self.configOPTIONS_Button.setStyleSheet(self.TextButton_Properties)
    def CR(self):
        self.configCR_Button.setDisabled(True)
        self.configCR_Button.setStyleSheet(self.configpTB_Properties)
        self.lastIndex=self.Mode_ComboBox.currentIndex()
        self.configInfo_Line.setPlainText('This tab contains my contacts, my Youtube channel and the SCMD Workshop Downloader discord where you can report bugs or seek help about the app.')
        self.Mode_ComboBox.setCurrentIndex(0)
        self.HideConfig()
        self.HideIH()
        self.HideES()
        self.HideMain()
        self.OPENFOLDER_Button.hide()
        self.configBar_Frame.show()
        self.configSandE_Button.show()
        self.configSandE_Button.setText('EXIT')
        self.configInfo_Frame.show()
        self.configInfo_Line.show()
        self.configIH_Button.show()
        self.configES_Button.show()
        self.configCR_Button.show()
        self.configOPTIONS_Button.show()
        self.configUPDATES_Button.show()
        self.CRLabel.show()
        self.CRButton0.show()
        self.CRButton1.show()
        self.CRButton2.show()
    def HideCR(self):
        self.CRLabel.hide()
        self.CRButton0.hide()
        self.CRButton1.hide()
        self.CRButton2.hide()
    def ES(self):
        self.configES_Button.setDisabled(True)
        self.configES_Button.setStyleSheet(self.configpTB_Properties)
        self.lastIndex=self.Mode_ComboBox.currentIndex()
        self.configInfo_Line.setPlainText('This tab is a guide on the problems that SCMD Workshop Downloader can present and how to solve them.')
        self.Mode_ComboBox.setCurrentIndex(0)
        self.HideConfig()
        self.HideIH()
        self.HideCR()
        self.HideMain()
        self.OPENFOLDER_Button.hide()
        self.configBar_Frame.show()
        self.configSandE_Button.show()
        self.configSandE_Button.setText('EXIT')
        self.configInfo_Frame.show()
        self.configInfo_Line.show()
        self.configIH_Button.show()
        self.configES_Button.show()
        self.configCR_Button.show()
        self.configOPTIONS_Button.show()
        self.configUPDATES_Button.show()
        self.ESTab.show()
    def HideES(self):
        self.ESTab.hide()
        pass
    def IH(self):
        self.configIH_Button.setDisabled(True)
        self.configIH_Button.setStyleSheet(self.configpTB_Properties)
        self.lastIndex=self.Mode_ComboBox.currentIndex()
        self.configInfo_Line.setPlainText('This tab is a guide on the use of SCMD Workshop Downloader and its features.')
        self.Mode_ComboBox.setCurrentIndex(0)
        self.HideConfig()
        self.HideMain()
        self.HideES()
        self.HideCR()
        self.OPENFOLDER_Button.hide()
        self.configBar_Frame.show()
        self.configSandE_Button.show()
        self.configSandE_Button.setText('EXIT')
        self.configInfo_Frame.show()
        self.configInfo_Line.show()
        self.configIH_Button.show()
        self.configES_Button.show()
        self.configCR_Button.show()
        self.configOPTIONS_Button.show()
        self.configUPDATES_Button.show()
        self.IHTab.show()
    def HideIH(self):
        self.IHTab.hide()
    def RepeatFix(self):
        if not self.configRepeat_Line.text() or self.configRepeat_Line.text()=='0':
            self.configRepeat_Line.setText('1')
    def Config(self):
        self.configOPTIONS_Button.setDisabled(True)
        self.configOPTIONS_Button.setStyleSheet(self.configpTB_Properties)
        self.lastIndex=self.Mode_ComboBox.currentIndex()
        self.configInfo_Line.setPlainText('This window will show you information about the configuration options of this tab.')
        self.Mode_ComboBox.setCurrentIndex(0)
        self.OPENFOLDER_Button.setFixedSize(438,32)
        self.OPENFOLDER_Button.move(12,82)
        self.configRepeat_Label.show()
        self.configRepeat_Line.show()
        self.OPENFOLDER_Button.show()
        self.configA_RadioButton.show()
        self.configpA_RadioButton.show()
        self.configD_RadioButton.show()
        self.configR_RadioButton.show()
        self.configGa_RadioButton.show()
        self.configGb_RadioButton.show()
        self.configpGa_RadioButton.show()
        self.configpGb_RadioButton.show()
        self.configB_RadioButton.show()
        self.configI_RadioButton.show()
        self.configT_RadioButton.show()
        self.configW_RadioButton.show()
        self.configpW_RadioButton.show()
        self.configBar_Frame.show()
        self.configIH_Button.show()
        self.configES_Button.show()
        self.configCR_Button.show()
        self.configOPTIONS_Button.show()
        self.configUPDATES_Button.show()
        self.configRGB_Button.show()
        self.configCustom_Button.show()
        self.configDefault_Button.show()
        self.configBright_Button.show()
        self.configSandE_Button.show()
        self.configInfo_Frame.show()
        self.configInfo_Line.show()
        self.configR_Line.show()
        self.configG_Line.show()
        self.configB_Line.show()
        self.configColorPalette_Label.show()
        self.configCDF_CheckBox.show()
        self.configBSCIM_CheckBox.show()
        self.configDLP_CheckBox.show()
        self.configDownloadFolder_Line.show()
        self.configDefault0_Button.show()
        self.configDefault1_Button.show()
        self.configDefault2_Button.show()
        self.configDefault3_Button.show()
        self.configSandE_Button.setText('SAVE && EXIT')
        self.HideIH()
        self.HideES()
        self.HideCR()
        self.HideMain()
        self.RGB()
    def HideMain(self):
        try:
            self.dIncrease.hide()
            self.dDecrease.hide()
            self.Info_Frame.hide()
            self.SteamCMD_Button.hide()
            self.Workshop_Button.hide()
            self.Mode_Button.hide()
            self.SAVELIST_Button.hide()
            self.LOADLIST_Button.hide()
            self.EXCEC_Button.hide()
            self.Folder_Button.hide()
            self.Config_Button.hide()
            self.User_Button.hide()
            self.Password_Button.hide()
            self.Guard_Button.hide()
            self.SteamCMD_Line.hide()
            self.User_Line.hide()
            self.Password_Line.hide()
            self.Guard_Line.hide()
            self.Workshop_Plain.hide()
            self.Info_Line.hide()
            self.Info_Button.hide()
            self.RANP_CheckBox.hide()
            self.Mode_ComboBox.hide()
            self.DownloadInfo_Label.hide()
            self.DownloadListPreview_Frame.hide()
            self.DownloadListPreview_Button.hide()
            self.dLink.hide()
            self.dFrame.hide()
            self.dLabel.hide()
            self.dTextGame.hide()
            self.dTextListed.hide()
            self.dTextName.hide()
        except:
            pass
    def Show(self):
        self.OPENFOLDER_Button.show()
        self.dIncrease.show()
        self.dDecrease.show()
        self.Info_Frame.show()
        self.SteamCMD_Button.show()
        self.Workshop_Button.show()
        self.Mode_Button.show()
        self.SAVELIST_Button.show()
        self.LOADLIST_Button.show()
        self.EXCEC_Button.show()
        self.Folder_Button.show()
        self.Config_Button.show()
        self.User_Button.show()
        self.Password_Button.show()
        self.Guard_Button.show()
        self.SteamCMD_Line.show()
        self.User_Line.show()
        self.Password_Line.show()
        self.Guard_Line.show()
        self.Workshop_Plain.show()
        self.Info_Line.show()
        self.Info_Button.show()
        self.RANP_CheckBox.show()
        self.Mode_ComboBox.show()
        self.DownloadInfo_Label.show()
        self.DownloadListPreview_Frame.show()
        self.DownloadListPreview_Button.show()
        self.dLink.show()
        self.dFrame.show()
        self.dLabel.show()
        self.dTextGame.show()
        self.dTextListed.show()
        self.dTextName.show()
        self.getData_link()
    def HideConfig(self):
        self.configOPTIONS_Button.setEnabled(True)
        self.configRepeat_Label.hide()
        self.configRepeat_Line.hide()
        self.configA_RadioButton.hide()
        self.configpA_RadioButton.hide()
        self.configD_RadioButton.hide()
        self.configR_RadioButton.hide()
        self.configGa_RadioButton.hide()
        self.configGb_RadioButton.hide()
        self.configpGa_RadioButton.hide()
        self.configpGb_RadioButton.hide()
        self.configB_RadioButton.hide()
        self.configI_RadioButton.hide()
        self.configT_RadioButton.hide()
        self.configW_RadioButton.hide()
        self.configpW_RadioButton.hide()
        self.configBar_Frame.hide()
        self.configIH_Button.hide()
        self.configES_Button.hide()
        self.configCR_Button.hide()
        self.configOPTIONS_Button.hide()
        self.configUPDATES_Button.hide()
        self.configRGB_Button.hide()
        self.configCustom_Button.hide()
        self.configDefault_Button.hide()
        self.configBright_Button.hide()
        self.configSandE_Button.hide()
        self.configInfo_Frame.hide()
        self.configInfo_Line.hide()
        self.configR_Line.hide()
        self.configG_Line.hide()
        self.configB_Line.hide()
        self.configColorPalette_Label.hide()
        self.configCDF_CheckBox.hide()
        self.configBSCIM_CheckBox.hide()
        self.configDLP_CheckBox.hide()
        self.configDownloadFolder_Line.hide()
        self.configDefault0_Button.hide()
        self.configDefault1_Button.hide()
        self.configDefault2_Button.hide()
        self.configDefault3_Button.hide()
        self.OPENFOLDER_Button.setFixedSize(304,32)
        self.OPENFOLDER_Button.move(12,234)
        try:
            self.Mode_ComboBox.setCurrentIndex(self.lastIndex)
        except:
            pass
    def Default0_Activator(self):
        if self.configCDF_CheckBox.isChecked()==True:
            self.configDefault0_Button.setEnabled(True)
            self.configDefault0_Button.setStyleSheet(self.DB_Properties)
        else:
            self.configDefault0_Button.setDisabled(True)
            self.configDefault0_Button.setStyleSheet(self.dDB_Properties)
    def Default0(self):
        self.configCDF_CheckBox.setChecked(False)
        self.Default0_Activator()
        self.SaveData()
    def Default1_Activator(self):
        if self.configBSCIM_CheckBox.isChecked()==True:
            self.configDefault1_Button.setEnabled(True)
            self.configDefault1_Button.setStyleSheet(self.DB_Properties)
        else:
            self.configDefault1_Button.setDisabled(True)
            self.configDefault1_Button.setStyleSheet(self.dDB_Properties)
    def Default1(self):
        self.configBSCIM_CheckBox.setChecked(False)
        self.Default1_Activator()
        self.SaveData()
    def Default2_Activator(self):
        if self.configDLP_CheckBox.isChecked()==False:
            self.configDefault2_Button.setEnabled(True)
            self.configDefault2_Button.setStyleSheet(self.DB_Properties)
        else:
            self.configDefault2_Button.setDisabled(True)
            self.configDefault2_Button.setStyleSheet(self.dDB_Properties)
    def Default2(self):
        self.configDLP_CheckBox.setChecked(True)
        self.Default2_Activator()
        self.SaveData()
    def RGBPicker(self):
        Pick=QtWidgets.QColorDialog.getColor()
        self.configR_Line.setText(str(Pick.red()))
        self.configG_Line.setText(str(Pick.green()))
        self.configB_Line.setText(str(Pick.blue()))
    def RGB(self):
        if self.data["ca"]!=self.data["a"] or self.data["cd"]!=self.data["d"] or self.data["cr"]!=self.data["r"] or self.data["cg"]!=self.data["g"] or self.data["cb"]!=self.data["b"] or self.data["ci"]!=self.data["i"] or self.data["ct"]!=self.data["t"] or self.data["cw"]!=self.data["w"]:
            self.data["d3"]=True
        else:
            self.data["d3"]=False
        try:
            self.configR_Line.textChanged.disconnect()
            self.configG_Line.textChanged.disconnect()
            self.configB_Line.textChanged.disconnect()
        except:
            pass
        self.PaletteUpdater()
        if self.configA_RadioButton.isChecked()==True:
            self.configR_Line.setText(str(self.a[0]))
            self.configG_Line.setText(str(self.a[1]))
            self.configB_Line.setText(str(self.a[2]))
        if self.configpA_RadioButton.isChecked()==True:
            self.configR_Line.setText(str(self.a[3]))
            self.configG_Line.setText(str(self.a[4]))
            self.configB_Line.setText(str(self.a[5]))
        if self.configD_RadioButton.isChecked()==True:
            self.configR_Line.setText(str(self.d[0]))
            self.configG_Line.setText(str(self.d[1]))
            self.configB_Line.setText(str(self.d[2]))
        if self.configR_RadioButton.isChecked()==True:
            self.configR_Line.setText(str(self.r[0]))
            self.configG_Line.setText(str(self.r[1]))
            self.configB_Line.setText(str(self.r[2]))
        if self.configGa_RadioButton.isChecked()==True:
            self.configR_Line.setText(str(self.g[0]))
            self.configG_Line.setText(str(self.g[1]))
            self.configB_Line.setText(str(self.g[2]))
        if self.configGb_RadioButton.isChecked()==True:
            self.configR_Line.setText(str(self.g[3]))
            self.configG_Line.setText(str(self.g[4]))
            self.configB_Line.setText(str(self.g[5]))
        if self.configpGa_RadioButton.isChecked()==True:
            self.configR_Line.setText(str(self.g[6]))
            self.configG_Line.setText(str(self.g[7]))
            self.configB_Line.setText(str(self.g[8]))
        if self.configpGb_RadioButton.isChecked()==True:
            self.configR_Line.setText(str(self.g[9]))
            self.configG_Line.setText(str(self.g[10]))
            self.configB_Line.setText(str(self.g[11]))
        if self.configB_RadioButton.isChecked()==True:
            self.configR_Line.setText(str(self.b[0]))
            self.configG_Line.setText(str(self.b[1]))
            self.configB_Line.setText(str(self.b[2]))
        if self.configI_RadioButton.isChecked()==True:
            self.configR_Line.setText(str(self.i[0]))
            self.configG_Line.setText(str(self.i[1]))
            self.configB_Line.setText(str(self.i[2]))
        if self.configT_RadioButton.isChecked()==True:
            self.configR_Line.setText(str(self.t[0]))
            self.configG_Line.setText(str(self.t[1]))
            self.configB_Line.setText(str(self.t[2]))
        if self.configW_RadioButton.isChecked()==True:
            self.configR_Line.setText(str(self.w[0]))
            self.configG_Line.setText(str(self.w[1]))
            self.configB_Line.setText(str(self.w[2]))
        if self.configpW_RadioButton.isChecked()==True:
            self.configR_Line.setText(str(self.w[3]))
            self.configG_Line.setText(str(self.w[4]))
            self.configB_Line.setText(str(self.w[5]))
        self.configR_Line.textChanged.connect(self.RGBLineMod)
        self.configG_Line.textChanged.connect(self.RGBLineMod)
        self.configB_Line.textChanged.connect(self.RGBLineMod)
        self.sSS()
    def RGBLineMod(self):
        if self.data["palette"]==2:
            if self.configA_RadioButton.isChecked()==True:
                    self.data["ca"][0]=self.configR_Line.text()
                    self.data["ca"][1]=self.configG_Line.text()
                    self.data["ca"][2]=self.configB_Line.text()
            if self.configpA_RadioButton.isChecked()==True:
                    self.data["ca"][3]=self.configR_Line.text()
                    self.data["ca"][4]=self.configG_Line.text()
                    self.data["ca"][5]=self.configB_Line.text()
            if self.configD_RadioButton.isChecked()==True:
                    self.data["cd"][0]=self.configR_Line.text()
                    self.data["cd"][1]=self.configG_Line.text()
                    self.data["cd"][2]=self.configB_Line.text()
            if self.configR_RadioButton.isChecked()==True:
                    self.data["cr"][0]=self.configR_Line.text()
                    self.data["cr"][1]=self.configG_Line.text()
                    self.data["cr"][2]=self.configB_Line.text()
            if self.configGa_RadioButton.isChecked()==True:
                    self.data["cg"][0]=self.configR_Line.text()
                    self.data["cg"][1]=self.configG_Line.text()
                    self.data["cg"][2]=self.configB_Line.text()
            if self.configGb_RadioButton.isChecked()==True:
                    self.data["cg"][3]=self.configR_Line.text()
                    self.data["cg"][4]=self.configG_Line.text()
                    self.data["cg"][5]=self.configB_Line.text()
            if self.configpGa_RadioButton.isChecked()==True:
                    self.data["cg"][6]=self.configR_Line.text()
                    self.data["cg"][7]=self.configG_Line.text()
                    self.data["cg"][8]=self.configB_Line.text()
            if self.configpGb_RadioButton.isChecked()==True:
                    self.data["cg"][9]=self.configR_Line.text()
                    self.data["cg"][10]=self.configG_Line.text()
                    self.data["cg"][11]=self.configB_Line.text()
            if self.configB_RadioButton.isChecked()==True:
                    self.data["cb"][0]=self.configR_Line.text()
                    self.data["cb"][1]=self.configG_Line.text()
                    self.data["cb"][2]=self.configB_Line.text()
            if self.configI_RadioButton.isChecked()==True:
                    self.data["ci"][0]=self.configR_Line.text()
                    self.data["ci"][1]=self.configG_Line.text()
                    self.data["ci"][2]=self.configB_Line.text()
            if self.configT_RadioButton.isChecked()==True:
                    self.data["ct"][0]=self.configR_Line.text()
                    self.data["ct"][1]=self.configG_Line.text()
                    self.data["ct"][2]=self.configB_Line.text()
            if self.configW_RadioButton.isChecked()==True:
                    self.data["cw"][0]=self.configR_Line.text()
                    self.data["cw"][1]=self.configG_Line.text()
                    self.data["cw"][2]=self.configB_Line.text()
            if self.configpW_RadioButton.isChecked()==True:
                    self.data["cw"][3]=self.configR_Line.text()
                    self.data["cw"][4]=self.configG_Line.text()
                    self.data["cw"][5]=self.configB_Line.text()
        self.PaletteUpdater()
        self.RGB()
    def Default3_Activator(self):
        if self.data["d3"]!=False or self.data["palette"]!=0:
                self.configDefault3_Button.setEnabled(True)
                self.configDefault3_Button.setStyleSheet(self.DB_Properties)
        else:
            if self.configDefault3_Button.isEnabled()!=False:
                self.configDefault3_Button.setDisabled(True)
                self.configDefault3_Button.setStyleSheet(self.dDB_Properties)
    def Default3(self):
        self.data["palette"]=0
        self.data["ca"]=[92, 126, 16, 117, 160, 21]
        self.data["cd"]=[194, 172, 93]
        self.data["cr"]=[194, 93, 93]
        self.data["cg"]=[61, 163, 241, 36, 96, 208, 71, 191, 255, 49, 135, 227]
        self.data["cb"]=[23, 26, 33]
        self.data["ci"]=[50, 53, 60]
        self.data["ct"]=[35, 38, 43]
        self.data["cw"]=[199, 213, 224, 255, 255, 255]
        self.PaletteUpdater()
        self.RGBLineMod()
        self.SaveData()
        self.RGB()
    def PaletteUpdater(self):
        if self.configOPTIONS_Button.isCheckable()==False:
            self.configOPTIONS_Button.setStyleSheet(self.configpTB_Properties)
        if self.data["palette"]==2:
            self.configCustom_Button.setStyleSheet(self.DeactivatedButton_Properties)
            self.configDefault_Button.setStyleSheet(self.GradientButton_Properties)
            self.configBright_Button.setStyleSheet(self.GradientButton_Properties)
            self.configCustom_Button.setDisabled(True)
            self.configDefault_Button.setEnabled(True)
            self.configBright_Button.setEnabled(True)
            self.configR_Line.setStyleSheet(self.EditableLineEdit_Properties)
            self.configG_Line.setStyleSheet(self.EditableLineEdit_Properties)
            self.configB_Line.setStyleSheet(self.EditableLineEdit_Properties)
            self.configR_Line.setReadOnly(False)
            self.configG_Line.setReadOnly(False)
            self.configB_Line.setReadOnly(False)
            self.configRGB_Button.setEnabled(True)
            self.configRGB_Button.setStyleSheet(self.GradientButton_Properties)
            self.configRGB_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        else:
            if self.data["palette"]==1:
                self.configCustom_Button.setStyleSheet(self.GradientButton_Properties)
                self.configDefault_Button.setStyleSheet(self.GradientButton_Properties)
                self.configBright_Button.setStyleSheet(self.DeactivatedButton_Properties)
                self.configCustom_Button.setEnabled(True)
                self.configDefault_Button.setEnabled(True)
                self.configBright_Button.setDisabled(True)
            else:
                self.configCustom_Button.setStyleSheet(self.GradientButton_Properties)
                self.configDefault_Button.setStyleSheet(self.DeactivatedButton_Properties)
                self.configBright_Button.setStyleSheet(self.GradientButton_Properties)
                self.configCustom_Button.setEnabled(True)
                self.configDefault_Button.setDisabled(True)
                self.configBright_Button.setEnabled(True)
            self.configR_Line.setStyleSheet(self.configNonEditableLineEdit_Properties)
            self.configG_Line.setStyleSheet(self.configNonEditableLineEdit_Properties)
            self.configB_Line.setStyleSheet(self.configNonEditableLineEdit_Properties)
            self.configR_Line.setReadOnly(True)
            self.configG_Line.setReadOnly(True)
            self.configB_Line.setReadOnly(True)
            self.configRGB_Button.setDisabled(True)
            self.configRGB_Button.setStyleSheet(self.DeactivatedButton_Properties)
            self.configRGB_Button.setCursor(QCursor(QtCore.Qt.ArrowCursor))
        self.Default3_Activator()
    def DLP(self):
        if self.configDLP_CheckBox.isChecked()==True:
            self.DownloadListPreview()
            self.IDManager()
        else:
            self.deactivateDownloadListPreview()
    def EXCEC_Name(self):
        if self.Mode_ComboBox.currentIndex()==2 or self.Mode_ComboBox.currentIndex()==3:
            self.EXCEC_Button.setText('GENERATE')
        elif self.Mode_ComboBox.currentIndex()==0 or self.Mode_ComboBox.currentIndex()==1:
            self.EXCEC_Button.setText('DOWNLOAD')
        elif self.Mode_ComboBox.currentIndex()==4 or self.Mode_ComboBox.currentIndex()==5:
            self.EXCEC_Button.setText('DOWNLOAD && GENERATE')
    def EXCEC_Activator(self):
        self.workshop=self.Workshop_Plain.toPlainText()
        self.realpath=(((str(self.SteamCMD_Line.text())).replace('/steamcmd.exe',''))+'/steamcmd.exe')
        doessteamcmdexist=os.path.exists(self.realpath)
        if doessteamcmdexist==True and self.workshop!='':
            self.EXCEC_Button.setStyleSheet(self.Button_Properties_0+f'{self.a[0]},{self.a[1]},{self.a[2]}'+self.Button_Properties_1+f'{self.a[3]},{self.a[4]},{self.a[5]}'+');}')
            self.EXCEC_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            try:
                self.EXCEC_Button.clicked.disconnect()
            except:
                pass
            self.EXCEC_Button.clicked.connect(lambda: self.Disabler())
            self.EXCEC_Button.clicked.connect(lambda: self.PreScript())
            self.EXCEC_Button.clicked.connect(lambda: self.PreProcess())
        elif doessteamcmdexist==False or self.workshop=='':
            self.EXCEC_Button.setStyleSheet(self.DeactivatedButton_Properties)
            self.EXCEC_Button.setCursor(QCursor(QtCore.Qt.ArrowCursor))
            try:
                self.EXCEC_Button.clicked.disconnect()
            except:
                pass
        self.EXCEC_Name()
    def SAVELIST_Activator(self):
        if self.Workshop_Plain.toPlainText()!='':
            self.SAVELIST_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            self.SAVELIST_Button.setStyleSheet(self.GradientButton_Properties)
            try:
                self.SAVELIST_Button.clicked.disconnect()
            except:
                pass
            self.SAVELIST_Button.clicked.connect(lambda:self.SaveList())
        else:
            self.SAVELIST_Button.setCursor(QCursor(QtCore.Qt.ArrowCursor))
            self.SAVELIST_Button.setStyleSheet(self.DeactivatedButton_Properties)
            try:
                self.SAVELIST_Button.clicked.disconnect()
            except:
                pass
    def OPENFOLDER_Activator(self):
        if self.Mode_ComboBox.currentIndex()==4 or self.Mode_ComboBox.currentIndex()==5:
            self.OPENFOLDER_Button.setText('OPEN FOLDERS')
        else:
            self.OPENFOLDER_Button.setText('OPEN FOLDER')
        if self.data["cdf"]==False:
            self.content_path=self.SteamCMD_Line.text()
            self.content_path=((str(self.SteamCMD_Line.text())).replace('/steamcmd.exe',''))
            self.content_path+='\steamapps\workshop\content'
        else:
            self.content_path=os.path.realpath(self.configDownloadFolder_Line.text())
        if os.path.exists(os.path.realpath(self.content_path))==True:
            self.OPENFOLDER_Button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            self.OPENFOLDER_Button.setStyleSheet(self.GradientButton_Properties)
            try:
                self.OPENFOLDER_Button.clicked.disconnect()
            except:
                pass
            self.data['steamcmd']=self.SteamCMD_Line.text()
            self.OPENFOLDER_Button.clicked.connect(lambda:self.OpenFolder())
            self.SaveData()
        else:
            self.OPENFOLDER_Button.setStyleSheet(self.DeactivatedButton_Properties)
            self.OPENFOLDER_Button.setCursor(QCursor(QtCore.Qt.ArrowCursor))
            try:
                self.OPENFOLDER_Button.clicked.disconnect()
            except:
                pass
            self.SaveData()
    def Disabler(self):
        self.LOADLIST_Button.setDisabled(True)
        self.SAVELIST_Button.setDisabled(True)
        self.OPENFOLDER_Button.setDisabled(True)
        self.EXCEC_Button.setDisabled(True)
        self.Config_Button.setDisabled(True)
        self.SteamCMD_Line.setDisabled(True)
        self.User_Line.setDisabled(True)
        self.Password_Line.setDisabled(True)
        self.Guard_Line.setDisabled(True)
        self.Workshop_Plain.setDisabled(True)
        self.SteamCMD_Button.setDisabled(True)
        self.Workshop_Button.setDisabled(True)
        self.Folder_Button.setDisabled(True)
        self.User_Button.setDisabled(True)
        self.Password_Button.setDisabled(True)
        self.Guard_Button.setDisabled(True)
        self.RANP_CheckBox.setDisabled(True)
        self.Mode_Button.setDisabled(True)
        self.Mode_ComboBox.setDisabled(True)
        self.DownloadListPreview_Button.setDisabled(True)
        self.notallowed0.show()
        self.notallowed1.show()
        self.notallowed2.show()
    def Enabler(self):
        self.LOADLIST_Button.setDisabled(False)
        self.SAVELIST_Button.setDisabled(False)
        self.OPENFOLDER_Button.setDisabled(False)
        self.EXCEC_Button.setDisabled(False)
        self.Config_Button.setDisabled(False)
        self.SteamCMD_Line.setDisabled(False)
        self.User_Line.setDisabled(False)
        self.Password_Line.setDisabled(False)
        self.Guard_Line.setDisabled(False)
        self.Workshop_Plain.setDisabled(False)
        self.SteamCMD_Button.setDisabled(False)
        self.Workshop_Button.setDisabled(False)
        self.Folder_Button.setDisabled(False)
        self.User_Button.setDisabled(False)
        self.Password_Button.setDisabled(False)
        self.Guard_Button.setDisabled(False)
        self.RANP_CheckBox.setDisabled(False)
        self.Mode_Button.setDisabled(False)
        self.Mode_ComboBox.setDisabled(False)
        self.DownloadListPreview_Button.setDisabled(False)
        self.notallowed0.hide()
        self.notallowed1.hide()
        self.notallowed2.hide()
    def ScriptCleaner(self):
        self.linksfixedlist=[]
        self.script=''
        self.appcondition='https://steamcommunity.com/app/'
        self.itemcondition='https://steamcommunity.com/sharedfiles/filedetails/?id='
        self.collectioncondition='https://steamcommunity.com/workshop/browse/?section=collections&appid='
    def PreScript(self):
        self.script=f'{self.realpath}'
        if self.data["cdf"]==True:
            self.script+=f' +force_install_dir {os.path.realpath(self.data["dfolder"])}'
        self.script+=' +login '
        if self.User_Line.text()!='' and self.Password_Line.text()!='':
            self.script+=f'{self.User_Line.text()} {self.Password_Line.text()}'
            if self.Guard_Line.text()!='':
                self.script+=f' {self.Guard_Line.text()}'
        else:
            self.script+='anonymous'
        self.workshopcontent=(str(self.workshop).replace(' ','\n')).split('\n')
        for coln in range(len(self.workshopcontent)):
            linkfixed=self.workshopcontent[coln].split('&searchtext=')[0]
            if 'https://steamcommunity.com/sharedfiles/filedetails/?id=' in linkfixed:
                self.linksfixedlist.append(linkfixed)
    def PreProcess(self):
        datetimenow=(str(datetime.datetime.now()).replace(':','-')).split(".")
        download={"script":self.script,"list":self.linksfixedlist,"datetime":datetimenow}
        with open('./data/download.json','w') as f:
            json.dump(download,f)
        if os.path.exists(os.path.realpath('SCMD List Manager.exe'))==True:
            try:
                os.startfile(os.path.realpath('SCMD List Manager.exe'))
            except:
                self.Info_Line.setText('SCMD List Manager is broken (0)')
                try:
                    self.Info_Button.disconnect()
                except:
                    pass
                self.Info_Button.clicked.connect(lambda:self.EnableButtons())
                self.Info_Button.clicked.connect(lambda:self.ES())
                self.Info_Button.clicked.connect(lambda:self.ESTab.setCurrentIndex(1))
                self.Info_Button.clicked.connect(lambda:self.ESTab_SCMDWD_subtab.setCurrentIndex(0))
                self.Info_Button.clicked.connect(lambda:self.ESTab_SCMDLM_subtab.setCurrentIndex(0))
                self.InfoError()
            self.Info_Line.setText('SCMD List Manager started')
        else:
            self.Info_Line.setText('SCMD List Manager not found (1)')
            try:
                    self.Info_Button.disconnect()
            except:
                pass
            self.Info_Button.clicked.connect(lambda:self.EnableButtons())
            self.Info_Button.clicked.connect(lambda:self.ES())
            self.Info_Button.clicked.connect(lambda:self.ESTab.setCurrentIndex(1))
            self.Info_Button.clicked.connect(lambda:self.ESTab_SCMDWD_subtab.setCurrentIndex(1))
            self.Info_Button.clicked.connect(lambda:self.ESTab_SCMDLM_subtab.setCurrentIndex(0))
            self.InfoError()
        self.ScriptCleaner()
        self.Enabler()
    def InfoReset(self):
        self.Info_Line.clear()
        self.Info_Line.setFixedSize(556,32)
        try:
            self.Info_Button.clicked().disconnect()
        except:
            pass
        self.Info_Button.move(-16,-16)
    def InfoError(self):
        self.Info_Line.setFixedSize(525,32)
        self.Info_Button.move(589,318)
    def DownloadListPreview(self):
        self.User_Line.textChanged.connect(self.DownloadInfo)
        self.Guard_Line.textChanged.connect(self.DownloadInfo)
        self.Password_Line.textChanged.connect(self.DownloadInfo)
        try:
            self.Workshop_Plain.disconnect()
            self.Workshop_Plain.textChanged.connect(self.EXCEC_Activator)
            self.Workshop_Plain.textChanged.connect(self.SAVELIST_Activator)
            self.Workshop_Plain.textChanged.connect(self.InfoReset)
            self.Workshop_Plain.textChanged.connect(self.getData_workshop)
        except:
            pass
        self.dLink.setDisabled(False)
        wlen=self.Workshop_Plain.toPlainText().replace(' ','\n').split('\n')
        self.dLink.setText(str(len(wlen)))
        self.IDManager()
        self.DownloadInfo()
    def deactivateDownloadListPreview(self):
        try:
            self.Workshop_Plain.disconnect()
            self.Workshop_Plain.textChanged.connect(self.EXCEC_Activator)
            self.Workshop_Plain.textChanged.connect(self.SAVELIST_Activator)
            self.Workshop_Plain.textChanged.connect(self.InfoReset)
        except:
            pass
        self.dDecrease.setStyleSheet(self.dDecrease_Properties)
        self.dIncrease.setStyleSheet(self.dIncrease_Properties)
        self.dIncrease.setDisabled(True)
        self.dDecrease.setDisabled(True)
        self.dLink.setText('0')
        self.dLink.setDisabled(True)
        self.wdict['isZero']=True
        self.wdict['isValid']='Closed'
        self.excecuteChanges()
        self.DownloadInfo()
    def DownloadInfo(self):
        if self.User_Line.text()!='' and self.Password_Line.text()!='':
            if self.Guard_Line.text()!='':
                self.DownloadInfo_Label.setText('Manifested with Guard code')
            else:
                self.DownloadInfo_Label.setText('Manifested')
        else:
            self.DownloadInfo_Label.setText('Anonymous')
        try:
            if self.dLink.text()!='0':
                if self.dTextListed.text()!='Listed':
                    self.getData_login()
        except:
            pass
    def SteamCMD(self):
        steamcmd=QFileDialog.getOpenFileName(self,'Select steamcmd.exe','','SteamCMD executable (steamcmd.exe)')
        if steamcmd:
            self.SteamCMD_Line.setText(steamcmd[0])
    def OpenFolder(self):
        self.OPENFOLDER_Activator()
        if os.path.exists(os.path.realpath('./generated scripts'))==False:
            os.mkdir('./generated scripts')
        try:
            if self.Mode_ComboBox.currentIndex()==0 or self.Mode_ComboBox.currentIndex()==1:
                if self.data["cdf"]==True:
                    self.Info_Line.setText('Custom download folder opened')
                else:
                    self.Info_Line.setText('SteamCMD download folder opened')
                os.startfile(os.path.realpath(self.content_path))
            if self.Mode_ComboBox.currentIndex()==2 or self.Mode_ComboBox.currentIndex()==3:
                os.startfile(os.path.realpath('./generated scripts'))
                self.Info_Line.setText('Scripts folder opened')
            if self.Mode_ComboBox.currentIndex()==4 or self.Mode_ComboBox.currentIndex()==5:
                os.startfile(os.path.realpath(self.content_path))
                os.startfile(os.path.realpath('./generated scripts'))
                if self.data["cdf"]==True:
                    self.Info_Line.setText('Scripts and custom download folder opened')
                else:
                    self.Info_Line.setText('Scripts and SteamCMD download folder opened')
        except FileNotFoundError:
            self.InfoReset()
            if self.data["cdf"]==True:
                self.Info_Line.setText('Custom downloads folder was modified and is not found (2)')
                try:
                    self.Info_Button.disconnect()
                except:
                    pass
                self.Info_Button.clicked.connect(lambda:self.EnableButtons())
                self.Info_Button.clicked.connect(lambda:self.ES())
                self.Info_Button.clicked.connect(lambda:self.ESTab.setCurrentIndex(1))
                self.Info_Button.clicked.connect(lambda:self.ESTab_SCMDWD_subtab.setCurrentIndex(2))
                self.Info_Button.clicked.connect(lambda:self.ESTab_SCMDLM_subtab.setCurrentIndex(0))
                self.InfoError()
            else:
                self.Info_Line.setText('SteamCMD folder was modified and downloads folder is not found (2)')
                try:
                    self.Info_Button.disconnect()
                except:
                    pass
                self.Info_Button.clicked.connect(lambda:self.EnableButtons())
                self.Info_Button.clicked.connect(lambda:self.ES())
                self.Info_Button.clicked.connect(lambda:self.ESTab.setCurrentIndex(1))
                self.Info_Button.clicked.connect(lambda:self.ESTab_SCMDWD_subtab.setCurrentIndex(2))
                self.Info_Button.clicked.connect(lambda:self.ESTab_SCMDLM_subtab.setCurrentIndex(0))
                self.InfoError()
            self.EXCEC_Activator()
            self.OPENFOLDER_Activator()
    def SaveList(self):
        self.InfoReset()
        datatimenow=str(datetime.datetime.now()).replace(':','-').split(".")
        self.PreScript()
        if not self.linksfixedlist:
            self.Info_Line.setText(f'There are not valid links to save (3)')
            try:
                self.Info_Button.disconnect()
            except:
                pass
            self.Info_Button.clicked.connect(lambda:self.EnableButtons())
            self.Info_Button.clicked.connect(lambda:self.ES())
            self.Info_Button.clicked.connect(lambda:self.ESTab.setCurrentIndex(1))
            self.Info_Button.clicked.connect(lambda:self.ESTab_SCMDWD_subtab.setCurrentIndex(3))
            self.Info_Button.clicked.connect(lambda:self.ESTab_SCMDLM_subtab.setCurrentIndex(0))
            self.InfoError()
        else:
            with open(f'./download lists/download list {datatimenow[0]}.scmdwddl','w') as s:
                s.write(str(self.linksfixedlist))
            self.Info_Line.setText(f'Download list saved as: download list {datatimenow[0]}')
        self.ScriptCleaner()
    def LoadList(self):
        try:
            loadlist=QFileDialog.getOpenFileName(self,'Select steamcmd.exe','','Download list file (*.scmdwddl)')
            if loadlist:
                with open(f'{loadlist[0]}','r') as s:
                    self.Workshop_Plain.setPlainText(str(s.read()).replace(',','\n').replace('[','').replace(']','').replace("'",''))
                self.InfoReset()
                self.Info_Line.setText(f"Loaded {(str(re.sub(r'^.*?download list', loadlist[0]))).replace('s/','').replace('.scmdwddl','')}")
        except:
            pass
    def RANP(self):
        if self.User_Line.text()!='' and self.Password_Line.text()!='' and self.RANP_CheckBox.isChecked()==True:
            self.data['account']=self.User_Line.text()
            self.data['password']=self.Password_Line.text()
        else:
            self.data['account']=''
            self.data['password']=''
        self.SaveData()
    def SaveData(self):
        if os.path.exists(((str(self.SteamCMD_Line.text())).replace('/steamcmd.exe',''))+'\\steamcmd.exe')==False:
            self.data['steamcmd']=''
        self.data['dfolder']=self.configDownloadFolder_Line.text()
        self.data['cdf']=self.configCDF_CheckBox.isChecked()
        self.data['bscim']=self.configBSCIM_CheckBox.isChecked()
        self.data['repeat']=int(self.configRepeat_Line.text())
        self.data['dlp']=self.configDLP_CheckBox.isChecked()
        self.data['ranp']=self.RANP_CheckBox.isChecked()
        self.data['mode']=self.Mode_ComboBox.currentIndex()
        with open('./data/data.json','w') as f:
            json.dump(self.data,f)
    def Pin(self):
        if self.Pin_CheckBox.isChecked()==True:
            self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint) |  Qt.WindowStaysOnTopHint)
            self.show()
        elif self.Pin_CheckBox.isChecked()==False:
            self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint))
            self.show()
    def Close(self):
        self.SaveData()
        self.close()
    def IDManager(self):
        wlen=self.Workshop_Plain.toPlainText().replace(' ','\n').split('\n')
        if self.Workshop_Plain.toPlainText():
            if int(self.dLink.text())==len(wlen):
                self.dIncrease.setStyleSheet(self.dIncrease_Properties)
                self.dIncrease.setDisabled(True)
            elif self.data['dlp']==True:
                if self.dIncrease.isCheckable()==False:
                    self.dIncrease.setStyleSheet(self.Increase_Properties)
                    self.dIncrease.setDisabled(False)
            
            if int(self.dLink.text())==0:
                self.dDecrease.setStyleSheet(self.dDecrease_Properties)
                self.dDecrease.setDisabled(True)
            elif self.data['dlp']==True:
                if self.dDecrease.isCheckable()==False:
                    self.dDecrease.setStyleSheet(self.Decrease_Properties)
                    self.dDecrease.setDisabled(False)
        else:
            self.dDecrease.setDisabled(True)
            self.dDecrease.setStyleSheet(self.dDecrease_Properties)
            self.dIncrease.setStyleSheet(self.dIncrease_Properties)
            self.dIncrease.setDisabled(True)
    def Increase(self):
        dLink=int(self.dLink.text())
        self.dLink.setText(str(dLink+1))
    def Decrease(self):
        dLink=int(self.dLink.text())
        self.dLink.setText(str(dLink-1))
    def getData_login(self):
        if self.data['dlp']==True:
            try:
                self.wdict.clear()
            except:
                pass
            self.dPixmap.load('./resources/loading.png')
            self.dPixmap = self.dPixmap.scaled(193,134)
            self.dLabel.setPixmap(self.dPixmap)
            self.dFrame.setStyleSheet('QFrame{border:None;background-color:rgb('+f'{self.t[0]},{self.t[1]},{self.t[2]}'+');}')
            self.dTextGame.setText('Loading...')
            self.dTextListed.setText('')
            self.dTextName.setText('')
            thread=Thread(target=self.numLink_fix)
            thread.start()
    def getData_workshop(self):
        if self.data['dlp']==True:
            try:
                self.wdict.clear()
            except:
                pass
            self.dPixmap.load('./resources/loading.png')
            self.dPixmap = self.dPixmap.scaled(193,134)
            self.dLabel.setPixmap(self.dPixmap)
            self.dFrame.setStyleSheet('QFrame{border:None;background-color:rgb('+f'{self.t[0]},{self.t[1]},{self.t[2]}'+');}')
            self.dTextGame.setText('Loading...')
            self.dTextListed.setText('')
            self.dTextName.setText('')
            thread=Thread(target=self.numLink_change)
            thread.start()
    def getData_link(self):
        if self.data['dlp']==True:
            try:
                self.wdict.clear()
            except:
                pass
            if self.Workshop_Plain.toPlainText():
                self.dPixmap.load('./resources/loading.png')
                self.dPixmap = self.dPixmap.scaled(193,134)
                self.dLabel.setPixmap(self.dPixmap)
                self.dFrame.setStyleSheet('QFrame{border:None;background-color:rgb('+f'{self.t[0]},{self.t[1]},{self.t[2]}'+');}')
                self.dTextGame.setText('Loading...')
                self.dTextListed.setText('')
                self.dTextName.setText('')
                thread=Thread(target=self.numLink_fix)
                thread.start()
            else:
                self.dLink.setText('0')
                self.wdict['isZero']=True
                self.excecuteChanges()
    def numLink_change(self):
        wlen=self.Workshop_Plain.toPlainText().replace(' ','\n').split('\n')
        self.dLink.setText(str(len(wlen)))
        self.numLink_fix()
    def numLink_fix(self):
        self.Info_Line.setText("")
        wlen=self.Workshop_Plain.toPlainText().replace(' ','\n').split('\n')
        if self.dLink.text():
            if int(self.dLink.text())>len(wlen):
                self.dLink.setText(str(len(wlen)))
            if int(self.dLink.text())<0:
                self.dLink.setText('0')
        else:
            self.dLink.setText('0')
        self.wdict={}
        if int(self.dLink.text())!=0:
            self.wdict['isZero']=False
            self.wdict['Index']=int(self.dLink.text())
            self.isValid()
        else:
            self.wdict['isZero']=True
            self.preExcecution()
    def isValid(self):
        wlen=self.Workshop_Plain.toPlainText().replace(' ','\n').split('\n')
        if self.itemcondition in wlen[int(self.dLink.text())-1]:
            self.wdict['isValid']=True
            threadName=Thread(target=self.getName)
            threadImage=Thread(target=self.getImage)
            threadName.start()
            threadImage.start()
            self.getGame()
        else:
            
            self.wdict['isValid']=False
            self.preExcecution()
    def getName(self):
        try:
            wlen=self.Workshop_Plain.toPlainText().replace(' ','\n').split('\n')
            self.wdict['Name']=(str(BeautifulSoup(requests.get(wlen[int(self.dLink.text())-1]).text, 'html.parser').find_all('title')).replace('[<title>Steam Workshop::','').replace('</title>]',''))
        except:
            pass
        
    def getImage(self):
        try:
            wlen=self.Workshop_Plain.toPlainText().replace(' ','\n').split('\n')
            wlen=wlen[int(self.dLink.text())-1]
        except:
            pass
        try:
            for img in BeautifulSoup(urllib.request.urlopen(wlen),features="lxml").findAll('img'):
                if 'https://steamuserimages-a.akamaihd.net/ugc/' in str(img.get('src')):
                    urllib.request.urlretrieve(str(img.get('src')),'./resources/preview.png')
                    break
        except:
            try:
                for img in BeautifulSoup(urllib.request.urlopen(wlen),features="lxml").find_all("img", src=re.compile('phd\d+\.gif$')):
                    if 'https://steamuserimages-a.akamaihd.net/ugc/' in str(img.get('src')):
                        urllib.request.urlretrieve(str(img.get('src')),'./resources/preview.png')
                        break
            except:
                pass
        
    def getGame(self):
            
            try:
                wlen=self.Workshop_Plain.toPlainText().replace(' ','\n').split('\n')
                wlen=wlen[int(self.dLink.text())-1]
            except:
                pass
            try:
                for link in BeautifulSoup(requests.get(wlen).text, 'html.parser').find_all('a'):
                    if self.appcondition in str(link.get('href')):
                        if re.findall('\d+',str(link.get('href')))[0] in self.list:
                            self.wdict['isListed']=True
                        else:
                            self.wdict['isListed']=False
                        self.wdict['Game']=(str(BeautifulSoup(requests.get(str(link.get('href'))).text, 'html.parser').find_all('title')).replace('[<title>Steam Community :: ','').replace('</title>]',''))
                        break
            except:
                pass
            
            self.preExcecution()
    def preExcecution(self):
        try:
            self.thread=ThreadClass(parent=self)
            self.thread.start()
            self.thread.startSignal.connect(self.excecuteChanges)
        except:
            pass
                
    def excecuteChanges(self):
        try:
            
            if self.wdict['isZero']==True or self.Workshop_Plain.toPlainText()=='':
                self.dLink.setText('0')
                self.dPixmap.load('./resources/berdyalexei.png')
                self.dPixmap = self.dPixmap.scaled(193,134)
                self.dLabel.setPixmap(self.dPixmap)
                self.dTextGame.setText('Made by Berdy Alexei')
                self.dTextListed.setText('')
                self.dTextName.setText('')
                self.dFrame.setStyleSheet('QFrame{border:None;background-color:rgb('+f'{self.t[0]},{self.t[1]},{self.t[2]}'+');}')
            if self.wdict['isValid']==True:
                
                if str(self.wdict['Index'])==self.dLink.text() or self.dLink.text()==0:
                    try:
                        self.dTextName.setText(self.wdict['Name'])
                        if '[<title>Steam Community :: Error' in self.dTextName.text() or '[<title>Steam Community :: Screenshot' in self.dTextName.text():
                            self.dPixmap.load('./resources/400.png')
                            self.dPixmap = self.dPixmap.scaled(193,134)
                            self.dLabel.setPixmap(self.dPixmap)
                            self.dTextName.setText('')
                            self.dFrame.setStyleSheet('QFrame{border:None;background-color:rgb('+f'{self.r[0]},{self.r[1]},{self.r[2]}'+');}')
                            self.dTextGame.setText('Wrong link')
                        else:
                            self.dPixmap.load('./resources/preview.png')
                            self.dPixmap = self.dPixmap.scaled(193,134)
                            self.dLabel.setPixmap(self.dPixmap)
                            self.dTextGame.setText(self.wdict['Game'])
                            if self.wdict['isListed']==True:
                                
                                self.dTextListed.setText('Listed')
                                self.dFrame.setStyleSheet('QFrame{border:None;background-color:rgb('+f'{self.a[0]},{self.a[1]},{self.a[2]}'+');}')
                            else:
                                self.dTextListed.setText('Unlisted')
                                self.Info_Line.setText("This item cannot be downloaded without purchase the game (4)")
                                try:
                                    self.Info_Button.disconnect()
                                except:
                                    pass
                                self.Info_Button.clicked.connect(lambda:self.EnableButtons())
                                self.Info_Button.clicked.connect(lambda:self.ES())
                                self.Info_Button.clicked.connect(lambda:self.ESTab.setCurrentIndex(1))
                                self.Info_Button.clicked.connect(lambda:self.ESTab_SCMDWD_subtab.setCurrentIndex(4))
                                self.Info_Button.clicked.connect(lambda:self.ESTab_SCMDLM_subtab.setCurrentIndex(0))
                                self.InfoError()
                                if self.DownloadInfo_Label.text()=='Anonymous':
                                    self.dFrame.setStyleSheet('QFrame{border:None;background-color:rgb('+f'{self.r[0]},{self.r[1]},{self.r[2]}'+');}')
                                else:
                                    self.dFrame.setStyleSheet('QFrame{border:None;background-color:rgb('+f'{self.d[0]},{self.d[1]},{self.d[2]}'+');}')
                    except:
                        self.getData_link()
                else:
                    pass
            elif self.wdict['isValid']=='Closed':
                pass
            else:
                self.dPixmap.load('./resources/404.png')
                self.dPixmap = self.dPixmap.scaled(193,134)
                self.dLabel.setPixmap(self.dPixmap)
                self.dTextName.setText('')
                self.dTextGame.setText('There are no valid links here')
                self.dTextListed.setText('')
        except:
            pass
    def mousePressEvent(self, event):
        CursorPosition=re.findall('\d+',str(QtGui.QCursor().pos()))
        WindowPosition=re.findall('\d+',str(self.pos()))
        self.rel_x=int(CursorPosition[1])-int(WindowPosition[1])
        self.rel_y=int(CursorPosition[2])-int(WindowPosition[2])
        if self.rel_x<743 and self.rel_y<32:
            self.oldPos = event.globalPos()
        else:
            pass
    def mouseMoveEvent(self, event):
        try:
            if self.rel_x<743 and self.rel_y<32:
                delta = QPoint(event.globalPos() - self.oldPos)
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.oldPos = event.globalPos()
            else:
                pass
        except AttributeError:
            pass
class ThreadClass(QtCore.QThread):
	startSignal=QtCore.pyqtSignal(bool)
	def __init__(self, parent=None):
		super(ThreadClass, self).__init__(parent)
	def run(self):
		self.startSignal.emit(True)
if __name__=='__main__':
    Palette=QPalette()
    Palette.setColor(QPalette.Highlight, QColor('#235FCF'))
    Palette.setColor(QPalette.Text,QColor(50,53,60))
    Aplication=QtWidgets.QApplication([])
    Aplication.setPalette(Palette)
    MainWindow=scmdwd()
    MainWindow.show()
    Aplication.exec_()