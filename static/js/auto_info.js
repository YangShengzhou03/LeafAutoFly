// 修改createTaskItem函数，确保任务项样式正确
function createTaskItem(task) {
    const taskItem = document.createElement('div');
    taskItem.className = 'task-item animate-fade-in'; // 确保基础样式类存在
    taskItem.setAttribute('data-task-id', task.id);
    taskItem.style.opacity = '0'; // 初始隐藏以便动画
    taskItem.style.transition = 'opacity 0.5s ease'; // 添加过渡效果
    
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

    // 触发动画
    setTimeout(() => {
        taskItem.style.opacity = '1';
    }, 10);

    return taskItem;
}

// 修改renderTaskList函数，确保DOM操作正确
function renderTaskList(tasks) {
    try {
        const taskList = document.getElementById('taskList');
        const taskCount = document.getElementById('taskCount');
        const emptyTaskState = document.getElementById('emptyTaskState');

        if (!(taskList && taskCount && emptyTaskState)) {
            console.error('缺少必要的DOM元素');
            return;
        }

        // 清空任务列表
        taskList.innerHTML = '';

        // 更新任务计数
        taskCount.textContent = tasks.length;

        // 显示/隐藏空状态
        if (tasks.length === 0) {
            emptyTaskState.style.display = 'flex'; // 确保使用正确的display值
            return;
        } else {
            emptyTaskState.style.display = 'none';
        }

        // 按发送时间排序
        tasks.sort((a, b) => new Date(a.sendTime) - new Date(b.sendTime));

        // 渲染每个任务
        tasks.forEach(task => {
            const taskItem = createTaskItem(task);
            taskList.appendChild(taskItem);
        });

    } catch (error) {
        console.error('渲染任务列表时出错:', error);
        showNotification('渲染任务失败: ' + error.message, 'error');
    }
}

// 修改addTask函数，确保正确触发渲染
function addTask(taskData) {
    try {
        tasks.push(taskData);
        console.log('任务已添加:', taskData);
        
        // 强制刷新任务列表
        renderTaskList([...tasks]); // 使用新数组引用强制重渲染
        
        showNotification('任务创建成功', 'success');
    } catch (error) {
        console.error('添加任务时出错:', error);
        showNotification('添加任务失败: ' + error.message, 'error');
    }
}
