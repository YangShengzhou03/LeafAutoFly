// 扩展应用实例，添加AI功能
app.config.globalProperties.$ai = {
    // 生成任务计划
    generateTaskPlan(prompt) {
        return new Promise(resolve => {
            // 模拟API调用延迟
            setTimeout(() => {
                const responses = [
                    "每日数据备份计划：\n1. 上午8:00 备份用户数据\n2. 下午14:00 备份系统配置\n3. 晚上22:00 备份日志文件",
                    "定期维护计划：\n1. 每周一凌晨3:00 系统检查\n2. 每月1日凌晨2:00 磁盘清理\n3. 每季度第一个周日 系统更新",
                    "API调用计划：\n1. 每小时调用一次数据同步API\n2. 每日9:00调用报表生成API\n3. 每周五18:00调用备份API"
                ];
                
                resolve(responses[Math.floor(Math.random() * responses.length)]);
            }, 1000);
        });
    },
    
    // 生成报告
    generateReport(topic) {
        return new Promise(resolve => {
            setTimeout(() => {
                const reports = [
                    `# ${topic} 报告\n\n## 摘要\n本报告总结了${topic}的主要情况和趋势...\n\n## 详细分析\n1. 数据统计\n2. 趋势分析\n3. 建议措施`,
                    `# ${topic} 状态报告\n\n### 完成情况\n- 已完成：60%\n- 进行中：30%\n- 未开始：10%\n\n### 问题与解决方案\n- 问题1：...\n- 解决方案：...`
                ];
                
                resolve(reports[Math.floor(Math.random() * reports.length)]);
            }, 1000);
        });
    },
    
    // 生成代码
    generateCode(requirement) {
        return new Promise(resolve => {
            setTimeout(() => {
                const codes = [
                    `// 根据需求生成的示例代码\nfunction processData(data) {\n  // 数据处理逻辑\n  return data.filter(item => item.active)\n    .map(item => ({ id: item.id, name: item.name }));\n}`,
                    `// API调用示例代码\nasync function fetchData(url) {\n  try {\n    const response = await fetch(url);\n    const data = await response.json();\n    return data;\n  } catch (error) {\n    console.error('获取数据失败:', error);\n    return null;\n  }\n}`
                ];
                
                resolve(codes[Math.floor(Math.random() * codes.length)]);
            }, 1000);
        });
    },
    
    // 获取建议
    getRecommendations(context) {
        return new Promise(resolve => {
            setTimeout(() => {
                const recommendations = [
                    "基于当前情况，我建议：\n1. 优化任务执行顺序，减少资源竞争\n2. 增加错误重试机制，提高稳定性\n3. 定期清理无用任务，提高系统效率",
                    "针对你的需求，推荐以下方案：\n1. 使用批量处理减少API调用次数\n2. 设置合理的缓存策略提升性能\n3. 实施监控告警机制及时发现问题"
                ];
                
                resolve(recommendations[Math.floor(Math.random() * recommendations.length)]);
            }, 1000);
        });
    },
    
    // 保存对话历史
    saveHistory(history) {
        localStorage.setItem('aiConversationHistory', JSON.stringify(history));
    },
    
    // 加载对话历史
    loadHistory() {
        const history = localStorage.getItem('aiConversationHistory');
        return history ? JSON.parse(history) : [];
    }
};

// 在当前页面的Vue实例中添加AI功能
app._context.config.globalProperties.data = function() {
    return {
        conversationHistory: this.$ai.loadHistory(),
        showPasswordDialog: false,
        showLoginLogs: false
    };
};

