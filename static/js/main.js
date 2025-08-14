// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化任务列表交互
    initTaskList();
    initAutoInfoTaskList();

    // 处理按钮点击态

    // 处理按钮点击态，排除升级专业版按钮
const buttons = document.querySelectorAll('button:not(.upgrade-btn)');
buttons.forEach(button => {
    button.addEventListener('mousedown', function() {
        this.style.transform = 'translateY(2px)';
    });
    button.addEventListener('mouseup', function() {
        this.style.transform = 'translateY(0)';
    });
    button.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});

    // 处理执行按钮的加载态
    const executeButtons = document.querySelectorAll('.execute-btn');
    executeButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('loading')) {
                this.classList.add('loading');
                this.textContent = '执行中...';
                this.disabled = true;

                // 模拟加载完成
                setTimeout(() => {
                    this.classList.remove('loading');
                    this.textContent = '开始执行';
                    this.disabled = false;
                }, 2000);
            }
        });
    });

    // 处理重复周期选择器
    const repeatBtns = document.querySelectorAll('.repeat-btn');
    repeatBtns.forEach(btn => {
        const currentRepeat = btn.querySelector('.current-repeat');
        const repeatOptions = btn.nextElementSibling;
        const repeatItems = repeatOptions.querySelectorAll('.repeat-option');
        const customRepeat = repeatOptions.querySelector('.custom-repeat');
        const customDays = repeatOptions.querySelector('.custom-days');
        const confirmCustom = repeatOptions.querySelector('.confirm-custom');
        const dayCheckboxes = customDays.querySelectorAll('.day-selector input');

        // 点击重复选项
        repeatItems.forEach(item => {
            item.addEventListener('click', function() {
                const value = this.getAttribute('data-value');
                let text = this.textContent;

                if (value === 'custom') {
                    customDays.style.display = 'block';
                } else {
                    customDays.style.display = 'none';
                    currentRepeat.textContent = text;
                }
            });
        });

        // 确认自定义选择
        confirmCustom.addEventListener('click', function() {
            const selectedDays = Array.from(dayCheckboxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.parentElement.textContent.trim());

            if (selectedDays.length > 0) {
                currentRepeat.textContent = selectedDays.join('、');
            } else {
                currentRepeat.textContent = '仅一次';
            }
            customDays.style.display = 'none';
        });
    });
});

// 初始化任务列表交互
function initTaskList() {
    // 任务项点击反馈
    const taskItems = document.querySelectorAll('.task-item');
    taskItems.forEach(item => {
        // 点击效果
        item.addEventListener('mousedown', function() {
            this.style.transform = 'scale(0.98)';
        });
        item.addEventListener('mouseup', function() {
            this.style.transform = 'scale(1)';
        });
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });

        // 点击展开详情
        item.addEventListener('click', function(e) {
            // 避免点击复选框或按钮时触发展开
            if (e.target.classList.contains('task-checkbox') || e.target.classList.contains('action-btn')) {
                return;
            }

            const detail = this.nextElementSibling;
            if (detail && detail.classList.contains('task-detail')) {
                detail.style.maxHeight = detail.style.maxHeight ? null : detail.scrollHeight + 'px';
            }
        });
    });

    // 批量选择功能
    const checkboxes = document.querySelectorAll('.task-checkbox');
    const batchActions = document.querySelector('.batch-actions');

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const checkedCount = document.querySelectorAll('.task-checkbox:checked').length;

            if (checkedCount > 0) {
                batchActions.classList.add('visible');
            } else {
                batchActions.classList.remove('visible');
            }
        });
    });

    // 全选功能
    const selectAll = document.querySelector('.select-all');
    if (selectAll) {
        selectAll.addEventListener('change', function() {
            checkboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });

            if (this.checked) {
                batchActions.classList.add('visible');
            } else {
                batchActions.classList.remove('visible');
            }
        });
    }

    // 批量删除功能
    const deleteSelected = document.querySelector('.delete-selected');
    if (deleteSelected) {
        deleteSelected.addEventListener('click', function() {
            const checkedItems = document.querySelectorAll('.task-checkbox:checked');
            checkedItems.forEach(checkbox => {
                const taskItem = checkbox.closest('.task-item');
                const detail = taskItem.nextElementSibling;

                // 添加删除动画
                taskItem.style.height = taskItem.offsetHeight + 'px';
                taskItem.style.overflow = 'hidden';
                taskItem.style.transition = 'all 0.3s';
                taskItem.style.opacity = '0';
                taskItem.style.transform = 'translateX(-20px)';

                setTimeout(() => {
                    taskItem.remove();
                    if (detail && detail.classList.contains('task-detail')) {
                        detail.remove();
                    }
                    batchActions.classList.remove('visible');
                }, 300);
            });
        });
    }

    // 批量启动功能
    const startSelected = document.querySelector('.start-selected');
    if (startSelected) {
        startSelected.addEventListener('click', function() {
            const checkedItems = document.querySelectorAll('.task-checkbox:checked');
            checkedItems.forEach(checkbox => {
                const taskItem = checkbox.closest('.task-item');
                const statusIcon = taskItem.querySelector('.status-icon');
                const statusText = taskItem.querySelector('.status-text');

                // 更新状态
                statusIcon.textContent = '🔄';
                statusIcon.style.animation = 'spin 1s linear infinite';
                statusText.textContent = '执行中';
                statusText.classList.remove('status-pending', 'status-completed', 'status-failed', 'status-paused');
                statusText.classList.add('status-running');
            });
            batchActions.classList.remove('visible');
        });
    }
}

