import re
from typing import List, Set, Optional

from PyQt6 import QtWidgets

from Thread import SplitWorkerThread
from common import log


class Split(QtWidgets.QWidget):
    def __init__(self, wx_instances: dict, membership: str, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self.parent = parent
        self.wx_instances = wx_instances
        self.current_wx = None
        self.membership = membership
        self.prepared_sentences = []
        self.is_sending = False
        self.split_thread = None
        self.update_current_wx()

    def update_current_wx(self) -> bool:
        selected_nickname = self.parent.comboBox_nickName.currentText()
        if selected_nickname in self.wx_instances:
            self.current_wx = self.wx_instances[selected_nickname]
            return True
        else:
            return False

    def on_start_split_clicked(self) -> None:
        if not self.update_current_wx() or self.current_wx is None:
            log("ERROR", "未选择有效的微信账号，请先选择微信账号")
            return

        split_rules = {
            'comma': self.parent.checkBox_comma.isChecked(),
            'space': self.parent.checkBox_Space.isChecked(),
            'period': self.parent.checkBox_period.isChecked(),
            'ai': self.parent.checkBox_Ai.isChecked()
        }

        if not any(split_rules.values()):
            log("WARNING", "请至少选择一种拆句规则作为句子分隔符")
            return

        message = self.parent.textEdit_2.toPlainText().strip()
        if not message:
            log("WARNING", "待拆分的文本内容为空")
            return

        delimiters = self._collect_delimiters(split_rules)
        self.prepared_sentences = self.split_message(message, delimiters)
        self._display_split_result()

    def _collect_delimiters(self, split_rules: dict) -> Set[str]:
        delimiters = set()

        if split_rules['comma']:
            delimiters.update(['，', ','])
        if split_rules['space']:
            delimiters.add(' ')
        if split_rules['period']:
            delimiters.update(['。', '.'])
        if split_rules['ai']:
            delimiters.update([
                '。', '.', '？', '?', '！', '!', '，', ',', '；', ';', '：', ':',
                '（', '）', '【', '】', '［', '］', '〈', '〉', '《', '》', '『', '』',
                '、', '——', '…', '……', '-', '·', '—', '“', '”', '‘', '’', '`',
                '\'', '"', '/', '｜', '│', '+', '-', '*', '%', '=', '#', '@',
                '&', '^', '_', '~', '\\', '|', '[', ']', '{', '}', '<', '>'
            ])

        return delimiters

    def _display_split_result(self) -> None:
        result_count = len(self.prepared_sentences)
        if result_count == 0:
            log("INFO", "未拆分出任何句子")
            return

        log("INFO", f"成功拆分为 {result_count} 个句子")
        self.parent.textEdit_2.clear()
        for i, sentence in enumerate(self.prepared_sentences, 1):
            self.parent.textEdit_2.append(f"{i}. {sentence}")

    def on_start_send_clicked(self) -> None:
        if not self.update_current_wx() or self.current_wx is None:
            log("ERROR", "未选择有效的微信账号，请先选择微信账号")
            return

        if self.is_sending:
            self._stop_sending()
        else:
            receiver = self.parent.SplitReceiver_lineEdit.text().strip()
            if not receiver:
                log("WARNING", "句子接收者为空，请输入有效的接收者")
                return

            if not self.prepared_sentences:
                log("WARNING", "没有准备好的句子，请先进行拆分")
                return

            self._start_sending(receiver)

    def _stop_sending(self) -> None:
        self.is_sending = False
        self.parent.pushButton_startSplit.setText("发送句子")
        if self.split_thread is not None:
            self.split_thread.requestInterruption()
            self.split_thread = None
            log("INFO", "已停止句子发送任务")

    def _start_sending(self, receiver: str) -> None:
        self.is_sending = True
        self.parent.pushButton_startSplit.setText("停止发送")

        self.split_thread = SplitWorkerThread(
            self,
            receiver=receiver,
            sentences=self.prepared_sentences,
            wx_instance=self.current_wx
        )
        self.split_thread.finished.connect(self.on_thread_finished)
        self.split_thread.start()
        log("INFO", f"开始向 {receiver} 发送拆分的句子")

    def on_thread_finished(self) -> None:
        log("INFO", "段落拆句发送任务执行完成")
        self.is_sending = False
        self.parent.pushButton_startSplit.setText("发送句子")

    def split_message(self, message: str, delimiters: Set[str]) -> List[str]:
        if not message:
            return []

        processed_message = self._handle_parentheses(message)

        delimiter_pattern = '|'.join(map(re.escape, delimiters))

        sentences = re.split(delimiter_pattern, processed_message)

        return [s.strip() for s in sentences if s.strip()]

    def _handle_parentheses(self, text: str) -> str:
        return re.sub(r'([\(\（][^(\(\（\)\）)]*[\)\）])', lambda m: m.group(0).replace('。', ''), text)
