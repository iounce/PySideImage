# -*- coding: utf-8 -*-

import json
import os
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtGui import QCursor, QAction
from PySide6.QtCore import Qt, QSize, QRect, Signal
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QMenu,
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QWidget,
    QSpacerItem,
)

import qtawesome as qta

from ui_main import Ui_MainWindow
from theme_window import ThemeWindow
from feedback_window import FeedbackWindow
from about_window import AboutWindow
from message_window import MessageWindow
from base_window import BaseWindow

from cursor import CursorDirection
from language import Language
from icon import LogoIcon, MenuIcon
from style import LabelStyle, ButtonStyle, WidgetStyle, MenuStyle
from utils import FileUtils
from widget import WidgetManager

# image type
class ImageType:
    GIF = 1
    Default = 0

# drag type
class DragAction:
    ENTER = "1"
    DROP = "2"

# view image window
class ViewWindow(BaseWindow):
    def __init__(self, parent, file_path):
        super().__init__(parent)

        self.screen = QtGui.QGuiApplication.primaryScreen().geometry()

        self.base_layout = QtWidgets.QHBoxLayout()
        self.widget_main = QtWidgets.QScrollArea()
        self.widget_main.setWidgetResizable(True)
        self.widget_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        ext = os.path.splitext(file_path)[1]
        if ext.lower() == ".gif":
            image_type = ImageType.GIF
            image = QtGui.QMovie(file_path)
            image.start()
            orig_width = image.currentImage().width()
            orig_height = image.currentImage().height()
        else:
            image_type = ImageType.Default
            image = QtGui.QImage(file_path)
            orig_width = image.width()
            orig_height = image.height()

        width = orig_width
        height = orig_height
        s_width = self.screen.width()

        if width > s_width:
            ratio = s_width / width
            height = height * ratio
            width = s_width

        self.lbl_image = QtWidgets.QLabel()
        self.lbl_image.setFixedSize(width, height)
        
        if image_type == ImageType.GIF:
            self.lbl_image.setMovie(image)
        else:
            pixmap = QtGui.QPixmap.fromImage(
                image.scaled(
                    self.lbl_image.size(),
                    aspectMode=Qt.KeepAspectRatio,
                    mode=Qt.SmoothTransformation,
                )
            )
            self.lbl_image.setPixmap(pixmap)

        self.widget_main.setWidget(self.lbl_image)
        self.base_layout.addWidget(self.widget_main)
        self.set_body_layout(self.base_layout)

        self.setStyleSheet("QDialog{border:1px solid; border-color:#4f5b62}")
        self.set_title(
            file_path
            + "  "
            + str(orig_width)
            + "*"
            + str(orig_height)
            + ViewWindow.tr("title_pixel")
        )

        self.init_max()

    # set max
    def init_max(self):
        self.show_max(False)
        self.show_restore(True)
        self.showMaximized()


