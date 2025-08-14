document.addEventListener('DOMContentLoaded', function() {
    // 初始化表单验证
    initValidation();

    // 初始化重复选项
    initRepeatOptions();

    // 初始化字符计数
    initCharCount();

    // 加载任务列表
    loadTasks();
});

// 初始化表单验证
function initValidation() {
    const form = document.getElementById('taskForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            // 获取表单数据
            const messageType = document.getElementById('messageType').value;
            const recipient = document.getElementById('recipient').value;
            const subject = document.getElementById('subject').value;
            const sendTime = document.getElementById('sendTime').value;
            const messageContent = document.getElementById('messageContent').value;
            const repeatType = document.getElementById('repeatType').value;

            // 基本验证
            let isValid = true;
            let errorMessage = '';

            if (!messageType) {
                isValid = false;
                errorMessage += '请选择消息类型\n';
            }

            if (!recipient) {
                isValid = false;
                errorMessage += '请输入收件人\n';
            } else if (messageType === 'email' && !isValidEmail(recipient)) {
                isValid = false;
                errorMessage += '请输入有效的邮箱地址\n';
            } else if (messageType === 'sms' && !isValidPhone(recipient)) {
                isValid = false;
                errorMessage += '请输入有效的手机号码\n';
            }

            if (!subject) {
                isValid = false;
                errorMessage += '请输入主题\n';
            }

            if (!sendTime) {
                isValid = false;
                errorMessage += '请选择发送时间\n';
            }

            if (!messageContent) {
                isValid = false;
                errorMessage += '请输入消息内容\n';
            } else if (messageContent.length > 500) {
                isValid = false;
                errorMessage += '消息内容不能超过500个字符\n';
            }

            // 处理自定义重复选项
            let repeatDays = [];
            if (repeatType === 'custom') {
                const checkedDays = document.querySelectorAll('input[name="repeatDays"]:checked');
                if (checkedDays.length === 0) {
                    isValid = false;
                    errorMessage += '请至少选择一个重复日期\n';
                } else {
                    checkedDays.forEach(day => {
                        repeatDays.push(day.value);
                    });
                }
            }

            if (isValid) {
                // 准备任务数据
                const taskData = {
                    id: Date.now().toString(),
                    messageType: messageType,
                    recipient: recipient,
                    subject: subject,
                    sendTime: sendTime,
                    messageContent: messageContent,
                    repeatType: repeatType,
                    repeatDays: repeatDays.length > 0 ? repeatDays : null,
                    status: 'pending',
                    createdAt: new Date().toISOString()
                };

                // 添加任务
                addTask(taskData);

                // 重置表单
                form.reset();
                document.getElementById('charCount').textContent = '0/500';
                document.getElementById('customDays').style.display = 'none';
                document.getElementById('repeatBtn').innerHTML = '不重复 <span class="dropdown-icon"></span>';

                // 显示成功通知
                showNotification('任务创建成功', 'success');
            } else {
                // 显示错误通知
                showNotification(errorMessage, 'error');
            }
        });
    }
}

// 初始化重复选项
function initRepeatOptions() {
    const repeatBtn = document.getElementById('repeatBtn');
    const repeatOptions = document.getElementById('repeatOptions');
    const repeatType = document.getElementById('repeatType');
    const customDays = document.getElementById('customDays');

    if (repeatBtn && repeatOptions && repeatType && customDays) {
        // 切换下拉菜单显示/隐藏
        repeatBtn.addEventListener('click', function(e) {
            e.stopPropagation(); // 防止事件冒泡到document
            repeatOptions.style.display = repeatOptions.style.display === 'block' ? 'none' : 'block';
        });

        // 点击其他地方关闭下拉菜单
        document.addEventListener('click', function(e) {
            if (!repeatBtn.contains(e.target) && !repeatOptions.contains(e.target)) {
                repeatOptions.style.display = 'none';
            }
        });

        // 选择重复类型
        const optionElements = document.querySelectorAll('.repeat-option');
        optionElements.forEach(option => {
            option.addEventListener('click', function() {
                const selectedValue = this.getAttribute('data-repeat');
                const selectedText = this.textContent;
                repeatBtn.innerHTML = selectedText + ' <span class="dropdown-icon"></span>';
                repeatType.value = selectedValue;
                repeatOptions.style.display = 'none';

                // 显示/隐藏自定义日期选项
                if (selectedValue === 'custom') {
                    customDays.style.display = 'block';
                } else {
                    customDays.style.display = 'none';
                }
            });
        });
    }
}

