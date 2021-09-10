import json
import os
import re
import sys

from PySide2.QtCore import Slot
from PySide2.QtGui import QTextCursor
from PySide2.QtWidgets import QApplication, QMainWindow, QLineEdit, QTextEdit, \
    QPushButton, \
    QFileDialog

from main_ui import Ui_water_mainwd


class UI(QMainWindow, Ui_water_mainwd):
    def __init__(self, *wd, **kw):
        Ui_water_mainwd.__init__(self)
        QMainWindow.__init__(self, parent=None)
        self.setupUi(self)
        #  self.setWindowIcon(QIcon("res\\main.ico"))

        # 所有tool button统一注册
        for k, item in self.__dict__.items():
            if isinstance(item, QPushButton):
                self.__getattribute__(k).clicked.connect(self.on_btn_clicked)
        self.dir_selector_map = {}
        self.file_selector_map = {
            self.sel_log_btn: self.sel_log_lbl,
            self.sel_tab_btn: self.sel_tab_lbl
        }
        self.file_exec_map = {
            self.load_setting_btn: self.load_setting,
            self.dump_setting_btn: self.dump_setting
        }

        self.load_input_set()

    def dump_input_set(self):
        dct = {}
        for k, item in self.__dict__.items():
            if isinstance(item, QLineEdit):
                dct[k] = item.text()
            elif isinstance(item, QTextEdit):
                dct[k] = item.toPlainText()
        with open(".ui.dump", "w+", encoding="utf-8") as f:
            f.write(json.dumps(dct, indent=1, ensure_ascii=False))

    def load_input_set(self):
        try:
            with open(".ui.dump", "r", encoding="utf-8") as f:
                dct = json.load(f)
                if dct:
                    for k, v in dct.items():
                        if hasattr(self, k):
                            item = self.__getattribute__(k)
                            if isinstance(item, QLineEdit) or isinstance(item, QTextEdit):
                                item.setText(v)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(e)

    def closeEvent(self, event):
        print("main window close event")
        self.dump_input_set()
        os._exit(0)
        # sys.exit(0)

    @Slot()
    def on_btn_clicked(self):
        obj = self.sender()
        # 文件选择器
        if self.file_selector_map.get(obj, None) is not None:
            return self.on_common_file_choice_btn_clicked(obj, sel="file",
                                                          txt_show=self.file_selector_map.get(obj, None))

        # 文件夹选择器
        elif self.dir_selector_map.get(obj, None) is not None:
            return self.on_common_file_choice_btn_clicked(obj, sel="dir",
                                                          txt_show=self.dir_selector_map.get(obj, None))
        # 文件选择后执行回调
        elif self.file_exec_map.get(obj, None) is not None:
            return self.on_common_file_choice_btn_clicked(obj, sel="file", callback=self.file_exec_map[obj])

    def on_common_file_choice_btn_clicked(self, obj, file_filter="*.*", sel="file", txt_show=None, callback=None):
        if txt_show is not None:
            curpath = txt_show.text()
            curpath = os.path.split(curpath)[0]
            curpath = curpath if curpath else "."
        else:
            curpath = ""
        if "file" == sel:
            # file_name = QFileDialog.getOpenFileName(None, "文件选择", curpath, file_filter)
            file_name = QFileDialog.getOpenFileNames(None, "文件选择", curpath, file_filter)
        else:
            file_name = [QFileDialog.getExistingDirectory(None, "文件选择", curpath)]
        show_text = ""
        if isinstance(file_name, tuple):
            if isinstance(file_name[0], list):
                show_text = "||".join(file_name[0])
            else:
                show_text = file_name[0]
        elif isinstance(file_name, list):
            show_text = file_name[0]
        if txt_show:
            txt_show.setText(show_text)

        if callable(callback):
            for item in show_text.split("||"):
                callback(item)

    def load_setting(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                dct = json.load(f)
                if dct:
                    for k, v in dct.items():
                        if hasattr(self, k):
                            item = self.__getattribute__(k)
                            if isinstance(item, QLineEdit) or isinstance(item, QTextEdit):
                                item.setText(v)
                self.log_msg(u"从:{0} 读取配置成功".format(path))
        except Exception as e:
            self.log_msg(str(e))

    def dump_setting(self, path):
        try:
            with open(path, "w+", encoding="utf-8") as f:
                dct = {}
                for k, item in self.__dict__.items():
                    if isinstance(item, QLineEdit):
                        if k.startswith("item_"):
                            dct[k] = item.text()
                f.write(json.dumps(dct, indent=1, ensure_ascii=False))
                self.log_msg(u"保存配置文件到:{0} 成功".format(path))
        except Exception as e:
            self.log_msg(str(e))

    def log_msg(self, msg, mv_end=False, replace_pattern=""):
        cursor = self.result_lbl.textCursor()
        if replace_pattern:
            ret = []
            found = False
            for item in self.result_lbl.toPlainText().split("\n"):
                if re.search(replace_pattern, item):
                    ret.append(msg)
                    found = True
                else:
                    ret.append(item)
            if not found:
                ret.append(msg)
            self.result_lbl.setText("\n".join(ret))
        else:
            cursor.insertText(msg + "\n")

        if mv_end:
            cursor.movePosition(QTextCursor.End)
            self.cmd_result_lbl.setTextCursor(cursor)


if __name__ == "__main__":
    uiapp = QApplication([])
    a = UI()
    a.show()
    sys.exit(uiapp.exec_())
