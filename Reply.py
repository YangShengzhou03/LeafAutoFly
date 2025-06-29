import json
import openpyxl
from PyQt6 import QtCore, QtWidgets, QtGui
from UI_Reply import Ui_ReplyDialog
from common import get_resource_path, log_print


class ReplyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        log_print("[REPLY_DIALOG] Initializing ReplyDialog")
        self.ui = Ui_ReplyDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("编辑Ai接管规则")
        self.setWindowIcon(QtGui.QIcon(get_resource_path('resources/img/tray.ico')))
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.ui.pushButton_save.clicked.connect(self.saveRulesToJsonAndClose)
        self.ui.pushButton_add.clicked.connect(self.add_rule)
        self.ui.file_pushButton.clicked.connect(self.open_file)
        self.ui.pushButton_cancel.clicked.connect(self.close)
        self.ui.pushButton_load.setText("导入规则")
        self.ui.pushButton_load.clicked.connect(self.import_rules_from_excel)
        self.rules = []
        self.loadRulesFromJson()
        self.displayRules()

    def open_file(self):
        log_print("[REPLY_DIALOG] Opening file dialog")
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*)")
        if file_path:
            self.ui.Reply_lineEdit.setText(file_path)
            log_print(f"[REPLY_DIALOG] File selected: {file_path}")

    def loadRulesFromJson(self):
        log_print("[REPLY_DIALOG] Loading rules from JSON")
        try:
            with open(get_resource_path('_internal/AutoReply_Rules.json'), 'r', encoding='utf-8') as file:
                self.rules = json.load(file)
                log_print(f"[REPLY_DIALOG] Loaded {len(self.rules)} rules from JSON")
        except FileNotFoundError:
            self.rules = []
            log_print("[REPLY_DIALOG] Rules file not found, starting with empty rules")

    def saveRulesToJson(self):
        log_print("[REPLY_DIALOG] Saving rules to JSON")
        try:
            rules = []
            for i in range(self.ui.formLayout.count()):
                widget_item = self.ui.formLayout.itemAt(i).widget()
                if widget_item is not None and isinstance(widget_item, QtWidgets.QWidget):
                    match_type = widget_item.findChild(QtWidgets.QLabel, "label_Rule").text()
                    keyword = widget_item.findChild(QtWidgets.QLabel, "label_KeyWord").text()
                    reply_content = widget_item.findChild(QtWidgets.QLabel, "label_Reply").text()
                    rules.append({
                        "match_type": match_type,
                        "keyword": keyword,
                        "reply_content": reply_content
                    })
            with open('_internal/AutoReply_Rules.json', 'w', encoding='utf-8') as file:
                json.dump(rules, file, ensure_ascii=False, indent=4)
                log_print(f"[REPLY_DIALOG] Saved {len(rules)} rules to JSON")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "保存失败", f"保存出错，{e}")
            log_print(f"[REPLY_DIALOG] Error saving rules: {str(e)}")

    def saveRulesToJsonAndClose(self):
        log_print("[REPLY_DIALOG] Saving rules and closing dialog")
        self.saveRulesToJson()
        self.close()

    def create_frame(self, match_type, keyword, reply_content):
        log_print(f"[REPLY_DIALOG] Creating rule frame: {match_type}, {keyword}, {reply_content}")
        RuleWidget_Item = QtWidgets.QWidget(parent=self.ui.scrollAreaWidgetContents)
        RuleWidget_Item.setMinimumSize(QtCore.QSize(760, 36))
        RuleWidget_Item.setMaximumSize(QtCore.QSize(760, 36))
        RuleWidget_Item.setStyleSheet("border-radius: 6px;\nbackground:rgba(255, 255, 255, 160);")
        RuleWidget_Item.setObjectName("RuleWidget_Item")

        horizontalLayout_18 = QtWidgets.QHBoxLayout(RuleWidget_Item)
        horizontalLayout_18.setContentsMargins(9, 4, 9, 4)
        horizontalLayout_18.setSpacing(6)
        horizontalLayout_18.setObjectName("horizontalLayout_18")

        label_Rule = QtWidgets.QLabel(match_type, parent=RuleWidget_Item)
        label_Rule.setMinimumSize(QtCore.QSize(50, 0))
        label_Rule.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(12)
        label_Rule.setFont(font)
        label_Rule.setStyleSheet("color:rgb(255, 255, 255);\nbackground:rgba(0, 0, 0, 0);")
        label_Rule.setObjectName("label_Rule")
        horizontalLayout_18.addWidget(label_Rule)

        label_KeyWord = QtWidgets.QLabel(keyword, parent=RuleWidget_Item)
        label_KeyWord.setMinimumSize(QtCore.QSize(200, 0))
        label_KeyWord.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(12)
        label_KeyWord.setFont(font)
        label_KeyWord.setStyleSheet("color:rgba(105, 27, 253, 180);\nbackground:rgba(0, 0, 0, 0);")
        label_KeyWord.setObjectName("label_KeyWord")
        horizontalLayout_18.addWidget(label_KeyWord)

        label_21 = QtWidgets.QLabel("回复内容", parent=RuleWidget_Item)
        label_21.setMinimumSize(QtCore.QSize(64, 0))
        label_21.setMaximumSize(QtCore.QSize(64, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(12)
        label_21.setFont(font)
        label_21.setStyleSheet("color:rgb(255, 255, 255);\nbackground:rgba(0, 0, 0, 0);")
        label_21.setObjectName("label_21")
        horizontalLayout_18.addWidget(label_21)

        label_Reply = QtWidgets.QLabel(reply_content, parent=RuleWidget_Item)
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(12)
        label_Reply.setFont(font)
        label_Reply.setStyleSheet("color:rgba(105, 27, 253, 180);\nbackground:rgba(0, 0, 0, 0);")
        label_Reply.setObjectName("label_Reply")
        horizontalLayout_18.addWidget(label_Reply)

        delete_button = QtWidgets.QPushButton("删除", parent=RuleWidget_Item)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 0, 180);
                border: none;
                border-radius: 6px;
                color: white;
                font-size: 12px;
                padding: 2px;
                width: 42px;
                height: 24px;
                min-width: 42px;
                max-width: 42px;
                min-height: 24px;
                max-height: 24px;
                transition: background-color 0.3s ease, transform 0.1s ease;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.9);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: rgba(200, 0, 0, 1);
                transform: scale(0.95);
                box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.5);
            }
        """)
        delete_button.hide()
        delete_button.clicked.connect(lambda: self.remove_rule(RuleWidget_Item))
        horizontalLayout_18.addWidget(delete_button)

        RuleWidget_Item.enterEvent = lambda event: delete_button.show()
        RuleWidget_Item.leaveEvent = lambda event: delete_button.hide()

        return RuleWidget_Item

    def add_rule(self):
        log_print("[REPLY_DIALOG] Add rule button clicked")
        match_type = self.ui.Rule_comboBox.currentText()
        keyword = self.ui.KeyWord_lineEdit.text()
        reply_content = self.ui.Reply_lineEdit.text()

        if keyword == "" or reply_content == "":
            log_print("[REPLY_DIALOG] Add rule failed: Missing required fields")
            QtWidgets.QMessageBox.warning(self, "输入不完整", "您尚未完成所有必填项，请确保输入完整。")
            return

        for rule in self.rules:
            if rule["match_type"] == match_type and rule["keyword"] == keyword and rule[
                "reply_content"] == reply_content:
                log_print("[REPLY_DIALOG] Duplicate rule found")
                QtWidgets.QMessageBox.warning(self, "重复规则", "该规则已存在，请检查后重试。")
                return

        widget_item = self.create_frame(match_type, keyword, reply_content)
        self.ui.formLayout.addRow(widget_item)
        self.rules.append({
            "match_type": match_type,
            "keyword": keyword,
            "reply_content": reply_content
        })
        self.ui.KeyWord_lineEdit.clear()
        self.ui.Reply_lineEdit.clear()

    def remove_rule(self, widget_item):
        log_print("[REPLY_DIALOG] Removing rule widget")
        widget_item.setParent(None)
        widget_item.deleteLater()

    def displayRules(self):
        log_print(f"[REPLY_DIALOG] Displaying {len(self.rules)} rules")
        for rule in self.rules:
            widget_item = self.create_frame(
                rule['match_type'],
                rule['keyword'],
                rule['reply_content']
            )
            self.ui.formLayout.addRow(widget_item)

    def import_rules_from_excel(self):
        log_print("[REPLY_DIALOG] Import rules from Excel button clicked")
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "选择Excel文件", "", "Excel Files (*.xlsx *.xls)"
        )
        if not file_path:
            log_print("[REPLY_DIALOG] No file selected for import")
            return

        try:
            workbook = openpyxl.load_workbook(file_path, read_only=True)
            sheet = workbook.active
            header = list(next(sheet.iter_rows(min_row=1, max_row=1, values_only=True)))

            required_columns = ['匹配类型', '关键词', '回复内容']
            missing_columns = [col for col in required_columns if col not in header]
            if missing_columns:
                log_print(f"[REPLY_DIALOG] Excel file missing required columns: {', '.join(missing_columns)}")
                QtWidgets.QMessageBox.warning(self, "格式错误", f"Excel文件缺少必要的列: {', '.join(missing_columns)}")
                return

            match_type_idx = header.index('匹配类型')
            keyword_idx = header.index('关键词')
            reply_content_idx = header.index('回复内容')

            imported_count = 0
            skipped_count = 0

            for row in sheet.iter_rows(min_row=2, values_only=True):
                if not all(row):
                    continue

                match_type = row[match_type_idx]
                keyword = str(row[keyword_idx]).strip() if row[keyword_idx] is not None else ""
                reply_content = str(row[reply_content_idx]).strip() if row[reply_content_idx] is not None else ""

                if not keyword or not reply_content:
                    skipped_count += 1
                    continue

                valid_match_types = ['包含', '等于']
                if match_type not in valid_match_types:
                    skipped_count += 1
                    continue

                is_duplicate = False
                for rule in self.rules:
                    if (rule["match_type"] == match_type and
                            rule["keyword"] == keyword and
                            rule["reply_content"] == reply_content):
                        is_duplicate = True
                        skipped_count += 1
                        break

                if not is_duplicate:
                    widget_item = self.create_frame(match_type, keyword, reply_content)
                    self.ui.formLayout.addRow(widget_item)
                    self.rules.append({
                        "match_type": match_type,
                        "keyword": keyword,
                        "reply_content": reply_content
                    })
                    imported_count += 1

            workbook.close()

            log_print(f"[REPLY_DIALOG] Successfully imported {imported_count} rules, skipped {skipped_count}")
            QtWidgets.QMessageBox.information(
                self, "导入完成",
                f"成功导入 {imported_count} 条规则\n"
                f"跳过 {skipped_count} 条规则（重复或不完整）"
            )

        except Exception as e:
            log_print(f"[REPLY_DIALOG] Error importing Excel file: {str(e)}")
            QtWidgets.QMessageBox.critical(self, "导入失败", f"导入Excel文件时出错: {str(e)}")
