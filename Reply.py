import json
import re

import openpyxl
from PyQt6 import QtCore, QtWidgets, QtGui
from UI_Reply import Ui_ReplyDialog
from common import get_resource_path, log_print


class ReplyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        log_print("Entering ReplyDialog initialization")
        super().__init__(parent)
        self.ui = Ui_ReplyDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("编辑Ai接管规则")
        self.setWindowIcon(QtGui.QIcon(get_resource_path('resources/img/tray.ico')))
        self.setWindowFlags(
            self.windowFlags() | QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.ui.pushButton_save.clicked.connect(self.saveRulesToJsonAndClose)
        self.ui.pushButton_add.clicked.connect(self.add_rule)
        self.ui.file_pushButton.clicked.connect(self.open_file)
        self.ui.pushButton_cancel.clicked.connect(self.on_cancel_clicked)
        self.ui.pushButton_load.clicked.connect(self.import_excel_rules)
        self.rules = []
        self.original_rules = []
        self.loadRulesFromJson()
        self.original_rules = self.rules.copy()
        self.displayRules()
        self.ui.Apply_lineEdit.setText("全部")
        log_print("Completed ReplyDialog initialization")

    def open_file(self):
        log_print("Opening file selection dialog")
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*)")
        if file_path:
            self.ui.Reply_lineEdit.setText(file_path)
            log_print(f"Selected file path: {file_path}")

    def loadRulesFromJson(self):
        log_print("Starting to load rules from JSON")
        try:
            with open(get_resource_path('_internal/AutoReply_Rules.json'), 'r', encoding='utf-8') as file:
                self.rules = json.load(file)
                log_print(f"Successfully loaded {len(self.rules)} rules")
        except FileNotFoundError:
            self.rules = []
            log_print("Rule file not found, creating new rule list")

    def saveRulesToJson(self):
        log_print("Starting to save rules to JSON")
        try:
            rules = []
            for i in range(self.ui.formLayout.count()):
                widget_item = self.ui.formLayout.itemAt(i).widget()
                if widget_item is not None and isinstance(widget_item, QtWidgets.QWidget):
                    rules.append({
                        "keyword": widget_item.findChild(QtWidgets.QLabel, "label_KeyWord").text(),
                        "match_type": widget_item.findChild(QtWidgets.QLabel, "label_Rule").text(),
                        "reply_content": widget_item.findChild(QtWidgets.QLabel, "label_Reply").text(),
                        "apply_to": widget_item.findChild(QtWidgets.QLabel, "label_ApplyTo").text()
                    })
            with open(get_resource_path('_internal/AutoReply_Rules.json'), 'w', encoding='utf-8') as file:
                json.dump(rules, file, ensure_ascii=False, indent=4)
            self.original_rules = rules.copy()
            log_print(f"Successfully saved {len(rules)} rules to JSON")
        except Exception as e:
            log_print(f"Error saving rules: {str(e)}")
            QtWidgets.QMessageBox.critical(self, "保存失败", f"保存出错，{e}")

    def saveRulesToJsonAndClose(self):
        log_print("Calling save rules and close dialog")
        self.saveRulesToJson()
        self.close()

    def create_frame(self, keyword, match_type, reply_content, apply_to="全部"):
        log_print("Creating rule display frame")
        RuleWidget_Item = QtWidgets.QWidget(parent=self.ui.scrollAreaWidgetContents)
        RuleWidget_Item.setMinimumSize(QtCore.QSize(760, 50))
        RuleWidget_Item.setMaximumSize(QtCore.QSize(16777215, 50))
        RuleWidget_Item.setObjectName("RuleWidget_Item")

        RuleWidget_Item.setStyleSheet("""
            QWidget#RuleWidget_Item {
                border-radius: 8px;
                background: rgba(255, 255, 255, 180);
                border: 1px solid rgba(200, 200, 200, 100);
                transition: all 0.3s ease;
            }
            QWidget#RuleWidget_Item:hover {
                background: rgba(255, 255, 255, 220);
                border: 1px solid rgba(105, 27, 253, 100);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            }
        """)

        main_layout = QtWidgets.QHBoxLayout(RuleWidget_Item)
        main_layout.setContentsMargins(12, 6, 12, 6)
        main_layout.setSpacing(12)
        main_layout.setObjectName("main_layout")

        keyword_frame = QtWidgets.QFrame(RuleWidget_Item)
        keyword_frame.setMinimumWidth(160)
        keyword_frame.setMaximumWidth(160)
        keyword_frame.setStyleSheet("background: transparent;")
        keyword_layout = QtWidgets.QVBoxLayout(keyword_frame)
        keyword_layout.setContentsMargins(0, 0, 0, 0)

        label_KeyWord = QtWidgets.QLabel(keyword, keyword_frame)
        label_KeyWord.setObjectName("label_KeyWord")
        label_KeyWord.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        label_KeyWord.setWordWrap(True)
        label_KeyWord.setMaximumHeight(40)

        font = QtGui.QFont()
        font.setPointSize(12)
        label_KeyWord.setFont(font)
        label_KeyWord.setStyleSheet("""
            color: rgba(105, 27, 253, 220);
            background: transparent;
            padding: 2px 0;
        """)

        keyword_layout.addWidget(label_KeyWord)
        main_layout.addWidget(keyword_frame)

        match_frame = QtWidgets.QFrame(RuleWidget_Item)
        match_frame.setMinimumWidth(60)
        match_frame.setMaximumWidth(60)
        match_frame.setStyleSheet("background: transparent;")
        match_layout = QtWidgets.QVBoxLayout(match_frame)
        match_layout.setContentsMargins(0, 0, 0, 0)

        label_Rule = QtWidgets.QLabel(match_type, match_frame)
        label_Rule.setObjectName("label_Rule")
        label_Rule.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font = QtGui.QFont()
        font.setPointSize(12)
        label_Rule.setFont(font)

        if match_type == "包含":
            bg_color = "rgba(0, 150, 136, 200)"
        elif match_type == "等于":
            bg_color = "rgba(33, 150, 243, 200)"
        elif match_type == "正则":
            bg_color = "rgba(156, 39, 176, 200)"
        else:
            bg_color = "rgba(121, 85, 72, 200)"

        label_Rule.setStyleSheet(f"""
            color: white;
            background: {bg_color};
            border-radius: 4px;
            padding: 3px 6px;
        """)

        match_layout.addWidget(label_Rule)
        main_layout.addWidget(match_frame)

        reply_frame = QtWidgets.QFrame(RuleWidget_Item)
        reply_frame.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        reply_frame.setStyleSheet("background: transparent;")
        reply_layout = QtWidgets.QVBoxLayout(reply_frame)
        reply_layout.setContentsMargins(0, 0, 0, 0)

        reply_label_frame = QtWidgets.QFrame(reply_frame)
        reply_label_frame.setStyleSheet("background: transparent;")
        reply_label_layout = QtWidgets.QHBoxLayout(reply_label_frame)
        reply_label_layout.setContentsMargins(0, 0, 0, 0)

        label_21 = QtWidgets.QLabel("回复：", reply_label_frame)
        label_21.setObjectName("label_21")
        label_21.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        label_21.setMinimumWidth(30)
        label_21.setMaximumWidth(50)

        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(13)
        label_21.setFont(font)
        label_21.setStyleSheet("""
            color: rgba(0, 0, 0, 180);
            background: transparent;
        """)

        label_Reply = QtWidgets.QLabel(reply_content, reply_label_frame)
        label_Reply.setObjectName("label_Reply")
        label_Reply.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        label_Reply.setWordWrap(True)
        label_Reply.setMaximumHeight(40)
        label_Reply.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        label_Reply.setFont(font)
        label_Reply.setStyleSheet("""
            color: rgba(0, 0, 0, 200);
            background: transparent;
        """)

        reply_label_layout.addWidget(label_21)
        reply_label_layout.addWidget(label_Reply, 1)
        reply_layout.addWidget(reply_label_frame)
        main_layout.addWidget(reply_frame, 1)

        apply_frame = QtWidgets.QFrame(RuleWidget_Item)
        apply_frame.setMinimumWidth(100)
        apply_frame.setMaximumWidth(100)
        apply_frame.setStyleSheet("background: transparent;")
        apply_layout = QtWidgets.QVBoxLayout(apply_frame)
        apply_layout.setContentsMargins(0, 0, 0, 0)

        label_ApplyTo = QtWidgets.QLabel(apply_to, apply_frame)
        label_ApplyTo.setObjectName("label_ApplyTo")
        label_ApplyTo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label_ApplyTo.setWordWrap(True)
        label_ApplyTo.setMaximumHeight(40)

        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        label_ApplyTo.setFont(font)
        label_ApplyTo.setStyleSheet("""
            color: rgba(255, 87, 34, 220);
            background: rgba(255, 243, 224, 200);
            border-radius: 4px;
            padding: 2px 6px;
        """)

        apply_layout.addWidget(label_ApplyTo)
        main_layout.addWidget(apply_frame)

        delete_button = QtWidgets.QPushButton("×", RuleWidget_Item)
        delete_button.setToolTip("删除该规则")
        delete_button.setObjectName("delete_button")
        delete_button.setFixedSize(24, 24)

        delete_button.setStyleSheet("""
            QPushButton#delete_button {
                background-color: rgba(255, 255, 255, 0);
                border: none;
                color: rgba(255, 100, 100, 0);
                font-size: 14px;
                font-weight: bold;
                transition: all 0.3s ease;
            }
            QWidget#RuleWidget_Item:hover QPushButton#delete_button {
                color: rgba(255, 100, 100, 255);
            }
            QPushButton#delete_button:hover {
                color: white;
                background-color: rgba(255, 59, 48, 1);
                border-radius: 12px;
            }
            QPushButton#delete_button:pressed {
                background-color: rgba(213, 0, 0, 1);
                transform: scale(0.9);
            }
        """)

        delete_button.hide()
        delete_button.clicked.connect(lambda checked, widget=RuleWidget_Item: self.remove_rule(widget))

        RuleWidget_Item.enterEvent = lambda event: delete_button.show()
        RuleWidget_Item.leaveEvent = lambda event: delete_button.hide()

        main_layout.addWidget(delete_button)
        log_print("Completed rule display frame creation")
        return RuleWidget_Item

    def add_rule(self):
        log_print("Starting to add new rule")
        match_type = self.ui.Rule_comboBox.currentText()
        keyword = self.ui.KeyWord_lineEdit.text()
        reply_content = self.ui.Reply_lineEdit.text()
        apply_to = self.ui.Apply_lineEdit.text() or "全部"

        if keyword == "" or reply_content == "":
            QtWidgets.QMessageBox.warning(self, "输入不完整", "关键词和回复内容为必填项，请确保输入完整。")
            log_print("Failed to add rule: Keyword or reply content is empty")
            return

        if match_type == "正则":
            try:
                re.compile(keyword)
            except re.error as e:
                QtWidgets.QMessageBox.warning(self, "正则表达式错误", f"您输入的正则表达式格式不正确: {str(e)}")
                log_print(f"Failed to add rule: Invalid regular expression - {keyword}: {str(e)}")
                return

        if self.is_duplicate_rule(keyword, match_type, reply_content, apply_to):
            QtWidgets.QMessageBox.warning(self, "规则重复", "相同配置的规则已存在!")
            log_print(f"Failed to add rule: Rule already exists - Keyword: {keyword}, Match Type: {match_type}")
            return

        widget_item = self.create_frame(keyword, match_type, reply_content, apply_to)
        self.ui.formLayout.addRow(widget_item)
        self.rules.append({
            "keyword": keyword,
            "match_type": match_type,
            "reply_content": reply_content,
            "apply_to": apply_to
        })

        self.ui.KeyWord_lineEdit.clear()
        self.ui.Reply_lineEdit.clear()
        self.ui.Apply_lineEdit.setText("全部")
        log_print(f"Successfully added rule - Keyword: {keyword}, Match Type: {match_type}")

    def is_duplicate_rule(self, keyword, match_type, reply_content, apply_to):
        log_print(f"Checking for duplicate rule - Keyword: {keyword}, Match Type: {match_type}")
        for rule in self.rules:
            if (rule['keyword'] == keyword and
                    rule['match_type'] == match_type and
                    rule['reply_content'] == reply_content and
                    rule['apply_to'] == apply_to):
                log_print(f"Duplicate rule found - Keyword: {keyword}, Match Type: {match_type}")
                return True
        return False

    def remove_rule(self, widget_item):
        log_print("Starting to delete rule")
        keyword = widget_item.findChild(QtWidgets.QLabel, "label_KeyWord").text()
        match_type = widget_item.findChild(QtWidgets.QLabel, "label_Rule").text()
        reply_content = widget_item.findChild(QtWidgets.QLabel, "label_Reply").text()
        apply_to = widget_item.findChild(QtWidgets.QLabel, "label_ApplyTo").text()

        for i, rule in enumerate(self.rules):
            if (rule['keyword'] == keyword and
                    rule['match_type'] == match_type and
                    rule['reply_content'] == reply_content and
                    rule['apply_to'] == apply_to):
                self.rules.pop(i)
                log_print(f"Removed from rule list - Keyword: {keyword}, Match Type: {match_type}")
                break

        layout = self.ui.formLayout
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget() == widget_item:
                layout.removeWidget(widget_item)
                widget_item.setParent(None)
                widget_item.deleteLater()
                log_print("Removed rule widget from UI")
                break

    def displayRules(self):
        log_print("Starting to display rules")
        while self.ui.formLayout.count():
            item = self.ui.formLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for rule in self.rules:
            widget_item = self.create_frame(
                rule['keyword'],
                rule['match_type'],
                rule['reply_content'],
                rule.get('apply_to', "全部")
            )
            self.ui.formLayout.addRow(widget_item)
        log_print(f"Displayed {len(self.rules)} rules")

    def on_cancel_clicked(self):
        log_print("Processing cancel operation")
        current_rules = []
        for i in range(self.ui.formLayout.count()):
            widget_item = self.ui.formLayout.itemAt(i).widget()
            if widget_item:
                current_rules.append({
                    "keyword": widget_item.findChild(QtWidgets.QLabel, "label_KeyWord").text(),
                    "match_type": widget_item.findChild(QtWidgets.QLabel, "label_Rule").text(),
                    "reply_content": widget_item.findChild(QtWidgets.QLabel, "label_Reply").text(),
                    "apply_to": widget_item.findChild(QtWidgets.QLabel, "label_ApplyTo").text()
                })

        if current_rules != self.original_rules:
            reply = QtWidgets.QMessageBox.question(
                self, "确认取消", "您还没保存，确定不保存并退出吗？",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No
            )
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                self.close()
                log_print("User confirmed cancel and closed window")
        else:
            self.close()
            log_print("Rules unchanged, closing window directly")

    def import_excel_rules(self):
        log_print("Starting to import Excel rules")
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "选择Excel文件", "", "Excel Files (*.xlsx *.xls)"
        )
        if not file_path:
            log_print("Cancelled importing Excel rules")
            return

        try:
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active
            log_print(f"Successfully opened Excel file: {file_path}")

            headers = [cell.value for cell in sheet[1]]
            required_headers = {'关键词', '匹配类型', '回复内容'}
            missing_headers = required_headers - set(headers)
            if missing_headers:
                QtWidgets.QMessageBox.warning(
                    self, "格式错误",
                    f"Excel文件缺少必要的列: {', '.join(missing_headers)}\n"
                    "Excel文件应包含: 关键词, 匹配类型, 回复内容"
                )
                log_print(f"Import failed: Excel file missing required columns - {', '.join(missing_headers)}")
                return

            keyword_col = headers.index('关键词')
            match_type_col = headers.index('匹配类型')
            reply_content_col = headers.index('回复内容')
            apply_to_col = headers.index('应用于') if '应用于' in headers else None
            log_print("Excel file headers verified")

            imported_count = 0
            skipped_count = 0
            duplicate_count = 0

            for row in sheet.iter_rows(min_row=2, values_only=True):
                if not row[keyword_col] or not row[reply_content_col]:
                    skipped_count += 1
                    continue

                keyword = str(row[keyword_col]).strip()
                reply_content = str(row[reply_content_col]).strip()

                match_type = str(row[match_type_col]).strip() if row[match_type_col] else "包含"
                if match_type not in {"包含", "等于", "正则"}:
                    match_type = "包含"

                apply_to = str(row[apply_to_col]).strip() if apply_to_col is not None and row[apply_to_col] else "全部"

                if match_type == "正则":
                    try:
                        re.compile(keyword)
                    except re.error as e:
                        skipped_count += 1
                        log_print(f"Skipping invalid regex: {keyword} - {str(e)}")
                        continue

                if self.is_duplicate_rule(keyword, match_type, reply_content, apply_to):
                    duplicate_count += 1
                    continue

                widget_item = self.create_frame(keyword, match_type, reply_content, apply_to)
                self.ui.formLayout.addRow(widget_item)
                self.rules.append({
                    "keyword": keyword,
                    "match_type": match_type,
                    "reply_content": reply_content,
                    "apply_to": apply_to
                })
                imported_count += 1

            message = f"成功导入 {imported_count} 条规则\n"
            if skipped_count > 0:
                message += f"跳过 {skipped_count} 条不完整的规则\n"
            if duplicate_count > 0:
                message += f"跳过 {duplicate_count} 条重复的规则"

            QtWidgets.QMessageBox.information(
                self,
                "导入完成",
                message,
                QtWidgets.QMessageBox.StandardButton.Ok
            )
            log_print(f"Excel rules import completed - Imported: {imported_count}, Skipped: {skipped_count}, Duplicates: {duplicate_count}")

        except Exception as e:
            log_print(f"Error importing Excel rules: {str(e)}")
            QtWidgets.QMessageBox.critical(
                self,
                "导入失败",
                f"导入Excel文件时出错: {str(e)}",
                QtWidgets.QMessageBox.StandardButton.Ok
            )
