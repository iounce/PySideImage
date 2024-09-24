# -*- coding: utf-8 -*-

import qtawesome as qta
from PySide6.QtCore import QSize


# generate icons from qtawesome library
class LogoIcon:
    @staticmethod
    def get_icon():
        return qta.icon("mdi6.image-multiple-outline", color="#2979ff")

    @staticmethod
    def get_pixmap(size=QSize(24, 24)):
        return LogoIcon.get_icon().pixmap(size)

    @staticmethod
    def get_logo(size):
        return qta.icon("mdi6.image-multiple-outline").pixmap(size)


class MenuIcon:
    @staticmethod
    def get_close():
        return qta.icon("mdi.close")

    @staticmethod
    def get_min():
        return qta.icon("mdi.minus")

    @staticmethod
    def get_max():
        return qta.icon("mdi.window-maximize")

    @staticmethod
    def get_restore():
        return qta.icon("mdi.window-restore")

    @staticmethod
    def get_more():
        return qta.icon("ri.more-2-fill")

    @staticmethod
    def get_theme():
        return qta.icon("msc.symbol-color")

    @staticmethod
    def get_language():
        return qta.icon("ri.global-line")

    @staticmethod
    def get_chinese():
        return qta.icon("ri.emphasis-cn")

    @staticmethod
    def get_english():
        return qta.icon("ri.emphasis")

    @staticmethod
    def get_feedback():
        return qta.icon("ri.feedback-line")

    @staticmethod
    def get_about():
        return qta.icon("mdi6.information-outline")

    @staticmethod
    def get_open_file():
        return qta.icon("mdi6.file-image", color="#a1887f")

    @staticmethod
    def get_remove_file():
        return qta.icon("mdi6.image-remove", color="#a1887f")

    @staticmethod
    def get_open_setting():
        return qta.icon("ri.settings-5-line", color="#a1887f")


class LabelIcon:
    @staticmethod
    def get_pdf(size):
        return qta.icon("mdi.file-pdf").pixmap(size)

    @staticmethod
    def get_word(size):
        return qta.icon("mdi.file-word").pixmap(size)

    @staticmethod
    def get_excel(size):
        return qta.icon("mdi.file-excel").pixmap(size)

    @staticmethod
    def get_ppt(size):
        return qta.icon("mdi.file-powerpoint").pixmap(size)

    @staticmethod
    def get_file(size):
        return qta.icon("mdi.file").pixmap(size)

    @staticmethod
    def get_folder(size):
        return qta.icon("mdi.folder-open-outline").pixmap(size)

    @staticmethod
    def get_close(size):
        return qta.icon("mdi.close").pixmap(size)

    @staticmethod
    def get_add(size):
        return qta.icon("ri.add-fill").pixmap(size)
