import json
import os
import re
import sys
import time
import threading
from PySide2.QtCore import Slot
from PySide2.QtGui import QTextCursor, QIcon, QPixmap
from PySide2.QtWidgets import QApplication, QMainWindow, QLineEdit, QTextEdit,QMessageBox, \
    QPushButton, QLabel, QWidget, \
    QFileDialog, QDesktopWidget
from PySide2.QtCore import Signal, Slot, QDateTime, QTimer, QEventLoop, QCoreApplication, Qt
from main_ui import Ui_water_mainwd
from AdPicEcc import AdPicEcc
import imgs  # pyside2生成的图片资源文件


class UI(QMainWindow, Ui_water_mainwd):
    signal_log = Signal(str, bool, object)
    SUPPORT_TYPE = ('.png', '.jpg', '.gif')

    def __init__(self, *wd, **kw):
        Ui_water_mainwd.__init__(self)
        QMainWindow.__init__(self, parent=None)
        self.setupUi(self)

        icon = QIcon()
        icon.addPixmap(QPixmap(":res/main.ico"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        # self.setWindowIcon(QIcon("res\\main.ico"))

        # 所有tool button统一注册
        for k, item in self.__dict__.items():
            if isinstance(item, QPushButton):
                self.__getattribute__(k).clicked.connect(self.onbtnclicked)
        self.dir_selector_map = {
            self.sel_pic_btn: self.sel_pic_lbl,
            self.sel_ecc_btn: self.sel_ecc_lbl
        }
        self.file_selector_map = {}
        self.file_exec_map = {
            self.sel_auth_btn: self.do_auth
        }

        self.signal_log.connect(self._log_msg)

        # 状态栏
        self._status_lbl = QLabel("未授权")
        self.statusbar.addWidget(self._status_lbl)
        self.change_status_lbl("auth", False)

        # 读取缓存
        self.load_input_set()

        self.sys_info_lbl.setText(AdPicEcc.get_sys_info())
        #
        self.auto_auth()

    def change_status_lbl(self, typ: str, status: bool):
        style = {True: "color: white; background-color:green",
                 False: "color: white; background-color:orange"}
        name = {"auth": self._status_lbl}
        msg = "=={0}==".format("已授权" if status else "未授权")

        name[typ].setText(msg)
        name[typ].setStyleSheet(style[status])

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

    def auto_auth(self):
        if os.path.exists(AdPicEcc.SCRIPT_KEY_PATH):
            key = AdPicEcc().gen_key()
            print(key)
            if key is not None:
                self.change_status_lbl("auth", True)
                return True
            else:
                self.change_status_lbl("auth", False)
                return False
        return False

    def do_auth(self, path):
        if not path:
            return
        print(path)
        if os.path.splitext(path)[-1].lower() == ".py":
            sys_info = self.sys_info_lbl.text()
            aux_info = "to:{0} == from:{1} == time:{2}"\
                .format(sys_info, AdPicEcc.get_sys_info(), time.asctime(time.localtime(time.time())))
            ret = AdPicEcc().gen_private(sys_info, input_path=path,
                                         output_path="{0}.ecc".format(sys_info), aux_info=aux_info)
            if ret:
                self.pop_msg("生成授权成功: {0}".format("{0}.ecc".format(sys_info)))
            else:
                self.pop_msg("生成授权失败: {0}".format(aux_info))
        elif os.path.splitext(path)[-1].lower() == ".ecc":
            try:
                with open(path, 'rb') as f:
                    txt = f.read()
                    with open(AdPicEcc.SCRIPT_KEY_PATH, 'wb') as fw:
                        fw.write(txt)
            except Exception as e:
                self.pop_msg("未知错误: {0}".format(e.__str__()))
            if self.auto_auth():
                self.pop_msg("授权成功!")
            else:
                self.pop_msg("授权失败!请确认当前机器码:{0}是否正确！".format(AdPicEcc.get_sys_info()))
        else:
            self.pop_msg("不支持的文件格式: {0}".format(os.path.split(path)[-1]))

    @Slot()
    def on_enc_btn_clicked(self):
        ip_info = AdPicEcc.get_ip_info()
        aux_info = "{0},dev:{1},time:{2}"\
            .format(ip_info, AdPicEcc.get_sys_info(), time.asctime(time.localtime(time.time())))
        # print(aux_info)

        ad = AdPicEcc()
        src_dir = self.sel_pic_lbl.text()
        dst_dir = self.sel_ecc_lbl.text()
        done = []
        failed = []
        for item in os.listdir(src_dir):
            typ = os.path.splitext(item)[-1].lower()
            # if typ in self.SUPPORT_TYPE:
            if typ and typ != '.enc':
                enc_name = os.path.splitext(item)[0] + '.enc'
                aux_info_per = "{0},id:{1},{2}".format(typ.strip("."), self.sign_lbl.text(), aux_info)
                if ad.enc_pic(src_dir + os.sep + item, dst_dir + os.sep + enc_name, aux_msg=aux_info_per):
                    done.append(item)
                else:
                    failed.append(item)
        self.result_lbl.clear()
        self.pop_msg("加密图片到{0}:成功{1} 失败{2}.".format(dst_dir, done.__len__(), failed.__len__()))
        self.result_lbl.setText("成功:\n{0}\n失败:\n{1}".format("\n".join(done), "\n".join(failed)))
        if self.open_when_fin_btn.isChecked():
            try:
                os.system("explorer \\e,\\root,{0}".format(dst_dir.replace("/", os.sep)))
            except Exception as e:
                print(e)

    @Slot()
    def on_dec_btn_clicked(self):
        ad = AdPicEcc()
        src_dir = self.sel_ecc_lbl.text()
        dst_dir = self.sel_ecc_lbl.text()
        done = []
        failed = []
        for item in os.listdir(src_dir):
            typ = os.path.splitext(item)[-1].lower()
            if typ == ".enc":
                pic_name = os.path.splitext(item)[0] + '.png'
                flag, aux_info = ad.dec_pic(src_dir + os.sep + item, dst_dir + os.sep + pic_name,
                                            has_aux_msg=True)
                typ_name = aux_info.split(",")[0]
                if typ_name and typ_name.__len__() < 20:
                    fin_name = dst_dir + os.sep + pic_name.replace(".png", ".{0}".format(typ_name))
                    if os.path.exists(fin_name) and typ_name != 'png':
                        os.remove(fin_name)
                    os.rename(dst_dir + os.sep + pic_name, fin_name)
                if flag:
                    done.append("{0} {1}".format(item, aux_info))
                else:
                    failed.append("{0} {1}".format(item, aux_info))
        self.result_lbl.clear()
        self.pop_msg("解密图片到{0}:成功{1} 失败{2}.".format(dst_dir, done.__len__(), failed.__len__()))
        self.result_lbl.setText("成功:\n{0}\n失败:\n{1}".format("\n".join(done), "\n".join(failed)))
        if self.open_when_fin_btn.isChecked():
            try:
                os.system("explorer \\e,\\root,{0}".format(dst_dir.replace("/", os.sep)))
            except Exception as e:
                print(e)

    def pop_msg(self, msg):
        QMessageBox.information(self, "提示", msg)

    def closeEvent(self, event):
        print("main window close event")
        self.dump_input_set()
        # os._exit(0)
        sys.exit(0)

    @Slot()
    def onbtnclicked(self):
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

    @staticmethod
    def on_common_file_choice_btn_clicked(obj, file_filter="*.*", sel="file", txt_show=None, callback=None):
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

    def log_msg(self, msg, mv_end=True, replace_pattern=""):
        self.signal_log.emit(msg, mv_end, replace_pattern)

    def _log_msg(self, msg, mv_end=True, replace_pattern=""):
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
            self.result_lbl.setTextCursor(cursor)

    # @Slot()
    # def on_clear_output_btn_clicked(self):
    #     self.result_lbl.clear()


if __name__ == "__main__":
    uiapp = QApplication([])
    a = UI()
    a.show()
    sys.exit(uiapp.exec_())