# setting window
class SettingWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent)

        self.fix_width = 600
        self.fix_height = self.fix_width * 0.618

        self.screen = QtGui.QGuiApplication.primaryScreen().geometry()
        self.column_count = int(self.screen.width() / self.fix_width)

        self.base_layout = QtWidgets.QGridLayout()
        self.base_layout.setSpacing(8)

        row = 1
        column = 0

        width_layout = QtWidgets.QHBoxLayout()
        width_layout.addWidget(
            QtWidgets.QLabel(SettingWindow.tr("title_default_width"))
        )
        self.width_line_edit = QtWidgets.QLineEdit()
        validator = QtGui.QDoubleValidator()
        validator.setRange(100, 2000, 2)
        validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        self.width_line_edit.setValidator(validator)
        self.width_line_edit.setFixedWidth(260)
        self.width_line_edit.setFixedHeight(28)
        self.width_line_edit.setText(str(self.fix_width))
        self.width_line_edit.textChanged.connect(self.on_text_changed)
        width_layout.addWidget(self.width_line_edit)
        self.base_layout.addLayout(width_layout, row, column)
        row += 1

        height_layout = QtWidgets.QHBoxLayout()
        height_layout.addWidget(
            QtWidgets.QLabel(SettingWindow.tr("title_default_height"))
        )
        self.height_line_edit = QtWidgets.QLineEdit()
        self.height_line_edit.setFixedWidth(260)
        self.height_line_edit.setFixedHeight(28)
        self.height_line_edit.setText(str(self.fix_height))
        self.height_line_edit.setReadOnly(True)
        height_layout.addWidget(self.height_line_edit)
        self.base_layout.addLayout(height_layout, row, column)
        row += 1

        column_layout = QtWidgets.QHBoxLayout()
        self.combox = QtWidgets.QComboBox()
        self.combox.addItem(SettingWindow.tr("title_auto_column"))
        self.combox.addItem(SettingWindow.tr("title_fix_column"))
        self.combox.setCurrentIndex(0)
        self.combox.currentIndexChanged.connect(self.on_index_changed)
        column_layout.addWidget(self.combox)
        self.column_line_edit = QtWidgets.QLineEdit()
        validator = QtGui.QIntValidator()
        validator.setRange(1, 20)
        self.column_line_edit.setValidator(validator)
        self.column_line_edit.setFixedWidth(260)
        self.column_line_edit.setFixedHeight(28)
        self.column_line_edit.setText(str(self.column_count))
        column_layout.addWidget(self.column_line_edit)
        self.base_layout.addLayout(column_layout, row, column)
        row += 1

        wid_blank = QtWidgets.QWidget()
        wid_blank.setFixedHeight(16)
        self.base_layout.addWidget(wid_blank, row, column)
        row += 1

        btn_layout = QtWidgets.QHBoxLayout()
        self.btn_ok = QtWidgets.QPushButton()
        self.btn_ok.setText(SettingWindow.tr("title_ok"))
        self.btn_ok.setFixedWidth(80)
        self.btn_ok.clicked.connect(self.on_ok)
        btn_layout.addWidget(self.btn_ok)
        self.btn_cancel = QtWidgets.QPushButton()
        self.btn_cancel.setText(SettingWindow.tr("title_cancel"))
        self.btn_cancel.setFixedWidth(80)
        self.btn_cancel.clicked.connect(self.on_cancel)
        btn_layout.addWidget(self.btn_cancel)
        self.base_layout.addLayout(btn_layout, row, column)

        self.set_body_layout(self.base_layout)

        self.show_min(False)
        self.show_max(False)
        self.show_restore(False)

        self.setStyleSheet("QDialog{border:1px solid; border-color:#4f5b62}")
        self.set_title(SettingWindow.tr("title_setting"))
        self.resize(400, 160)

    # callback when text changed
    def on_text_changed(self, text):
        data = self.get_value(self.width_line_edit)
        if data <= 0:
            return

        print(self.width_line_edit.text(), data)

        self.fix_width = data
        self.fix_height = self.fix_width * 0.618

        self.height_line_edit.setText(str(self.fix_height))

        self.set_column_count()

    # callback when index changed
    def on_index_changed(self, index):
        print(
            "index: ",
            index,
            self.screen.width(),
            self.fix_width,
            self.column_line_edit.text(),
        )
        self.set_column_count()

    # get int value
    def get_value(self, line_edit):
        data = 0

        try:
            data = int(line_edit.text())
        except:
            pass

        return data

    # set column count according to the selection
    def set_column_count(self):
        index = self.combox.currentIndex()
        if index == 0:
            self.column_count = int(self.screen.width() / self.fix_width)

            self.column_line_edit.setText(str(self.column_count))
        if index == 1:
            self.column_count = self.get_value(self.column_line_edit)

    # callback of OK button
    def on_ok(self):
        self.set_column_count()
        self.done(1)

    # callback of Cancel button
    def on_cancel(self):
        self.done(0)