// 初始化自动信息页面的任务列表
function initAutoInfoTaskList() {
    const taskList = document.getElementById('taskList');
    const addTaskBtn = document.getElementById('add-task-btn');
    const emptyState = document.querySelector('.empty-task-state');

    // 检查任务列表是否存在
    if (!taskList) return;

    // 加载本地存储中的任务
    loadAutoInfoTasks();

    // 添加任务按钮事件
    if (addTaskBtn) {
        addTaskBtn.addEventListener('click', function() {
            const messageInput = document.querySelector('.message-input');
            const datetimeInput = document.querySelector('.datetime-input');
            const repeatBtn = document.querySelector('.repeat-btn');
            const currentRepeat = repeatBtn ? repeatBtn.querySelector('.current-repeat') : null;

            const taskText = messageInput.value.trim();
            const taskTime = datetimeInput.value;
            const repeatValue = currentRepeat ? currentRepeat.textContent : '仅一次';

            if (!taskText || !taskTime) {
                alert('请输入消息内容和时间');
                return;
            }

            // 创建新任务
            const task = {
                id: Date.now(),
                text: taskText,
                time: taskTime,
                repeat: repeatValue,
                createdAt: new Date().toISOString()
            };

            // 添加任务到列表
            addAutoInfoTask(task);

            // 保存任务到本地存储
            saveAutoInfoTasks();

            // 清空输入框
            messageInput.value = '';
        });
    }

    // 添加任务到列表
    function addAutoInfoTask(task) {
        // 隐藏空状态
        if (emptyState) {
            emptyState.style.display = 'none';
        }

        // 创建任务项
        const taskItem = document.createElement('div');
        taskItem.className = 'task-item';
        taskItem.dataset.id = task.id;

        // 格式化时间
        const date = new Date(task.time);
        const formattedDate = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
        const formattedTime = `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;

        // 设置任务项内容
        taskItem.innerHTML = `
            <div class="task-info">
                <div class="task-title">${task.text}</div>
                <div class="task-time">
                    时间: ${formattedDate} ${formattedTime} | 重复: ${task.repeat}
                </div>
            </div>
            <div class="task-actions">
                <button class="task-action-btn edit"><i class="edit-icon"></i></button>
                <button class="task-action-btn delete"><i class="delete-icon"></i></button>
            </div>
        `;

        // 添加删除按钮事件
        const deleteBtn = taskItem.querySelector('.task-action-btn.delete');
        deleteBtn.addEventListener('click', function() {
            // 添加删除动画
            taskItem.style.height = taskItem.offsetHeight + 'px';
            taskItem.style.overflow = 'hidden';
            taskItem.style.transition = 'all 0.3s';
            taskItem.style.opacity = '0';
            taskItem.style.transform = 'translateX(-20px)';

            setTimeout(() => {
                taskItem.remove();
                saveAutoInfoTasks();

                // 检查是否还有任务
                const taskItems = document.querySelectorAll('.task-item');
                if (taskItems.length === 0 && emptyState) {
                    emptyState.style.display = 'flex';
                }
            }, 300);
        });

        // 添加编辑按钮事件
        const editBtn = taskItem.querySelector('.task-action-btn.edit');
        editBtn.addEventListener('click', function() {
            const messageInput = document.querySelector('.message-input');
            const datetimeInput = document.querySelector('.datetime-input');
            const repeatBtn = document.querySelector('.repeat-btn');
            const currentRepeat = repeatBtn ? repeatBtn.querySelector('.current-repeat') : null;

            if (messageInput && datetimeInput && currentRepeat) {
                // 填充表单
                messageInput.value = task.text;
                datetimeInput.value = task.time;
                currentRepeat.textContent = task.repeat;

                // 删除原任务
                taskItem.remove();
                saveAutoInfoTasks();

                // 检查是否还有任务
                const taskItems = document.querySelectorAll('.task-item');
                if (taskItems.length === 0 && emptyState) {
                    emptyState.style.display = 'flex';
                }
            }
        });

        // 添加到任务列表
        taskList.insertBefore(taskItem, emptyState);

        // 添加点击效果
        taskItem.addEventListener('mousedown', function() {
            this.style.transform = 'scale(0.98)';
        });
        taskItem.addEventListener('mouseup', function() {
            this.style.transform = 'scale(1)';
        });
        taskItem.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    }

    // 保存任务到本地存储
    function saveAutoInfoTasks() {
        const tasks = [];
        const taskItems = document.querySelectorAll('.task-item');

        taskItems.forEach(item => {
            const taskTime = item.querySelector('.task-time').textContent;
            const repeatIndex = taskTime.indexOf('重复: ');
            const repeatValue = repeatIndex !== -1 ? taskTime.substring(repeatIndex + 4) : '仅一次';

            tasks.push({
                id: parseInt(item.dataset.id),
                text: item.querySelector('.task-title').textContent,
                time: item.dataset.time || '',
                repeat: repeatValue
            });
        });

        localStorage.setItem('autoInfoTasks', JSON.stringify(tasks));
    }

    // 从本地存储加载任务
    function loadAutoInfoTasks() {
        const tasks = JSON.parse(localStorage.getItem('autoInfoTasks') || '[]');

        if (tasks.length > 0) {
            // 隐藏空状态
            if (emptyState) {
                emptyState.style.display = 'none';
            }

            // 添加任务到列表
            tasks.forEach(task => {
                addAutoInfoTask(task);
            });
        }
    }
}

// 添加CSS动画
const style = document.createElement('style');
style.textContent = `
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* 编辑和删除图标样式 */
.edit-icon::before {
    content: '✏️';
}

.delete-icon::before {
    content: '🗑️';
}
`;
document.head.appendChild(style);