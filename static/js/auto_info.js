/**
 * 自动信息任务管理系统 - 优化版
 * 提供任务创建、列表管理、表单验证等功能
 */

document.addEventListener('DOMContentLoaded', function() {
    // 初始化所有功能
    initApp();
});

/**
 * 应用初始化函数
 * 统一管理所有初始化操作
 */
function initApp() {
    initValidation();
    initRepeatOptions();
    initCharCount();
    loadTasks();
    initThemeToggle();
}

/**
 * 表单验证初始化
 */
function initValidation() {
    const form = document.getElementById('taskForm');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // 获取表单数据
        const recipient = document.getElementById('recipient').value;
        const sendTime = document.getElementById('sendTime').value;
        const messageContent = document.getElementById('messageContent').value;
        const repeatType = document.getElementById('repeatType').value;

        // 基本验证
        const validationResult = validateForm(recipient, sendTime, messageContent, repeatType);

        if (validationResult.isValid) {
            // 准备任务数据
            const taskData = {
                id: Date.now().toString(),
                recipient: recipient,
                sendTime: sendTime,
                messageContent: messageContent,
                repeatType: repeatType,
                repeatDays: validationResult.repeatDays,
                status: 'pending',
                createdAt: new Date().toISOString()
            };

            // 添加任务
            addTask(taskData);

            // 重置表单
            resetForm(form);

            // 显示成功通知
            showNotification('任务创建成功', 'success');
        } else {
            // 显示错误通知
            showNotification(validationResult.errorMessage, 'error');
        }
    });

    // 重置按钮事件
    const resetBtn = document.getElementById('resetBtn');
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            resetForm(document.getElementById('taskForm'));
        });
    }
}

/**
 * 表单验证函数
 * @param {string} recipient - 接收者
 * @param {string} sendTime - 发送时间
 * @param {string} messageContent - 消息内容
 * @param {string} repeatType - 重复类型
 * @returns {Object} 验证结果
 */
function validateForm(recipient, sendTime, messageContent, repeatType) {
    let isValid = true;
    let errorMessage = '';
    let repeatDays = [];

    if (!recipient.trim()) {
        isValid = false;
        errorMessage += '请输入收件人\n';
    }

    if (!sendTime) {
        isValid = false;
        errorMessage += '请选择发送时间\n';
    } else if (new Date(sendTime) <= new Date()) {
        isValid = false;
        errorMessage += '发送时间必须晚于当前时间\n';
    }

    if (!messageContent.trim()) {
        isValid = false;
        errorMessage += '请输入消息内容\n';
    } else if (messageContent.length > 500) {
        isValid = false;
        errorMessage += '消息内容不能超过500个字符\n';
    }

    // 处理自定义重复选项
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

    return {
        isValid: isValid,
        errorMessage: errorMessage,
        repeatDays: repeatDays.length > 0 ? repeatDays : null
    };
}

/**
 * 重置表单
 * @param {HTMLFormElement} form - 表单元素
 */
function resetForm(form) {
    if (!form) return;

    form.reset();
    document.getElementById('charCount').textContent = '0/500';
    document.getElementById('customDays').style.display = 'none';
    document.getElementById('repeatBtn').innerHTML = '不重复 <span class="dropdown-icon"></span>';
    document.getElementById('repeatType').value = 'none';
}

/**
 * 初始化重复选项
 */
function initRepeatOptions() {
    const repeatBtn = document.getElementById('repeatBtn');
    const repeatOptions = document.getElementById('repeatOptions');
    const repeatType = document.getElementById('repeatType');
    const customDays = document.getElementById('customDays');

    if (!(repeatBtn && repeatOptions && repeatType && customDays)) return;

    // 切换下拉菜单显示/隐藏
    repeatBtn.addEventListener('click', function(e) {
        e.stopPropagation();
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
            customDays.style.display = selectedValue === 'custom' ? 'block' : 'none';
        });
    });
}

/**
 * 初始化字符计数
 */
function initCharCount() {
    const messageContent = document.getElementById('messageContent');
    const charCount = document.getElementById('charCount');

    if (!(messageContent && charCount)) return;

    messageContent.addEventListener('input', function() {
        const length = this.value.length;
        charCount.textContent = length + '/500';

        // 超过限制时改变颜色
        charCount.style.color = length > 500 ? 'var(--error-color)' : 'inherit';
    });
}

/**
 * 加载任务
 */
function loadTasks() {
    const tasks = JSON.parse(localStorage.getItem('autoInfoTasks')) || [];
    renderTaskList(tasks);
}

/**
 * 渲染任务列表
 * @param {Array} tasks - 任务数组
 */
function renderTaskList(tasks) {
    // 检查DOM元素是否存在
    const taskList = document.getElementById('taskList');
    const taskCount = document.getElementById('taskCount');
    const emptyTaskState = document.getElementById('emptyTaskState');

    if (!(taskList && taskCount && emptyTaskState)) {
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
        return;
    } else {
        emptyTaskState.style.display = 'none';
    }

    // 按发送时间排序（升序）
    tasks.sort((a, b) => new Date(a.sendTime) - new Date(b.sendTime));

    // 渲染每个任务
    tasks.forEach(task => {
        const taskItem = createTaskItem(task);
        taskList.appendChild(taskItem);
    });
}

/**
 * 创建任务项
 * @param {Object} task - 任务对象
 * @returns {HTMLElement} 任务项元素
 */
