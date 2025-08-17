function ensureFormBinding() {
    const taskForm = document.getElementById('taskForm');
    const submitBtn = document.getElementById('submitBtn');
    
    if (taskForm && submitBtn) {
        console.log('表单元素已找到，开始绑定事件');
        
        taskForm.removeEventListener('submit', handleFormSubmit);
        submitBtn.removeEventListener('click', handleSubmitClick);
        
        taskForm.addEventListener('submit', handleFormSubmit);
        submitBtn.addEventListener('click', handleSubmitClick);
        
        console.log('表单提交事件已绑定');
        return true;
    } else {
        console.log('表单元素尚未准备好，将重试...');
        return false;
    }
}

function handleSubmitClick(e) {
    console.log('提交按钮点击事件触发');
    e.preventDefault();
    e.stopPropagation();
    
    const taskForm = document.getElementById('taskForm');
    if (taskForm) {
        const submitEvent = new Event('submit', {cancelable: true, bubbles: true});
        taskForm.dispatchEvent(submitEvent);
    }
}

function initForm() {
    console.log('初始化表单');
    
    if (!ensureFormBinding()) {
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
    
    loadTasks();
    
    handleUrlParams();
    
    function setDefaultTime() {
        const now = new Date();

        console.log("加载啦")
        
        const date = now.toISOString().split('T')[0];
        
        const time = now.toTimeString().split(' ')[0].slice(0, 5);
        
        const defaultDateTime = `${date}T${time}`;
        
        const sendTimeInput = document.getElementById('sendTime');
        if (sendTimeInput) {
            sendTimeInput.value = defaultDateTime;
        }
    }

    setDefaultTime();
}

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

function handleUrlParams() {
    const params = new URLSearchParams(window.location.search);
    if (params.has('recipient') && params.has('sendTime') && params.has('messageContent')) {
        const taskData = {
            recipient: params.get('recipient'),
            sendTime: params.get('sendTime'),
            repeatType: params.get('repeatType') || 'none',
            messageContent: params.get('messageContent')
        };
        
        document.getElementById('recipient').value = taskData.recipient;
        document.getElementById('sendTime').value = taskData.sendTime;
        document.getElementById('repeatType').value = taskData.repeatType;
        document.getElementById('messageContent').value = taskData.messageContent;
        
        if (params.has('repeatDays')) {
            const repeatDays = params.get('repeatDays').split(',');
            repeatDays.forEach(day => {
                const checkbox = document.querySelector(`input[name="repeatDays"][value="${day}"]`);
                if (checkbox) checkbox.checked = true;
            });
        }
        
        const repeatBtn = document.getElementById('repeatBtn');
        const repeatOptions = document.querySelectorAll('.repeat-option');
        repeatOptions.forEach(option => {
            if (option.getAttribute('data-repeat') === taskData.repeatType) {
                repeatBtn.firstChild.textContent = option.textContent + ' ';
            }
        });
        
        document.getElementById('customDays').style.display =
            taskData.repeatType === 'custom' ? 'block' : 'none';
    }
}

document.addEventListener('DOMContentLoaded', initForm);

window.addEventListener('load', initForm);

function handleFormSubmit(e) {
    console.log('表单提交事件触发');
    e.preventDefault();
    e.stopPropagation();
    
    const formData = {
        recipient: document.getElementById('recipient').value,
        sendTime: document.getElementById('sendTime').value,
        repeatType: document.getElementById('repeatType').value,
        messageContent: document.getElementById('messageContent').value
    };
    
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

function addTask(taskData) {
    try {
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
            
            fetch('/api/tasks')
            .then(response => response.json())
            .then(tasks => {
                renderTaskList(tasks);
                showNotification('任务创建成功', 'success');
            });
            
            const taskForm = document.getElementById('taskForm');
            if (taskForm) taskForm.reset();
            
            document.getElementById('repeatType').value = 'none';
            document.getElementById('repeatBtn').firstChild.textContent = '不重复 ';
            document.getElementById('customDays').style.display = 'none';
            
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

function deleteTask(taskId) {
    if (confirm('确定要删除这个任务吗？')) {
        try {
            const taskElement = document.querySelector(`[data-task-id="${taskId}"]`);
            if (taskElement) {
                taskElement.classList.add('task-remove-animation');
                
                setTimeout(() => {
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
                        fetch('/api/tasks')
                        .then(response => response.json())
                        .then(tasks => {
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

function createTaskItem(task) {
    const li = document.createElement('li');
    li.className = 'task-item task-transition';
    li.dataset.taskId = task.id;
    
    const sendTime = new Date(task.sendTime);
    const formattedTime = `${sendTime.getFullYear()}-${padZero(sendTime.getMonth() + 1)}-${padZero(sendTime.getDate())} ${padZero(sendTime.getHours())}:${padZero(sendTime.getMinutes())}`;
    
    let repeatText = '不重复';
    if (task.repeatType === 'daily') repeatText = '每天';
    else if (task.repeatType === 'weekly') repeatText = '每周';
    else if (task.repeatType === 'monthly') repeatText = '每月';
    else if (task.repeatType === 'workday') repeatText = '法定工作日';
    else if (task.repeatType === 'holiday') repeatText = '法定节假日';
    else if (task.repeatType === 'custom') {
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

function renderTaskList(tasks) {
    try {
        const taskList = document.getElementById('taskList');
        const taskCount = document.getElementById('taskCount');
        const emptyState = document.getElementById('emptyTaskState');

        if (!(taskList && taskCount && emptyState)) {
            console.error('缺少必要的DOM元素: taskList, taskCount或emptyState');
            return;
        }

        const itemsToRemove = taskList.querySelectorAll('.task-item:not(.task-remove-animation)');
        itemsToRemove.forEach(item => item.remove());

        taskCount.textContent = tasks.length;

        emptyState.style.display = tasks.length === 0 ? 'flex' : 'none';

        const sortedTasks = [...tasks].sort((a, b) => new Date(a.sendTime) - new Date(b.sendTime));
        
        sortedTasks.forEach(task => {
            const taskItem = createTaskItem(task);
            taskList.appendChild(taskItem);
        });

    } catch (error) {
        console.error('渲染任务列表时出错:', error);
    }
}

function padZero(num) {
    return num < 10 ? '0' + num : num;
}

function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type} task-transition`;
    notification.textContent = message;
    
    const notificationContainer = document.getElementById('notificationContainer');
    if (notificationContainer) {
        notificationContainer.appendChild(notification);
    } else {
        document.body.appendChild(notification);
    }
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

function setDefaultTime() {
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset(), 0, 0);
    document.getElementById('sendTime').value = now.toISOString().slice(0, 16);
}

document.addEventListener('DOMContentLoaded', function() {
    const repeatBtn = document.getElementById('repeatBtn');
    const repeatOptions = document.getElementById('repeatOptions');
    if (repeatBtn && repeatOptions) {
        repeatBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            repeatOptions.style.display = repeatOptions.style.display === 'none' ? 'block' : 'none';
        });
        
        document.addEventListener('click', (e) => {
            if (!repeatBtn.contains(e.target) && !repeatOptions.contains(e.target)) {
                repeatOptions.style.display = 'none';
            }
        });
        
        document.querySelectorAll('.repeat-option').forEach(option => {
            option.addEventListener('click', function() {
                const repeatType = this.getAttribute('data-repeat');
                document.getElementById('repeatType').value = repeatType;
                repeatBtn.firstChild.textContent = this.textContent + ' ';
                repeatOptions.style.display = 'none';
                
                document.getElementById('customDays').style.display =
                    repeatType === 'custom' ? 'block' : 'none';
            });
        });
    }
    
    const resetBtn = document.getElementById('resetBtn');
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            const taskForm = document.getElementById('taskForm');
            if (taskForm) taskForm.reset();
            
            document.getElementById('repeatType').value = 'none';
            document.getElementById('repeatBtn').firstChild.textContent = '不重复 ';
            document.getElementById('customDays').style.display = 'none';
            
            setDefaultTime();
        });
    }
    
    const messageContent = document.getElementById('messageContent');
    const charCount = document.getElementById('charCount');
    if (messageContent && charCount) {
        messageContent.addEventListener('input', function() {
            charCount.textContent = `${this.value.length}/500`;
            if (this.value.length > 500) {
                this.value = this.value.substring(0, 500);
                charCount.textContent = `500/500`;
            } else {
                charCount.style.color = '';
            }
        });
    }
});
