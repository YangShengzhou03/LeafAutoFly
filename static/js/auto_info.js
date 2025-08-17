// 表单元素绑定轮询函数
function ensureFormBinding() {
    const taskForm = document.getElementById('taskForm');
    const submitBtn = document.getElementById('submitBtn');
    
    if (taskForm && submitBtn) {
        console.log('表单元素已找到，开始绑定事件');
        
        // 移除旧事件监听器
        taskForm.removeEventListener('submit', handleFormSubmit);
        submitBtn.removeEventListener('click', handleSubmitClick);
        
        // 添加新的事件监听器
        taskForm.addEventListener('submit', handleFormSubmit);
        submitBtn.addEventListener('click', handleSubmitClick);
        
        console.log('表单提交事件已绑定');
        return true;
    } else {
        console.log('表单元素尚未准备好，将重试...');
        return false;
    }
}

// 提交按钮点击处理
function handleSubmitClick(e) {
    console.log('提交按钮点击事件触发');
    e.preventDefault();
    e.stopPropagation();
    
    const taskForm = document.getElementById('taskForm');
    if (taskForm) {
        // 手动触发表单提交事件，确保处理逻辑统一
        const submitEvent = new Event('submit', {cancelable: true, bubbles: true});
        taskForm.dispatchEvent(submitEvent);
    }
}

// 初始化表单和事件监听
function initForm() {
    console.log('初始化表单');
    
    // 尝试立即绑定表单事件，如果失败则轮询重试
    if (!ensureFormBinding()) {
        // 设置轮询，每100毫秒尝试一次，最多尝试10次
        let attempts = 0;
        const maxAttempts = 10;
        const pollInterval = setInterval(() => {
            attempts++;
            if (ensureFormBinding() || attempts >= maxAttempts) {
                clearInterval(pollInterval);
                if (attempts >= maxAttempts) {
                    console.error('超过最大尝试次数，无法绑定表单事件');
                }
            }
        }, 100);
    }
    
    // 加载任务列表
    loadTasks();
    
    // 处理URL参数
    handleUrlParams();
    
    // 设置默认时间
function setDefaultTime() {
    // 获取当前日期时间
    const now = new Date();

    console.log("加载啦")
    
    // 格式化日期为 YYYY-MM-DD
    const date = now.toISOString().split('T')[0];
    
    // 格式化时间为 HH:MM
    const time = now.toTimeString().split(' ')[0].slice(0, 5);
    
    // 组合成 datetime-local 格式
    const defaultDateTime = `${date}T${time}`;
    
    // 设置输入框的值
    const sendTimeInput = document.getElementById('sendTime');
    if (sendTimeInput) {
        sendTimeInput.value = defaultDateTime;
    }
}

setDefaultTime();
}

// 加载任务列表
function loadTasks() {
    fetch('/api/tasks')
    .then(response => response.json())
    .then(tasks => {
        renderTaskList(tasks);
    })
    .catch(error => {
        console.error('加载任务列表时出错:', error);
        showNotification('加载任务失败: ' + error.message, 'error');
    });
}

// 处理URL参数
function handleUrlParams() {
    const params = new URLSearchParams(window.location.search);
    if (params.has('recipient') && params.has('sendTime') && params.has('messageContent')) {
        const taskData = {
            recipient: params.get('recipient'),
            sendTime: params.get('sendTime'),
            repeatType: params.get('repeatType') || 'none',
            messageContent: params.get('messageContent')
        };
        
        // 填充表单
        document.getElementById('recipient').value = taskData.recipient;
        document.getElementById('sendTime').value = taskData.sendTime;
        document.getElementById('repeatType').value = taskData.repeatType;
        document.getElementById('messageContent').value = taskData.messageContent;
        
        // 如果有repeatDays参数
        if (params.has('repeatDays')) {
            const repeatDays = params.get('repeatDays').split(',');
            repeatDays.forEach(day => {
                const checkbox = document.querySelector(`input[name="repeatDays"][value="${day}"]`);
                if (checkbox) checkbox.checked = true;
            });
        }
        
        // 更新重复按钮显示
        const repeatBtn = document.getElementById('repeatBtn');
        const repeatOptions = document.querySelectorAll('.repeat-option');
        repeatOptions.forEach(option => {
            if (option.getAttribute('data-repeat') === taskData.repeatType) {
                repeatBtn.firstChild.textContent = option.textContent + ' ';
            }
        });
        
        // 显示/隐藏自定义日期
        document.getElementById('customDays').style.display = 
            taskData.repeatType === 'custom' ? 'block' : 'none';
    }
}

// 当DOM加载完成时初始化表单
document.addEventListener('DOMContentLoaded', initForm);

// 监听页面刷新事件，确保表单绑定
window.addEventListener('load', initForm);

