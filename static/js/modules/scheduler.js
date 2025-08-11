// 任务调度模块
const schedulerModule = {
    // 获取所有任务
    async getTasks() {
        try {
            const response = await fetch('/api/tasks');
            if (!response.ok) {
                throw new Error('获取任务失败');
            }
            return await response.json();
        } catch (error) {
            console.error('获取任务列表时出错:', error);
            throw error;
        }
    },
    
    // 创建新任务
    async createTask(taskData) {
        try {
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(taskData)
            });
            
            if (!response.ok) {
                throw new Error('创建任务失败');
            }
            
            return await response.json();
        } catch (error) {
            console.error('创建任务时出错:', error);
            throw error;
        }
    },
    
    // 更新任务
    async updateTask(taskId, taskData) {
        try {
            const response = await fetch(`/api/tasks/${taskId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(taskData)
            });
            
            if (!response.ok) {
                throw new Error('更新任务失败');
            }
            
            return await response.json();
        } catch (error) {
            console.error('更新任务时出错:', error);
            throw error;
        }
    },
    
    // 删除任务
    async deleteTask(taskId) {
        try {
            const response = await fetch(`/api/tasks/${taskId}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error('删除任务失败');
            }
            
            return await response.json();
        } catch (error) {
            console.error('删除任务时出错:', error);
            throw error;
        }
    },
    
    // 立即运行任务
    async runTaskNow(taskId) {
        try {
            const response = await fetch(`/api/tasks/${taskId}/run`, {
                method: 'POST'
            });
            
            if (!response.ok) {
                throw new Error('运行任务失败');
            }
            
            return await response.json();
        } catch (error) {
            console.error('运行任务时出错:', error);
            throw error;
        }
    },
    
    // 格式化Cron表达式为人类可读形式
    formatCronExpression(expr) {
        if (!expr) return "无效表达式";
        
        const parts = expr.split(' ');
        if (parts.length !== 5) return "无效表达式";
        
        const [minute, hour, day, month, weekday] = parts;
        
        let result = '';
        
        // 处理分钟
        if (minute === '*') result += '每分钟 ';
        else if (minute.startsWith('*/')) result += `每${minute.slice(2)}分钟 `;
        else result += `${minute}分 `;
        
        // 处理小时
        if (hour === '*') result += '每小时 ';
        else if (hour.startsWith('*/')) result += `每${hour.slice(2)}小时 `;
        else result += `${hour}时 `;
        
        // 处理日期和星期
        if (day === '*' && weekday === '*') result += '每天 ';
        else if (day !== '*') result += `${day}日 `;
        else if (weekday !== '*') {
            if (weekday.startsWith('*/')) result += `每${weekday.slice(2)}周 `;
            else {
                const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
                result += `${weekdays[parseInt(weekday)]} `;
            }
        }
        
        // 处理月份
        if (month === '*') result += '每月';
        else if (month.startsWith('*/')) result += `每${month.slice(2)}月`;
        else result += `${month}月`;
        
        return result;
    },
    
    // 解析人类可读时间到Cron表达式
    parseHumanToCron(humanExpression) {
        // 简单实现，实际应用中可以扩展更多规则
        humanExpression = humanExpression.toLowerCase();
        
        // 默认值
        let minute = '*', hour = '*', day = '*', month = '*', weekday = '*';
        
        // 处理分钟
        if (humanExpression.includes('每5分钟')) minute = '*/5';
        else if (humanExpression.includes('每10分钟')) minute = '*/10';
        else if (humanExpression.includes('每30分钟')) minute = '*/30';
        else if (humanExpression.includes('每分钟')) minute = '*';
        else if (humanExpression.match(/(\d+)分/)) {
            minute = humanExpression.match(/(\d+)分/)[1];
        }
        
        // 处理小时
        if (humanExpression.includes('每小时')) hour = '*';
        else if (humanExpression.includes('每2小时')) hour = '*/2';
        else if (humanExpression.match(/(\d+)时/)) {
            hour = humanExpression.match(/(\d+)时/)[1];
        }
        
        // 处理日期
        if (humanExpression.includes('每天')) {
            day = '*';
            weekday = '*';
        } else if (humanExpression.match(/(\d+)日/)) {
            day = humanExpression.match(/(\d+)日/)[1];
            weekday = '*';
        }
        
        // 处理星期
        const weekdaysMap = {
            '周日': '0', '周一': '1', '周二': '2', '周三': '3',
            '周四': '4', '周五': '5', '周六': '6'
        };
        
        for (const [name, value] of Object.entries(weekdaysMap)) {
            if (humanExpression.includes(name)) {
                weekday = value;
                day = '*';
                break;
            }
        }
        
        // 处理月份
        if (humanExpression.includes('每月')) month = '*';
        else if (humanExpression.match(/(\d+)月/)) {
            month = humanExpression.match(/(\d+)月/)[1];
        }
        
        return `${minute} ${hour} ${day}