// 添加方法
app._context.config.globalProperties.methods = {
    // 生成任务计划
    generateTask() {
        this.$message.loading('AI正在生成任务计划...', 0);
        this.$ai.generateTaskPlan('日常维护').then(result => {
            this.$message.success('任务计划生成完成');
            
            // 找到AI控制台组件并添加消息
            const aiConsole = this.$root.$children.find(child => child.$options.name === 'ai-console');
            if (aiConsole) {
                aiConsole.messages.push({
                    text: "请为我生成一个任务计划",
                    isUser: true,
                    timestamp: aiConsole.formatTime(new Date())
                });
                aiConsole.messages.push({
                    text: result,
                    isUser: false,
                    timestamp: aiConsole.formatTime(new Date())
                });
                aiConsole.scrollToBottom();
                
                // 保存到历史记录
                this.conversationHistory.unshift("任务计划生成: " + result.substring(0, 50) + "...");
                if (this.conversationHistory.length > 10) {
                    this.conversationHistory.pop();
                }
                this.$ai.saveHistory(this.conversationHistory);
            }
        });
    },
    
    // 生成报告
    generateReport() {
        this.$message.loading('AI正在生成报告...', 0);
        this.$ai.generateReport('本周系统运行状态').then(result => {
            this.$message.success('报告生成完成');
            
            // 找到AI控制台组件并添加消息
            const aiConsole = this.$root.$children.find(child => child.$options.name === 'ai-console');
            if (aiConsole) {
                aiConsole.messages.push({
                    text: "请生成本周系统运行状态报告",
                    isUser: true,
                    timestamp: aiConsole.formatTime(new Date())
                });
                aiConsole.messages.push({
                    text: result,
                    isUser: false,
                    timestamp: aiConsole.formatTime(new Date())
                });
                aiConsole.scrollToBottom();
                
                // 保存到历史记录
                this.conversationHistory.unshift("报告生成: " + result.substring(0, 50) + "...");
                if (this.conversationHistory.length > 10) {
                    this.conversationHistory.pop();
                }
                this.$ai.saveHistory(this.conversationHistory);
            }
        });
    },
    
    // 生成代码
    generateCode() {
        this.$message.loading('AI正在生成代码...', 0);
        this.$ai.generateCode('数据处理函数').then(result => {
            this.$message.success('代码生成完成');
            
            // 找到AI控制台组件并添加消息
            const aiConsole = this.$root.$children.find(child => child.$options.name === 'ai-console');
            if (aiConsole) {
                aiConsole.messages.push({
                    text: "请生成一个数据处理的函数",
                    isUser: true,
                    timestamp: aiConsole.formatTime(new Date())
                });
                aiConsole.messages.push({
                    text: "以下是生成的代码：\n```javascript\n" + result + "\n```",
                    isUser: false,
                    timestamp: aiConsole.formatTime(new Date())
                });
                aiConsole.scrollToBottom();
                
                // 保存到历史记录
                this.conversationHistory.unshift("代码生成: " + result.substring(0, 50) + "...");
                if (this.conversationHistory.length > 10) {
                    this.conversationHistory.pop();
                }
                this.$ai.saveHistory(this.conversationHistory);
            }
        });
    },
    
    // 获取建议
    getRecommendations() {
        this.$message.loading('AI正在分析并生成建议...', 0);
        this.$ai.getRecommendations('系统性能优化').then(result => {
            this.$message.success('建议生成完成');
            
            // 找到AI控制台组件并添加消息
            const aiConsole = this.$root.$children.find(child => child.$options.name === 'ai-console');
            if (aiConsole) {
                aiConsole.messages.push({
                    text: "请提供一些系统性能优化的建议",
                    isUser: true,
                    timestamp: aiConsole.formatTime(new Date())
                });
                aiConsole.messages.push({
                    text: result,
                    isUser: false,
                    timestamp: aiConsole.formatTime(new Date())
                });
                aiConsole.scrollToBottom();
                
                // 保存到历史记录
                this.conversationHistory.unshift("建议获取: " + result.substring(0, 50) + "...");
                if (this.conversationHistory.length > 10) {
                    this.conversationHistory.pop();
                }
                this.$ai.saveHistory(this.conversationHistory);
            }
        });
    },
    
    // 清空历史记录
    clearHistory() {
        this.$confirm('确定要清空所有对话历史吗?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        }).then(() => {
            this.conversationHistory = [];
            this.$ai.saveHistory([]);
            this.$message.success('对话历史已清空');
        }).catch(() => {
            // 取消操作
        });
    },
    
    // 加载历史对话
    loadHistory(index) {
        const historyText = this.conversationHistory[index];
        // 在实际应用中，这里会加载完整的历史对话
        this.$message.info('已加载历史对话');
        
        // 找到AI控制台组件并清空当前消息
        const aiConsole = this.$root.$children.find(child => child.$options.name === 'ai-console');
        if (aiConsole) {
            aiConsole.messages = [
                {
                    text: "你好！我是你的AI助手，有什么可以帮助你的吗？",
                    isUser: false,
                    timestamp: aiConsole.formatTime(new Date())
                },
                {
                    text: "我想查看之前的对话内容",
                    isUser: true,
                    timestamp: aiConsole.formatTime(new Date())
                },
                {
                    text: historyText,
                    isUser: false,
                    timestamp: aiConsole.formatTime(new Date())
                }
            ];
            aiConsole.scrollToBottom();
        }
    }
};