# draggable QLabel
class DragLabel(QtWidgets.QLabel):
    drag_signal = QtCore.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = ""
        self.old_pixmap = None
        self.clipboard = QtGui.QGuiApplication.clipboard()

        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_show_menu)

        self.context_menu = QtWidgets.QMenu(self)
        self.copy_file = self.context_menu.addAction(MainWindow.tr("title_copy"))
        self.copy_file.triggered.connect(self.on_copy_file)

        self.view_file = self.context_menu.addAction(MainWindow.tr("title_image_info"))
        self.view_file.triggered.connect(self.on_view_file)

        self.open_file_folder = self.context_menu.addAction(
            MainWindow.tr("title_open_folder")
        )
        self.open_file_folder.triggered.connect(self.on_open_folder)

    # mouse enter
    def enterEvent(self, event):
        self.btn_close.setVisible(True)
        self.setStyleSheet("QLabel{border:3px solid; border-color:#3d5afe;}")

    # mouse leave
    def leaveEvent(self, event):
        self.btn_close.setVisible(False)
        self.setStyleSheet("QLabel{border:0px solid;}")

    # mouse press
    def mousePressEvent(self, event):
        # allow the context menu to pop up
        if event.button() == Qt.RightButton:
            return
        
        if self.is_gif():
            return

        drag = QtGui.QDrag(self)
        mime_data = QtCore.QMimeData()
        mime_data.setImageData(self.pixmap())
        drag.setMimeData(mime_data)
        drag.exec()

    # start dragging
    def dragEnterEvent(self, event):
        if self.is_gif():
            return
        
        image = event.mimeData().imageData()
        if image is None:
            return

        event.accept()
        print("enter: ", self, id(self), image)

        self.drag_emit(DragAction.ENTER)

    # end dragging
    def dropEvent(self, event):
        if self.is_gif():
            return
        
        image = event.mimeData().imageData()
        if image is None:
            return

        self.old_pixmap = self.pixmap()
        self.setPixmap(event.mimeData().imageData())

        self.drag_emit(DragAction.DROP)

    # send signal
    def drag_emit(self, action):
        obj = {}
        obj["id"] = id(self)
        obj["action"] = action
        self.drag_signal.emit(json.dumps(obj))

    # save close buttion
    def set_button(self, btn):
        self.btn_close = btn

    # save file path
    def set_file_path(self, file_path):
        self.file_path = file_path

    # check gif
    def is_gif(self):
        ext = os.path.splitext(self.file_path)[1]
        if ext.lower() == ".gif":
            return True
        
        return False

    # show context menu
    def on_show_menu(self, pos):
        print("show:", self.sender())
        pos = self.mapToGlobal(pos)
        self.context_menu.move(pos)
        self.context_menu.show()

    # callback when file copied
    def on_copy_file(self):
        if self.is_gif():
            return

        mime_data = QtCore.QMimeData()
        mime_data.setImageData(QtGui.QImage(self.file_path))
        self.clipboard.setMimeData(mime_data)

    # callback when file viewed
    def on_view_file(self):
        dlg = ViewWindow(self, self.file_path)
        dlg.exec()

    # callback when folder opened
    def on_open_folder(self):
        print(self.file_path)
        if len(self.file_path) == 0:
            return

        os.startfile(os.path.split(self.file_path)[0])


# draggable QScrollArea
class DragScrollArea(QtWidgets.QScrollArea):
    drag_signal = QtCore.Signal(str)

    def __init__(self):
        super().__init__()

    # start dragging
    def dragEnterEvent(self, event):
        mime_data = event.mimeData()
        file_name = mime_data.text()
        postfix = os.path.splitext(file_name)[1]
        if postfix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
            event.accept()

        print("enter: ", self, id(self), file_name, postfix)

    # end dragging
    def dropEvent(self, event):
        mime_data = event.mimeData()
        text = mime_data.text()

        file_path = text.split("file:///")[1]
        print("drop: ", self, id(self), file_path)

        self.drag_emit(file_path)

    # send signal
    def drag_emit(self, file_path):
        obj = {}
        obj["id"] = id(self)
        obj["file_path"] = file_path
        self.drag_signal.emit(json.dumps(obj))


