from .nlp import NLPProcessor

class DialogManager:
    """对话管理系统（示例实现）"""
    
    def __init__(self):
        self.nlp = NLPProcessor()
        self.context = {}
    
    def process_message(self, message):
        """处理用户消息并生成响应"""
        # 分析意图
        intent = self.nlp.analyze_intent(message)
        # 提取实体
        entities = self.nlp.extract_entities(message)
        
        # 根据意图生成响应
        response = self.generate_response(intent, entities, message)
        
        # 更新对话上下文
        self.context['last_intent'] = intent
        self.context['last_entities'] = entities
        
        return response
    
    def generate_response(self, intent, entities, original_message):
        """根据意图生成响应"""
        if intent == 'task_management':
            return self._handle_task_intent(entities, original_message)
        elif intent == 'system_settings':
            return "你可以在设置页面调整系统参数，包括主题、通知等选项。需要我指导你如何操作吗？"
        elif intent == 'help':
            return "我可以帮助你管理定时任务和系统设置。你可以问我如何创建任务、修改任务或者调整系统参数。"
        else:
            return "我不太明白你的意思。你可以问我关于任务调度或系统设置的问题，我会尽力帮助你。"
    
    def _handle_task_intent(self, entities, original_message):
        """处理任务相关意图"""
        task_name = next((e['value'] for e in entities if e['type'] == 'task_name'), None)
        
        if '创建' in original_message:
            if task_name:
                return f"你想创建名为'{task_name}'的任务吗？请告诉我任务的执行时间和描述，我可以帮你创建。"
            else:
                return "你想创建新任务吗？请告诉我任务名称、执行时间和描述。"
        elif '删除' in original_message:
            if task_name:
                return f"你想删除名为'{task_name}'的任务吗？这个操作不可恢复，请确认。"
            else:
                return "你想删除哪个任务？请告诉我任务名称。"
        elif '运行' in original_message or '执行' in original_message:
            if task_name:
                return f"你想立即运行名为'{task_name}'的任务吗？"
            else:
                return "你想运行哪个任务？请告诉我任务名称。"
        else:
            return "你想对任务进行什么操作？我可以帮你创建、编辑、删除或运行任务。"