// 初始化字符计数
function initCharCount() {
    const messageContent = document.getElementById('messageContent');
    const charCount = document.getElementById('charCount');

    if (messageContent && charCount) {
        messageContent.addEventListener('input', function() {
            const length = this.value.length;
            charCount.textContent = length + '/500';

            // 超过限制时改变颜色
            if (length > 500) {
                charCount.style.color = 'red';
            } else {
                charCount.style.color = 'inherit';
            }
        });
    }
}

// 加载任务
function loadTasks() {
    const tasks = JSON.parse(localStorage.getItem('autoInfoTasks')) || [];
    renderTaskList(tasks);
}

// 渲染任务列表
function renderTaskList(tasks) {
    // 检查DOM元素是否存在
    const taskList = document.getElementById('taskList');
    const taskCount = document.getElementById('taskCount');
    const emptyTaskState = document.getElementById('emptyTaskState');

    if (!taskList || !taskCount || !emptyTaskState) {
        console.error('One or more required DOM elements are missing');
        return;
    }

    // 清空任务列表
    taskList.innerHTML = '';

    // 更新任务计数
    taskCount.textContent = tasks.length;

    // 显示/隐藏空状态
    if (tasks.length === 0) {
        emptyTaskState.style.display = 'block';
    } else {
        emptyTaskState.style.display = 'none';

        // 按发送时间排序
        tasks.sort((a, b) => new Date(a.sendTime) - new Date(b.sendTime));

        // 渲染每个任务
        tasks.forEach((task, index) => {
            const taskItem = document.createElement('div');
            taskItem.className = 'task-item ' + task.status;

            // 获取格式化的日期
            const sendDate = new Date(task.sendTime);
            const formattedDate = sendDate.toLocaleString();

            // 设置任务内容
            taskItem.innerHTML = `
                <div class="task-header">
                    <div class="task-type">${getTaskTypeText(task.messageType)}</div>
                    <div class="task-status">${getStatusText(task.status)}</div>
                </div>
                <div class="task-content">
                    <h3>${task.subject}</h3>
                    <p class="recipient">${task.recipient}</p>
                    <p class="send-time">发送时间: ${formattedDate}</p>
                    <p class="repeat-info">${getRepeatInfo(task.repeatType, task.repeatDays)}</p>
                </div>
                <div class="task-actions">
                    <button class="edit-btn" data-index="${index}">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
                    </button>
                    <button class="delete-btn" data-index="${index}">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                    </button>
                </div>
            `;

            // 添加到任务列表
            taskList.appendChild(taskItem);
        });

        // 添加编辑和删除事件
        document.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const index = parseInt(this.getAttribute('data-index'));
                editTask(index);
            });
        });

        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const index = parseInt(this.getAttribute('data-index'));
                deleteTask(index);
            });
        });
    }
}

// 获取任务类型文本
function getTaskTypeText(type) {
    switch (type) {
        case 'email':
            return '邮件';
        case 'sms':
            return '短信';
        case 'push':
            return '推送';
        default:
            return '未知';
    }
}

// 获取状态文本
function getStatusText(status) {
    switch (status) {
        case 'pending':
            return '待执行';
        case 'running':
            return '执行中';
        case 'completed':
            return '已完成';
        case 'failed':
            return '执行失败';
        default:
            return '未知状态';
    }
}

// 获取重复信息
function getRepeatInfo(type, days) {
    if (!type || type === 'none') {
        return '不重复';
    }

    let repeatText = getRepeatText(type);

    if (type === 'custom' && days && days.length > 0) {
        const dayNames = {
            'mon': '周一',
            'tue': '周二',
            'wed': '周三',
            'thu': '周四',
            'fri': '周五',
            'sat': '周六',
            'sun': '周日'
        };

        const dayTexts = days.map(day => dayNames[day] || day).join('、');
        repeatText += ` (${dayTexts})`;
    }

    return `重复: ${repeatText}`;
}