# main window
class MainWindow(QMainWindow):
    load_signal = Signal(str)

    def __init__(self, p_theme, p_translator, p_setting):
        super(MainWindow, self).__init__()

        self.theme = p_theme
        self.translator = p_translator
        self.setting = p_setting

        self.cursor_direction = CursorDirection.Default
        self.left_btn_pressed = False
        self.drag_point = 0

        self.cn_menu = None
        self.en_menu = None
        self.open_file_menu = None
        self.remove_file_menu = None
        self.open_setting_menu = None
        self.last_path = os.getcwd()

        self.wid_mng = WidgetManager()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init()

    # initialize the window
    def init(self):
        self.init_window()
        self.init_app_bar()
        self.init_more_menu()
        self.init_language()
        self.init_window_content()
        self.init_hotkey()
        self.init_data()

    # initialize the window style
    def init_window(self):
        self.ui.wid_main.setStyleSheet(WidgetStyle.get_border("wid_main"))
        self.setWindowFlags(
            Qt.Window
            | Qt.FramelessWindowHint
            | Qt.WindowSystemMenuHint
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

    # initialize the window title bar(self-defined logo, title and min/restore/max icons)
    def init_app_bar(self):
        self.ui.lbl_logo.setMinimumSize(QSize(24, 24))
        self.ui.lbl_logo.setMaximumSize(QSize(24, 24))
        self.ui.lbl_logo.setPixmap(LogoIcon.get_pixmap())
        self.ui.lbl_logo.setScaledContents(True)

        self.ui.btn_max.setVisible(True)
        self.ui.btn_restore.setVisible(False)

        self.ui.btn_more.setFlat(True)
        self.ui.btn_min.setFlat(True)
        self.ui.btn_close.setFlat(True)
        self.ui.btn_max.setFlat(True)
        self.ui.btn_restore.setFlat(True)

        self.ui.btn_more.setIcon(MenuIcon.get_more())
        self.ui.btn_min.setIcon(MenuIcon.get_min())
        self.ui.btn_close.setIcon(MenuIcon.get_close())
        self.ui.btn_max.setIcon(MenuIcon.get_max())
        self.ui.btn_restore.setIcon(MenuIcon.get_restore())

        self.ui.btn_more.setIconSize(QSize(24, 24))
        self.ui.btn_min.setIconSize(QSize(24, 24))
        self.ui.btn_close.setIconSize(QSize(24, 24))
        self.ui.btn_max.setIconSize(QSize(24, 24))
        self.ui.btn_restore.setIconSize(QSize(24, 24))

        self.ui.btn_close.setStyleSheet(ButtonStyle.get_close())

        self.ui.btn_min.clicked.connect(self.on_min)
        self.ui.btn_close.clicked.connect(self.on_exit)
        self.ui.btn_max.clicked.connect(self.on_max)
        self.ui.btn_restore.clicked.connect(self.on_restore)

        self.ui.lbl_title.setStyleSheet(LabelStyle.get_title())

    # initialize the other menu(theme, language, feedback and about)
    def init_more_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet(MenuStyle.get_more())

        action = QAction(MainWindow.tr("menu_theme"), self)
        action.setIcon(MenuIcon.get_theme())
        action.triggered.connect(self.on_show_theme)
        menu.addAction(action)
        self.wid_mng.add(action, text="menu_theme")

        languageMenu = QMenu(MainWindow.tr("menu_language"))
        languageMenu.setIcon(MenuIcon.get_language())
        menu.addMenu(languageMenu)
        self.wid_mng.add(languageMenu, text="menu_language")

        action = QAction(MainWindow.tr("menu_chinese"), languageMenu)
        action.setCheckable(True)
        action.setChecked(True)
        action.triggered.connect(self.on_show_chinese)
        languageMenu.addAction(action)
        self.cn_menu = action
        self.wid_mng.add(action, text="menu_chinese")

        action = QAction(MainWindow.tr("menu_english"), languageMenu)
        action.setCheckable(True)
        action.setChecked(False)
        action.triggered.connect(self.on_show_english)
        languageMenu.addAction(action)
        self.en_menu = action
        self.wid_mng.add(action, text="menu_english")

        action = QAction(MainWindow.tr("menu_feedback"), self)
        action.setIcon(MenuIcon.get_feedback())
        action.triggered.connect(self.on_show_feedback)
        menu.addAction(action)
        self.wid_mng.add(action, text="menu_feedback")

        action = QAction(MainWindow.tr("menu_about"), self)
        action.setIcon(MenuIcon.get_about())
        action.triggered.connect(self.on_show_about)
        menu.addAction(action)
        self.wid_mng.add(action, text="menu_about")

        self.ui.btn_more.setMenu(menu)
        self.ui.btn_more.setStyleSheet(ButtonStyle.get_more())

    # initialize the default language
    def init_language(self):
        if self.setting.get_language() == Language.Chinese.value:
            self.cn_menu.setChecked(True)
            self.en_menu.setChecked(False)
        else:
            self.en_menu.setChecked(True)
            self.cn_menu.setChecked(False)

    # initialize the main window
    def init_window_content(self):
        self.horizontalLayoutTop = QVBoxLayout(self.ui.widget_body)
        self.toolWidget = QWidget()
        self.toolWidget.setFixedHeight(24)
        self.toolWidget.setContentsMargins(0, 0, 0, 0)

        toolLayout = QHBoxLayout()
        toolLayout.setContentsMargins(0, 0, 0, 0)

        btn_open_file = QPushButton()
        btn_open_file.setFixedSize(QSize(24, 24))
        btn_open_file.setFlat(True)
        btn_open_file.setIcon(MenuIcon.get_open_file())
        btn_open_file.setIconSize(QSize(24, 24))
        btn_open_file.setToolTip(MainWindow.tr("menu_open_file"))
        btn_open_file.clicked.connect(self.on_open_file)
        self.open_file_menu = btn_open_file
        toolLayout.addWidget(btn_open_file)

        btn_remove_file = QPushButton()
        btn_remove_file.setFixedSize(QSize(24, 24))
        btn_remove_file.setFlat(True)
        btn_remove_file.setIcon(MenuIcon.get_remove_file())
        btn_remove_file.setIconSize(QSize(24, 24))
        btn_remove_file.setToolTip(MainWindow.tr("menu_remove_file"))
        btn_remove_file.clicked.connect(self.on_remove_file)
        self.remove_file_menu = btn_remove_file
        toolLayout.addWidget(btn_remove_file)

        btn_open_setting = QPushButton()
        btn_open_setting.setFixedSize(QSize(24, 24))
        btn_open_setting.setFlat(True)
        btn_open_setting.setIcon(MenuIcon.get_open_setting())
        btn_open_setting.setIconSize(QSize(24, 24))
        btn_open_setting.setToolTip(MainWindow.tr("menu_open_setting"))
        btn_open_setting.clicked.connect(self.on_open_setting)
        self.open_setting_menu = btn_open_setting
        toolLayout.addWidget(btn_open_setting)

        blank_widget = QSpacerItem(
            self.width(), 24, QSizePolicy.Expanding, QSizePolicy.Minimum
        )
        toolLayout.addItem(blank_widget)

        self.toolWidget.setLayout(toolLayout)
        self.horizontalLayoutTop.addWidget(self.toolWidget)

        self.widget_main = DragScrollArea()
        self.widget_main.setWidgetResizable(True)
        self.widget_main.setMouseTracking(True)
        self.widget_main.setAcceptDrops(True)
        self.widget_main.drag_signal.connect(self.on_drag_image)

        self.widget_base = QtWidgets.QWidget()

        self.body_layout = QtWidgets.QGridLayout(self.widget_base)
        self.body_layout.setSpacing(8)

        self.widget_main.setWidget(self.widget_base)
        self.horizontalLayoutTop.addWidget(self.widget_main)

        self.setMinimumSize(800, 450)
        self.show_max()

    # initialize the hotkey
    def init_hotkey(self):
        self.clipboard = QtGui.QGuiApplication.clipboard()

        self.key_exit = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self)
        self.key_exit.activated.connect(self.close)

        self.key_open = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+O"), self)
        self.key_open.activated.connect(self.on_open_file)

        self.key_clear = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+E"), self)
        self.key_clear.activated.connect(self.clear_layout)

        self.key_set = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+T"), self)
        self.key_set.activated.connect(self.on_open_setting)

        self.key_paste = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+V"), self)
        self.key_paste.activated.connect(self.on_paste_image)

    # initialize common data
    def init_data(self):
        self.screen = QtGui.QGuiApplication.primaryScreen().geometry()

        self.fix_width = 600
        self.fix_height = self.fix_width * 0.618
        self.images = []
        self.row = 1
        self.column = 0
        self.column_count = int(self.screen.width() / self.fix_width)

        self.labels = {}
        self.btn_labels = {}
        self.drag_labels = []
        self.image_labels = {}
        self.last_path = os.getcwd()

    # show max window
    def show_max(self):
        self.ui.btn_max.setVisible(False)
        self.ui.btn_restore.setVisible(True)
        self.showMaximized()

    # add image
    # image: QImage/QMovie
    # file_path: image path
    def add_image(self, image, image_type, file_path):
        #print(image.width(), image.height())
        orig_width = 0
        orig_height = 0

        if image_type == ImageType.GIF:
            print("Add:", file_path, image_type, image.currentImage())
            orig_width = image.currentImage().width()
            orig_height = image.currentImage().height()
        else:
            orig_width = image.width()
            orig_height = image.height()

        width = self.fix_width
        height = self.fix_height

        print("Add:", file_path, image_type, orig_width, orig_height)

        if orig_height > orig_width:
            width = self.fix_height
            height = self.fix_width

        label = DragLabel(self)
        label.setMouseTracking(True)
        label.setFixedSize(width, height)
        label.setAcceptDrops(True)
        
        if image_type == ImageType.GIF:
            label.setMovie(image)
        else:
            pixmap = QtGui.QPixmap.fromImage(
                image.scaled(
                    label.size(),
                    aspectMode=Qt.IgnoreAspectRatio,
                    mode=Qt.SmoothTransformation,
                )
            )
            label.setPixmap(pixmap)
        label.setScaledContents(True)
        label.setMouseTracking(True)
        label.drag_signal.connect(self.on_change_image)

        btn = QtWidgets.QPushButton(label)
        btn.setIcon(qta.icon("mdi.close", color="#fafafa"))
        btn.setStyleSheet(
            "QPushButton{background-color:red; border: 1px solid red; border-radius: 0px;}"
        )
        btn.setIconSize(QSize(24, 24))
        btn.setFixedSize(QSize(32, 32))
        btn.setToolTip(MainWindow.tr("title_remove_image"))
        btn.move(label.width() - 35, 3)
        btn.setVisible(False)
        btn.clicked.connect(self.on_close_image)

        label.set_button(btn)
        label.set_file_path(file_path)

        self.labels[id(label)] = label
        self.btn_labels[id(btn)] = label
        self.image_labels[id(label)] = file_path

        self.body_layout.addWidget(label, self.row, self.column)

        self.column += 1

        if self.column % self.column_count == 0:
            self.row += 1
            self.column = 0

        self.images.append(label)

    # callback when image changed
    def on_change_image(self, msg):
        obj = json.loads(msg)
        img_id = obj["id"]
        action = obj["action"]

        print("on_change_image:", msg)

        if action == DragAction.ENTER:
            label = self.labels[img_id]
            self.drag_labels.append(label)
        if action == DragAction.DROP:
            label = self.labels[img_id]
            if len(self.drag_labels) < 2:
                return

            self.drag_labels.remove(label)
            orig_label = self.drag_labels[0]
            orig_label.setPixmap(label.old_pixmap)

            file_path = label.file_path
            orig_path = orig_label.file_path

            orig_label.set_file_path(file_path)
            label.set_file_path(orig_path)

            self.drag_labels = []

    # callback when image dragged
    def on_drag_image(self, msg):
        obj = json.loads(msg)
        id = obj["id"]
        file_path = obj["file_path"]
        print("on_drag_image:", msg)
        
        ext = os.path.splitext(file_path)[1]
        if ext.lower() == ".gif":
            image_type = ImageType.GIF
            image = QtGui.QMovie(file_path)
            image.start()
        else:
            image_type = ImageType.Default
            image = QtGui.QImage(file_path)
                
        self.add_image(image, image_type, file_path)

    # callback when image closed
    def on_close_image(self):
        btn = self.sender()
        label = self.btn_labels.get(id(btn))

        btn.setParent(None)
        label.setParent(None)

        self.body_layout.removeWidget(label)
        self.body_layout.update()

        label.deleteLater()
        btn.deleteLater()

        self.refresh_layout()

    # callback of open file button
    def on_open_file(self):
        result = QtWidgets.QFileDialog.getOpenFileNames(
            self, MainWindow.tr("title_choose_image"), self.last_path, "*.*"
        )
        print(result)
        file_paths = result[0]
        if len(file_paths) == 0:
            return

        self.last_path = os.path.split(file_paths[0])[0]
        # print("end:", self.last_path)

        for file_path in file_paths:
            ext = os.path.splitext(file_path)[1]
            if ext.lower() == ".gif":
                image_type = ImageType.GIF
                image = QtGui.QMovie(file_path)
                image.start()
            else:
                image_type = ImageType.Default
                image = QtGui.QImage(file_path)
                
            print("Open:", file_path, image_type, image)
            self.add_image(image, image_type, file_path)

    # callback when image removed
    def on_remove_file(self):
        self.clear_layout()

    # callback when setting
    def on_open_setting(self):
        dlg = SettingWindow(self)
        dlg.exec()
        if dlg.result() != 1:
            return

        self.fix_width = dlg.fix_width
        self.fix_height = dlg.fix_height
        self.column_count = dlg.column_count

        self.refresh_layout()

        print("setting:", self.fix_width, self.fix_height, self.column_count)

    # callback when image pasted
    def on_paste_image(self):
        mime_data = self.clipboard.mimeData()
        if mime_data:
            if mime_data.hasImage():
                image = QtGui.QImage(mime_data.imageData())
                self.add_image(image, ImageType.Default, None)

    # clear current layout
    def clear_layout(self):
        print("clear: ", self.body_layout.rowCount(), self.body_layout.columnCount())
        for row in range(1, self.body_layout.rowCount() + 1):
            for column in range(self.body_layout.columnCount()):
                item = self.body_layout.itemAtPosition(row, column)
                print("clear: ", item, id(item))
                if item is None:
                    continue

                label = item.widget()

                self.body_layout.removeItem(item)

                if label:
                    btn = label.btn_close
                    btn.deleteLater()
                    label.deleteLater()

        self.body_layout.update()

        self.row = 1
        self.column = 0

    # refresh current layout
    def refresh_layout(self):
        print("refresh: ", self.body_layout.rowCount(), self.body_layout.columnCount())

        widgets = []

        for row in range(1, self.body_layout.rowCount() + 1):
            for column in range(self.body_layout.columnCount()):
                item = self.body_layout.itemAtPosition(row, column)

                if item is None:
                    continue

                widgets.append(item.widget())
                self.body_layout.removeItem(item)

        self.row = 1
        self.column = 0

        for widget in widgets:
            width = self.fix_width
            height = self.fix_height

            if widget.height() > widget.width():
                width = self.fix_height
                height = self.fix_width

            widget.setFixedSize(width, height)
            widget.btn_close.move(widget.width() - 35, 3)

            self.body_layout.addWidget(widget, self.row, self.column)

            self.column += 1

            if self.column % self.column_count == 0:
                self.row += 1
                self.column = 0

    # minimize the window
    def on_min(self):
        self.showMinimized()

    # maximize the window
    def on_max(self):
        self.ui.btn_max.setVisible(False)
        self.ui.btn_restore.setVisible(True)
        self.showMaximized()

    # restore the window
    def on_restore(self):
        self.ui.btn_max.setVisible(True)
        self.ui.btn_restore.setVisible(False)
        self.showNormal()

    # exit the application
    def on_exit(self):
        # confirm before exit
        dlg = MessageWindow(
            self,
            self.theme,
            MainWindow.tr("title_exit"),
            MainWindow.tr("tip_exit_message"),
        )
        result = dlg.exec()
        if result != QDialog.DialogCode.Accepted:
            return

        one = QApplication.instance()
        one.quit()

    # update widgets that created dynamically
    # call this function when changing language
    def update_dynamic_widgets(self):
        dynamic_widgets = self.wid_mng.get_all()
        for widget, text in dynamic_widgets.items():
            if isinstance(widget, QMenu):
                widget.setTitle(MainWindow.tr(text))
            else:
                widget.setText(MainWindow.tr(text))

        self.open_file_menu.setToolTip(MainWindow.tr("menu_open_file"))
        self.remove_file_menu.setToolTip(MainWindow.tr("menu_remove_file"))
        self.open_setting_menu.setToolTip(MainWindow.tr("menu_open_setting"))

    # show theme window
    def on_show_theme(self):
        dlg = ThemeWindow(self, self.theme)
        dlg.theme_signal.connect(self.proc_theme_signal)
        dlg.show()

    # response when changing Chinese language
    def on_show_chinese(self):
        cn_checked = self.cn_menu.isChecked()
        en_checked = not cn_checked

        self.cn_menu.setChecked(cn_checked)
        self.en_menu.setChecked(en_checked)

        if cn_checked:
            self.translator.load("zh_CN")
            self.setting.save(Language.Chinese.value, self.theme.get_theme_name())
        else:
            self.translator.load("en_US")
            self.setting.save(Language.English.value, self.theme.get_theme_name())

        self.ui.retranslateUi(self)
        self.update_dynamic_widgets()

    # response when changing English language
    def on_show_english(self):
        en_checked = self.en_menu.isChecked()
        cn_checked = not en_checked

        self.en_menu.setChecked(en_checked)
        self.cn_menu.setChecked(cn_checked)

        if en_checked:
            self.translator.load("en_US")
            self.setting.save(Language.English.value, self.theme.get_theme_name())
        else:
            self.translator.load("zh_CN")
            self.setting.save(Language.Chinese.value, self.theme.get_theme_name())

        self.ui.retranslateUi(self)
        # update the widgets that created dynamically when changing language
        self.update_dynamic_widgets()

    # show feedback window
    def on_show_feedback(self):
        dlg = FeedbackWindow(self, self.theme)
        dlg.show()

    # show about window
    def on_show_about(self):
        dlg = AboutWindow(self, self.theme)
        dlg.show()

    # process the signal of changing theme
    def proc_theme_signal(self, content):
        language = (
            Language.Chinese
            if self.cn_menu and self.cn_menu.isChecked()
            else Language.English
        )
        self.setting.save(language.value, FileUtils.get_name(content))

    # get the cursor direction when dragging the mouse
    def get_cursor_direction(self, global_point):
        padding = 1

        rect = self.rect()
        top_left = self.mapToGlobal(rect.topLeft())
        bottom_right = self.mapToGlobal(rect.bottomRight())

        x = global_point.x()
        y = global_point.y()

        if (
            top_left.x() + padding >= x >= top_left.x()
            and top_left.y() + padding >= y >= top_left.y()
        ):
            self.cursor_direction = CursorDirection.LeftTop
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif (
            bottom_right.x() - padding <= x <= bottom_right.x()
            and bottom_right.y() - padding <= y <= bottom_right.y()
        ):
            self.cursor_direction = CursorDirection.RightBottom
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif (
            top_left.x() + padding >= x >= top_left.x()
            and bottom_right.y() - padding <= y <= bottom_right.y()
        ):
            self.cursor_direction = CursorDirection.LeftBottom
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif (
            bottom_right.x() >= x >= bottom_right.x() - padding
            and top_left.y() <= y <= top_left.y() + padding
        ):
            self.cursor_direction = CursorDirection.RightTop
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif top_left.x() + padding >= x >= top_left.x():
            self.cursor_direction = CursorDirection.Left
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif bottom_right.x() >= x >= bottom_right.x() - padding:
            self.cursor_direction = CursorDirection.Right
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif top_left.y() <= y <= top_left.y() + padding:
            self.cursor_direction = CursorDirection.Up
            self.setCursor(QCursor(Qt.SizeVerCursor))
        elif bottom_right.y() >= y >= bottom_right.y() - padding:
            self.cursor_direction = CursorDirection.Down
            self.setCursor(QCursor(Qt.SizeVerCursor))
        else:
            self.cursor_direction = CursorDirection.Default
            self.setCursor(QCursor(Qt.ArrowCursor))

    # process mouse event when dragging the window
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.left_btn_pressed = True

            if self.cursor_direction != CursorDirection.Default:
                self.mouseGrabber()
            else:
                self.drag_point = e.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        global_point = e.globalPos()
        rect = self.rect()
        top_left = self.mapToGlobal(rect.topLeft())
        bottom_right = self.mapToGlobal(rect.bottomRight())

        if not self.left_btn_pressed:
            self.get_cursor_direction(global_point)
        else:
            if self.cursor_direction != CursorDirection.Default:
                move_rect = QRect(top_left, bottom_right)

                if self.cursor_direction == CursorDirection.Left:
                    if bottom_right.x() - global_point.x() <= self.minimumWidth():
                        move_rect.setX(top_left.x())
                    else:
                        move_rect.setX(global_point.x())
                elif self.cursor_direction == CursorDirection.Right:
                    move_rect.setWidth(global_point.x() - top_left.x())
                elif self.cursor_direction == CursorDirection.Up:
                    if bottom_right.y() - global_point.y() <= self.minimumHeight():
                        move_rect.setY(top_left.y())
                    else:
                        move_rect.setY(global_point.y())
                elif self.cursor_direction == CursorDirection.Down:
                    move_rect.setHeight(global_point.y() - top_left.y())
                elif self.cursor_direction == CursorDirection.LeftTop:
                    if bottom_right.x() - global_point.x() <= self.minimumWidth():
                        move_rect.setX(top_left.x())
                    else:
                        move_rect.setX(global_point.x())

                    if bottom_right.y() - global_point.y() <= self.minimumHeight():
                        move_rect.setY(top_left.y())
                    else:
                        move_rect.setY(global_point.y())
                elif self.cursor_direction == CursorDirection.RightTop:
                    move_rect.setWidth(global_point.x() - top_left.x())
                    move_rect.setY(global_point.y())
                elif self.cursor_direction == CursorDirection.LeftBottom:
                    move_rect.setX(global_point.x())
                    move_rect.setHeight(global_point.y() - top_left.y())
                elif self.cursor_direction == CursorDirection.RightBottom:
                    move_rect.setWidth(global_point.x() - top_left.x())
                    move_rect.setHeight(global_point.y() - top_left.y())
                else:
                    pass

                self.setGeometry(move_rect)
            else:
                self.move(e.globalPos() - self.drag_point)
                e.accept()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.left_btn_pressed = False

            if self.cursor_direction != CursorDirection.Default:
                self.releaseMouse()
                self.setCursor(QCursor(Qt.ArrowCursor))