// 表单提交处理函数
function handleFormSubmit(e) {
    console.log('表单提交事件触发');
    e.preventDefault();
    e.stopPropagation();
    
    // 收集表单数据
    const formData = {
        recipient: document.getElementById('recipient').value,
        sendTime: document.getElementById('sendTime').value,
        repeatType: document.getElementById('repeatType').value,
        messageContent: document.getElementById('messageContent').value
    };
    
    // 简单验证
    if (!formData.recipient.trim()) {
        showNotification('请输入接收者', 'error');
        return;
    }
    
    if (!formData.sendTime) {
        showNotification('请选择发送时间', 'error');
        return;
    }
    
    if (!formData.messageContent.trim()) {
        showNotification('请输入消息内容', 'error');
        return;
    }
    
    // 处理重复日期
    if (formData.repeatType === 'custom') {
        const repeatDays = Array.from(
            document.querySelectorAll('input[name="repeatDays"]:checked')
        ).map(checkbox => checkbox.value);
        
        if (repeatDays.length === 0) {
            showNotification('请至少选择一个重复日期', 'error');
            return;
        }
        
        formData.repeatDays = repeatDays;
    }
    
    addTask(formData);
}

// 添加任务到列表
function addTask(taskData) {
    try {
        // 发送POST请求到后端API
        fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(taskData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('网络响应错误: ' + response.status);
            }
            return response.json();
        })
        .then(newTask => {
            console.log('任务已添加:', newTask);
            
            // 获取最新任务列表
            fetch('/api/tasks')
            .then(response => response.json())
            .then(tasks => {
                // 刷新任务列表
                renderTaskList(tasks);
                showNotification('任务创建成功', 'success');
            });
            
            // 清空表单
            const taskForm = document.getElementById('taskForm');
            if (taskForm) taskForm.reset();
            
            document.getElementById('repeatType').value = 'none';
            document.getElementById('repeatBtn').firstChild.textContent = '不重复 ';
            document.getElementById('customDays').style.display = 'none';
            
            // 设置默认时间
        setDefaultTime();
        })
        .catch(error => {
            console.error('添加任务时出错:', error);
            showNotification('添加任务失败: ' + error.message, 'error');
        });
    } catch (error) {
        console.error('添加任务时出错:', error);
        showNotification('添加任务失败: ' + error.message, 'error');
    }
}

// 删除指定ID的任务
function deleteTask(taskId) {
    if (confirm('确定要删除这个任务吗？')) {
        try {
            // 找到要删除的任务元素并添加动画
            const taskElement = document.querySelector(`[data-task-id="${taskId}"]`);
            if (taskElement) {
                taskElement.classList.add('task-remove-animation');
                
                // 等待动画完成后再调用API
                setTimeout(() => {
                    // 发送DELETE请求到后端API
                    fetch(`/api/tasks/${taskId}`, {
                        method: 'DELETE'
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('网络响应错误: ' + response.status);
                        }
                        return response.json();
                    })
                    .then(data => {
                        // 获取最新任务列表
                        fetch('/api/tasks')
                        .then(response => response.json())
                        .then(tasks => {
                            // 刷新任务列表
                            renderTaskList(tasks);
                            showNotification('任务删除成功', 'success');
                        });
                    })
                    .catch(error => {
                        console.error('删除任务时出错:', error);
                        showNotification('删除任务失败: ' + error.message, 'error');
                    });
                }, 300);
            }
        } catch (error) {
            console.error('删除任务时出错:', error);
            showNotification('删除任务失败: ' + error.message, 'error');
        }
    }
}

// 创建任务项DOM元素
function createTaskItem(task) {
    const li = document.createElement('li');
    li.className = 'task-item task-transition';
    li.dataset.taskId = task.id;
    
    // 格式化日期时间显示
    const sendTime = new Date(task.sendTime);
    const formattedTime = `${sendTime.getFullYear()}-${padZero(sendTime.getMonth() + 1)}-${padZero(sendTime.getDate())} ${padZero(sendTime.getHours())}:${padZero(sendTime.getMinutes())}`;
    
    // 处理重复类型显示
    let repeatText = '不重复';
    if (task.repeatType === 'daily') repeatText = '每天';
    else if (task.repeatType === 'weekly') repeatText = '每周';
    else if (task.repeatType === 'monthly') repeatText = '每月';
    else if (task.repeatType === 'workday') repeatText = '法定工作日';
    else if (task.repeatType === 'holiday') repeatText = '法定节假日';
    else if (task.repeatType === 'custom') {
        // 转换数字为星期几
        const dayMap = {
            '0': '周日',
            '1': '周一',
            '2': '周二',
            '3': '周三',
            '4': '周四',
            '5': '周五',
            '6': '周六'
        };
        repeatText = `自定义: ${task.repeatDays?.map(day => dayMap[day]).join(', ') || ''}`;
    }
    
    li.innerHTML = `
        <div class="task-content">
            <h3 class="task-recipient">接收者: ${escapeHtml(task.recipient)}</h3>
            <p class="task-message">内容: ${escapeHtml(task.messageContent)}</p>
            <div class="task-meta">
                <span class="task-time"><i class="fa fa-clock-o"></i> ${formattedTime}</span>
                <span class="task-repeat"><i class="fa fa-refresh"></i> ${repeatText}</span>
                <span class="task-status ${task.status}">${task.status === 'pending' ? '待执行' : '已完成'}</span>
            </div>
        </div>
        <div class="task-actions">
            <button class="delete-btn" data-task-id="${task.id}" aria-label="删除任务">
                <i class="fa fa-trash-o"></i> 删除
            </button>
        </div>
    `;
    
    // 绑定删除事件
    const deleteBtn = li.querySelector('.delete-btn');
    deleteBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        deleteTask(task.id);
    });
    
    return li;
}