function createTaskItem(task) {
    const taskItem = document.createElement('div');
    taskItem.className = 'task-item animate-fade-in';
    taskItem.setAttribute('data-task-id', task.id);

    // 格式化日期
    const sendTime = new Date(task.sendTime);
    const formattedDate = `${sendTime.getFullYear()}-${padZero(sendTime.getMonth() + 1)}-${padZero(sendTime.getDate())} ${padZero(sendTime.getHours())}:${padZero(sendTime.getMinutes())}`;

    // 设置重复信息
    let repeatInfo = '不重复';
    if (task.repeatType === 'daily') {
        repeatInfo = '每天';
    } else if (task.repeatType === 'workday') {
        repeatInfo = '法定工作日';
    } else if (task.repeatType === 'holiday') {
        repeatInfo = '法定节假日';
    } else if (task.repeatType === 'custom' && task.repeatDays) {
        const daysMap = {'0': '周日', '1': '周一', '2': '周二', '3': '周三', '4': '周四', '5': '周五', '6': '周六'};
        repeatInfo = '每周: ' + task.repeatDays.map(day => daysMap[day]).join('、');
    }

    // 设置状态样式
    let statusClass = 'status-pending';
    let statusText = '待执行';
    if (task.status === 'completed') {
        statusClass = 'status-completed';
        statusText = '已执行';
    } else if (task.status === 'failed') {
        statusClass = 'status-failed';
        statusText = '执行失败';
    }

    taskItem.innerHTML = `
        <div class="task-content">
            <div class="task-header">
                <div class="task-title">${truncateText(task.messageContent, 30)}</div>
                <div class="status ${statusClass}">${statusText}</div>
            </div>
            <div class="task-body">
                <div class="task-recipient">收件人: ${task.recipient}</div>
                <div class="task-time">发送时间: ${formattedDate}</div>
                <div class="task-repeat">重复: ${repeatInfo}</div>
            </div>
        </div>
        <div class="task-actions">
            <button class="btn btn-outline-secondary edit-btn" data-id="${task.id}">编辑</button>
            <button class="btn btn-outline-secondary delete-btn" data-id="${task.id}">删除</button>
        </div>
    `;

    // 添加事件监听器
    const editBtn = taskItem.querySelector('.edit-btn');
    const deleteBtn = taskItem.querySelector('.delete-btn');

    if (editBtn) {
        editBtn.addEventListener('click', function() {
            editTask(task.id);
        });
    }

    if (deleteBtn) {
        deleteBtn.addEventListener('click', function() {
            deleteTask(task.id);
        });
    }

    return taskItem;
}

/**
 * 添加任务
 * @param {Object} taskData - 任务数据
 */
function addTask(taskData) {
    const tasks = JSON.parse(localStorage.getItem('autoInfoTasks')) || [];
    tasks.push(taskData);
    localStorage.setItem('autoInfoTasks', JSON.stringify(tasks));
    renderTaskList(tasks);
}

/**
 * 编辑任务
 * @param {string} taskId - 任务ID
 */
function editTask(taskId) {
    const tasks = JSON.parse(localStorage.getItem('autoInfoTasks')) || [];
    const task = tasks.find(t => t.id === taskId);

    if (!task) return;

    // 填充表单
    document.getElementById('recipient').value = task.recipient;
    document.getElementById('sendTime').value = task.sendTime;
    document.getElementById('messageContent').value = task.messageContent;
    document.getElementById('repeatType').value = task.repeatType;

    // 更新字符计数
    document.getElementById('charCount').textContent = task.messageContent.length + '/500';

    // 处理重复选项
    const repeatBtn = document.getElementById('repeatBtn');
    const customDays = document.getElementById('customDays');

    if (task.repeatType === 'custom' && task.repeatDays) {
        customDays.style.display = 'block';
        repeatBtn.innerHTML = '自定义 <span class="dropdown-icon"></span>';

        // 选中对应的日期
        task.repeatDays.forEach(day => {
            const checkbox = document.querySelector(`input[name="repeatDays"][value="${day}"]`);
            if (checkbox) checkbox.checked = true;
        });
    } else {
        customDays.style.display = 'none';
        const repeatTextMap = {
            'none': '不重复',
            'daily': '每天',
            'workday': '法定工作日',
            'holiday': '法定节假日'
        };
        repeatBtn.innerHTML = repeatTextMap[task.repeatType] + ' <span class="dropdown-icon"></span>';
    }

    // 删除原任务
    deleteTask(taskId);
}

/**
 * 删除任务
 * @param {string} taskId - 任务ID
 */
function deleteTask(taskId) {
    let tasks = JSON.parse(localStorage.getItem('autoInfoTasks')) || [];
    tasks = tasks.filter(task => task.id !== taskId);
    localStorage.setItem('autoInfoTasks', JSON.stringify(tasks));
    renderTaskList(tasks);
    showNotification('任务已删除', 'info');
}

/**
 * 显示通知
 * @param {string} message - 通知消息
 * @param {string} type - 通知类型 (success, error, info)
 */
function showNotification(message, type) {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} animate-fade-in`;
    notification.textContent = message;

    // 添加到页面
    document.body.appendChild(notification);

    // 自动移除
    setTimeout(() => {
        notification.classList.add('animate-fade-out');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

/**
 * 数字补零
 * @param {number} num - 数字
 * @returns {string} 补零后的字符串
 */
function padZero(num) {
    return num < 10 ? '0' + num : num;
}

/**
 * 截断文本
 * @param {string} text - 文本
 * @param {number} maxLength - 最大长度
 * @returns {string} 截断后的文本
 */
function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

/**
 * 初始化主题切换
 */
function initThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    if (!themeToggle) return;

    // 检查本地存储中的主题偏好
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark-mode');
        themeToggle.checked = true;
    }

    // 添加切换事件
    themeToggle.addEventListener('change', function() {
        if (this.checked) {
            document.documentElement.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark-mode');
            localStorage.setItem('theme', 'light');
        }
    });
}