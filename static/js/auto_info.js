// 全局任务数组 - 仅在内存中存储，不使用localStorage
let tasks = [];
let taskIdCounter = 1;

// 确保DOM完全加载后再执行代码
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    // 初始渲染空任务列表
    renderTaskList(tasks);
    
    // 设置默认时间为当前时间
    const now = new Date();
    // 取整到分钟
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset(), 0, 0);
    document.getElementById('sendTime').value = now.toISOString().slice(0, 16);
});

// 添加任务函数 - 仅操作内存数据
function addTask(taskData) {
    try {
        // 生成唯一ID
        const newTask = {
            id: taskIdCounter++,
            ...taskData,
            status: 'pending', // 默认状态
            createdAt: new Date().toISOString()
        };
        
        tasks.push(newTask);
        console.log('任务已添加:', newTask);
        
        // 刷新任务列表（无页面刷新）
        renderTaskList([...tasks]);
        showNotification('任务创建成功', 'success');
        
        // 清空表单
        document.getElementById('taskForm').reset();
        document.getElementById('repeatType').value = 'none';
        document.getElementById('repeatBtn').firstChild.textContent = '不重复 ';
        document.getElementById('customDays').style.display = 'none';
        
        // 重新设置默认时间
        const now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset(), 0, 0);
        document.getElementById('sendTime').value = now.toISOString().slice(0, 16);
    } catch (error) {
        console.error('添加任务时出错:', error);
        showNotification('添加任务失败: ' + error.message, 'error');
    }
}

// 删除任务函数 - 仅操作内存数据
function deleteTask(taskId) {
    if (confirm('确定要删除这个任务吗？')) {
        try {
            // 找到要删除的任务元素并添加动画
            const taskElement = document.querySelector(`[data-task-id="${taskId}"]`);
            if (taskElement) {
                taskElement.classList.add('task-remove-animation');
                
                // 等待动画完成后再移除数据
                setTimeout(() => {
                    // 从内存数组中删除任务
                    tasks = tasks.filter(task => task.id !== taskId);
                    // 刷新任务列表
                    renderTaskList([...tasks]);
                    showNotification('任务删除成功', 'success');
                }, 300);
            }
        } catch (error) {
            console.error('删除任务时出错:', error);
            showNotification('删除任务失败: ' + error.message, 'error');
        }
    }
}

// 创建单个任务项元素
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
    else if (task.repeatType === 'custom') {
        repeatText = `自定义: ${task.repeatDays?.join(', ') || ''}`;
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

// 渲染任务列表
function renderTaskList(tasks) {
    try {
        const taskList = document.getElementById('taskList');
        const taskCount = document.getElementById('taskCount');
        const emptyState = document.getElementById('emptyState');

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

// 辅助函数：数字补零
function padZero(num) {
    return num < 10 ? '0' + num : num;
}

// 辅助函数：防止XSS攻击
function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// 显示通知提示
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `notification ${type} task-transition`;
    notification.textContent = message;
    
    // 添加到页面
    document.body.appendChild(notification);
    
    // 显示通知（触发动画）
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // 3秒后自动消失
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// 表单提交事件监听
document.addEventListener('DOMContentLoaded', function() {
    // 添加表单提交处理
    const taskForm = document.getElementById('taskForm');
    if (taskForm) {
        taskForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
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
        });
    }
    
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
            document.getElementById('taskForm').reset();
            document.getElementById('repeatType').value = 'none';
            document.getElementById('repeatBtn').firstChild.textContent = '不重复 ';
            document.getElementById('customDays').style.display = 'none';
            
            // 重新设置默认时间
            const now = new Date();
            now.setMinutes(now.getMinutes() - now.getTimezoneOffset(), 0, 0);
            document.getElementById('sendTime').value = now.toISOString().slice(0, 16);
        });
    }
});