// 渲染完整任务列表
function renderTaskList(tasks) {
    try {
        const taskList = document.getElementById('taskList');
        const taskCount = document.getElementById('taskCount');
        const emptyState = document.getElementById('emptyTaskState');

        if (!(taskList && taskCount && emptyState)) {
            console.error('缺少必要的DOM元素: taskList, taskCount或emptyState');
            return;
        }

        // 清除现有任务项（除了正在删除动画的）
        const itemsToRemove = taskList.querySelectorAll('.task-item:not(.task-remove-animation)');
        itemsToRemove.forEach(item => item.remove());

        // 更新任务计数
        taskCount.textContent = tasks.length;

        // 显示/隐藏空状态
        emptyState.style.display = tasks.length === 0 ? 'flex' : 'none';

        // 按时间排序任务
        const sortedTasks = [...tasks].sort((a, b) => new Date(a.sendTime) - new Date(b.sendTime));
        
        // 添加所有任务项
        sortedTasks.forEach(task => {
            const taskItem = createTaskItem(task);
            taskList.appendChild(taskItem);
        });

    } catch (error) {
        console.error('渲染任务列表时出错:', error);
    }
}

// 数字补零(小于10加前导零)
function padZero(num) {
    return num < 10 ? '0' + num : num;
}

// 转义HTML特殊字符(防止XSS攻击)
function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// 显示通知消息
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `notification ${type} task-transition`;
    notification.textContent = message;
    
    // 添加到页面
    const notificationContainer = document.getElementById('notificationContainer');
    if (notificationContainer) {
        notificationContainer.appendChild(notification);
    } else {
        document.body.appendChild(notification);
    }
    
    // 显示通知（触发动画）
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // 3秒后自动消失
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// 设置默认时间函数
function setDefaultTime() {
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset(), 0, 0);
    document.getElementById('sendTime').value = now.toISOString().slice(0, 16);
}

// 重复选项切换逻辑
document.addEventListener('DOMContentLoaded', function() {
    // 添加重复选项切换逻辑
    const repeatBtn = document.getElementById('repeatBtn');
    const repeatOptions = document.getElementById('repeatOptions');
    if (repeatBtn && repeatOptions) {
        repeatBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            repeatOptions.style.display = repeatOptions.style.display === 'none' ? 'block' : 'none';
        });
        
        // 点击其他区域关闭下拉
        document.addEventListener('click', (e) => {
            if (!repeatBtn.contains(e.target) && !repeatOptions.contains(e.target)) {
                repeatOptions.style.display = 'none';
            }
        });
        
        // 重复选项点击事件
        document.querySelectorAll('.repeat-option').forEach(option => {
            option.addEventListener('click', function() {
                const repeatType = this.getAttribute('data-repeat');
                document.getElementById('repeatType').value = repeatType;
                repeatBtn.firstChild.textContent = this.textContent + ' ';
                repeatOptions.style.display = 'none';
                
                // 显示/隐藏自定义日期
                document.getElementById('customDays').style.display = 
                    repeatType === 'custom' ? 'block' : 'none';
            });
        });
    }
    
    // 添加重置按钮功能
    const resetBtn = document.getElementById('resetBtn');
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            const taskForm = document.getElementById('taskForm');
            if (taskForm) taskForm.reset();
            
            document.getElementById('repeatType').value = 'none';
            document.getElementById('repeatBtn').firstChild.textContent = '不重复 ';
            document.getElementById('customDays').style.display = 'none';
            
            // 设置默认时间
            setDefaultTime();
        });
    }
    
    // 字符计数实时更新
    const messageContent = document.getElementById('messageContent');
    const charCount = document.getElementById('charCount');
    if (messageContent && charCount) {
        messageContent.addEventListener('input', function() {
            charCount.textContent = `${this.value.length}/500`;
            // 超过字数限制时给出视觉提示
            if (this.value.length > 500) {
                this.value = this.value.substring(0, 500);
                charCount.textContent = `500/500`;
            } else {
                charCount.style.color = '';
            }
        });
    }
});