// 验证邮箱
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// 验证手机
function isValidPhone(phone) {
    const re = /^1[3-9]\d{9}$/;
    return re.test(phone);
}

// 显示通知
function showNotification(message, type = 'info') {
    const notificationContainer = document.getElementById('notificationContainer');

    if (notificationContainer) {
        // 创建通知元素
        const notification = document.createElement('div');
        notification.className = `notification notification-${type} animate-fade-in`;
        notification.innerHTML = `
            <div class="notification-icon">
                ${getNotificationIcon(type)}
            </div>
            <div class="notification-content">
                <p>${message}</p>
            </div>
            <button type="button" class="close-notification">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
        `;

        // 添加到容器
        notificationContainer.appendChild(notification);

        // 关闭按钮事件
        notification.querySelector('.close-notification').addEventListener('click', function() {
            notification.classList.add('animate-fade-out');
            setTimeout(() => {
                notification.remove();
            }, 300);
        });

        // 自动关闭
        setTimeout(() => {
            notification.classList.add('animate-fade-out');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 5000);
    }
}

// 获取通知图标
function getNotificationIcon(type) {
    switch (type) {
        case 'success':
            return '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
        case 'error':
            return '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>';
        case 'info':
            return '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>';
        default:
            return '';
    }
}

// 添加任务
function addTask(taskData) {
    // 获取现有任务
    const tasks = JSON.parse(localStorage.getItem('autoInfoTasks')) || [];

    // 添加新任务
    tasks.push(taskData);

    // 保存到本地存储
    localStorage.setItem('autoInfoTasks', JSON.stringify(tasks));

    // 重新渲染任务列表
    renderTaskList(tasks);
}

// 编辑任务
function editTask(index) {
    // 获取现有任务
    const tasks = JSON.parse(localStorage.getItem('autoInfoTasks')) || [];

    // 检查索引是否有效
    if (index >= 0 && index < tasks.length) {
        const task = tasks[index];

        // 填充表单
        const messageType = document.getElementById('messageType');
        const recipient = document.getElementById('recipient');
        const subject = document.getElementById('subject');
        const sendTime = document.getElementById('sendTime');
        const messageContent = document.getElementById('messageContent');
        const charCount = document.getElementById('charCount');
        const repeatTypeSelect = document.getElementById('repeatType');
        const repeatBtn = document.getElementById('repeatBtn');
        const customDays = document.getElementById('customDays');

        if (messageType && recipient && subject && sendTime && messageContent && charCount && repeatTypeSelect && repeatBtn && customDays) {
            messageType.value = task.messageType;
            recipient.value = task.recipient;
            subject.value = task.subject;
            sendTime.value = task.sendTime;
            messageContent.value = task.messageContent;
            charCount.textContent = task.messageContent.length + '/500';

            // 设置重复选项
            const repeatType = task.repeatType || 'none';
            repeatTypeSelect.value = repeatType;
            repeatBtn.innerHTML = getRepeatText(repeatType) + ' <span class="dropdown-icon"></span>';

            // 处理自定义重复日期
            if (repeatType === 'custom' && task.repeatDays) {
                customDays.style.display = 'block';
                // 勾选对应的日期
                document.querySelectorAll('input[name="repeatDays"]').forEach(checkbox => {
                    checkbox.checked = task.repeatDays.includes(checkbox.value);
                });
            } else {
                customDays.style.display = 'none';
            }

            // 删除原任务
            tasks.splice(index, 1);
            localStorage.setItem('autoInfoTasks', JSON.stringify(tasks));

            // 滚动到表单顶部
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });

            // 显示通知
            showNotification('任务已加载到编辑表单', 'info');
        }
    }
}

// 该函数不再使用，已移除

// 删除任务
function deleteTask(index) {
    // 获取现有任务
    const tasks = JSON.parse(localStorage.getItem('autoInfoTasks')) || [];

    // 检查索引是否有效
    if (index >= 0 && index < tasks.length) {
        // 删除任务
        tasks.splice(index, 1);

        // 保存到本地存储
        localStorage.setItem('autoInfoTasks', JSON.stringify(tasks));

        // 重新渲染任务列表
        renderTaskList(tasks);

        // 显示通知
        showNotification('任务已删除', 'success');
    }
}