// 自动信息任务管理基础功能

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 初始化功能
    initRepeatOptions();
    initAddTask();
    initTaskActions();
});

// 优化的重复选项功能
function initRepeatOptions() {
    const repeatBtn = document.querySelector('.repeat-btn');
    const repeatOptions = document.querySelector('.repeat-options');
    const currentRepeat = document.querySelector('.current-repeat');
    const repeatOptionItems = document.querySelectorAll('.repeat-option');
    const customDays = document.querySelector('.custom-days');
    const confirmCustom = document.querySelector('.confirm-custom');

    if (repeatBtn && repeatOptions) {
        // 点击按钮切换下拉菜单
        repeatBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            repeatOptions.style.display = repeatOptions.style.display === 'block' ? 'none' : 'block';
        });

        // 点击页面其他地方关闭下拉菜单
        document.addEventListener('click', function() {
            repeatOptions.style.display = 'none';
            if (customDays) {
                customDays.style.display = 'none';
            }
        });

        // 阻止下拉菜单内部点击事件冒泡
        repeatOptions.addEventListener('click', function(e) {
            e.stopPropagation();
        });

        // 重复选项点击事件
        if (repeatOptionItems.length > 0 && currentRepeat) {
            repeatOptionItems.forEach(item => {
                item.addEventListener('click', function() {
                    const value = this.getAttribute('data-value');
                    currentRepeat.textContent = this.textContent;
                    repeatOptions.style.display = 'none';

                    if (customDays) {
                        customDays.style.display = value === 'custom' ? 'block' : 'none';
                    }
                });
            });
        }

        // 确认自定义重复
        if (confirmCustom && currentRepeat && customDays) {
            confirmCustom.addEventListener('click', function() {
                const checkedDays = document.querySelectorAll('.day-selector input:checked');
                const dayLabels = Array.from(checkedDays).map(checkbox => {
                    return checkbox.parentElement.textContent.trim();
                });

                if (dayLabels.length > 0) {
                    currentRepeat.textContent = '自定义 (' + dayLabels.join(', ') + ')';
                } else {
                    currentRepeat.textContent = '不重复';
                }
                customDays.style.display = 'none';
            });
        }
    }
}

// 添加任务功能
function initAddTask() {
    const addTaskBtn = document.getElementById('add-task-btn');
    const taskList = document.getElementById('taskList');
    const messageContent = document.getElementById('messageContent');
    const charCount = document.getElementById('charCount');
    const recipient = document.getElementById('recipient');
    const messageContentError = document.getElementById('messageContentError');
    const recipientError = document.getElementById('recipientError');

    // 添加字数统计功能
    if (messageContent && charCount) {
        messageContent.addEventListener('input', function() {
            const count = this.value.length;
            charCount.textContent = `${count}/500`;
            if (count > 500) {
                charCount.style.color = '#dc3545';
                this.value = this.value.substring(0, 500);
                charCount.textContent = '500/500';
            } else {
                charCount.style.color = '#666666';
            }
        });
    }

    if (addTaskBtn && taskList) {
        addTaskBtn.addEventListener('click', function() {
            let isValid = true;

            // 验证消息内容
            if (messageContent && !messageContent.value.trim()) {
                showError(messageContent, messageContentError, '请填写消息内容');
                isValid = false;
            } else if (messageContent && messageContent.value.length > 500) {
                showError(messageContent, messageContentError, '消息内容不能超过500字');
                isValid = false;
            } else {
                hideError(messageContent, messageContentError);
            }

            // 验证接收者
            if (recipient && !recipient.value.trim()) {
                showError(recipient, recipientError, '请填写信息接收者');
                isValid = false;
            } else if (recipient && recipient.value.trim() && !validateRecipient(recipient.value.trim())) {
                showError(recipient, recipientError, '请输入正确的11位手机号或联系人姓名');
                isValid = false;
            } else {
                hideError(recipient, recipientError);
            }

            if (!isValid) return;

            // 获取表单数据
            // 获取表单数据
            const messageContent = document.getElementById('messageContent')?.value || '';
            const sendTime = document.getElementById('sendTime')?.value || '';
            const recipient = document.getElementById('recipient')?.value || '';
            const repeatOption = document.querySelector('.current-repeat')?.textContent || '不重复';

            // 简单验证
            if (!messageContent.trim()) {
                alert('请填写消息内容');
                return;
            }

            if (!sendTime) {
                alert('请设置发送时间');
                return;
            }

            if (!recipient.trim()) {
                alert('请填写信息接收者');
                return;
            }

            // 隐藏空状态
            const emptyState = document.querySelector('.empty-task-state');
            if (emptyState) {
                emptyState.remove();
            }

            // 创建任务项
            const taskItem = document.createElement('div');
            taskItem.className = 'task-item card-shadow p-3 mb-3';
            const taskTitle = '文本消息';
            let contentPreview = messageContent.substring(0, 50);
            if (messageContent.length > 50) {
                contentPreview += '...';
            }

            taskItem.innerHTML = `
                <div class="task-header d-flex justify-content-between">
                    <h3 class="task-title">${taskTitle}</h3>
                    <span class="task-status enabled">已启用</span>
                </div>
                <div class="task-content mt-2">
                    <p>${contentPreview}</p>
                    <p class="task-time">发送时间: ${new Date(sendTime).toLocaleString()}</p>
                    <p class="task-repeat">重复: ${repeatOption}</p>
                </div>
                <div class="task-actions mt-3 d-flex justify-content-end gap-2">
                    <button class="btn btn-sm btn-outline-primary edit-task">编辑</button>
                    <button class="btn btn-sm btn-outline-danger delete-task">删除</button>
                </div>
            `;

            // 添加到任务列表
            taskList.appendChild(taskItem);

            // 清空表单
            if (document.getElementById('messageContent')) {
                document.getElementById('messageContent').value = '';
            }
            if (document.getElementById('filePath')) {
                document.getElementById('filePath').value = '';
            }

            // 为删除按钮添加事件
            const deleteBtn = taskItem.querySelector('.delete-task');
            if (deleteBtn) {
                deleteBtn.addEventListener('click', function() {
                    taskItem.remove();

                    // 如果任务列表为空，显示空状态
                    if (taskList.children.length === 0) {
                        taskList.innerHTML = `
                            <div class="empty-task-state">
                                <img src="${window.location.origin}/static/images/empty-tasks.svg" alt="暂无任务" class="empty-state-image">
                                <h3 class="empty-state-title">暂无任务</h3>
                                <p class="empty-state-description">点击上方"添加任务"按钮创建新任务</p>
                                <button class="btn btn-primary mt-3" id="createFirstTaskBtn">创建第一个任务</button>
                            </div>
                        `;

                        // 绑定创建第一个任务按钮事件
                        const createFirstTaskBtn = document.getElementById('createFirstTaskBtn');
                        if (createFirstTaskBtn) {
                            createFirstTaskBtn.addEventListener('click', function() {
                                // 这里可以滚动到添加任务区域
                                document.querySelector('.task-creation-card')?.scrollIntoView({ behavior: 'smooth' });
                            });
                        }
                    }
                });
            }

            // 为编辑按钮添加事件
            const editBtn = taskItem.querySelector('.edit-task');
            if (editBtn) {
                editBtn.addEventListener('click', function() {
                    alert('编辑功能将在后续实现');
                });
            }
        });
    }
}

// 任务操作功能
function initTaskActions() {
    // 开始执行所有任务按钮
    const startAllTasksBtn = document.getElementById('startAllTasksBtn');
    if (startAllTasksBtn) {
        startAllTasksBtn.addEventListener('click', function() {
            alert('开始执行所有任务');
            // 实际应用中这里会发送请求到后端执行任务
        });
    }

    // 导入导出任务按钮
    const importTasksBtn = document.getElementById('importTasksBtn');
    const exportTasksBtn = document.getElementById('exportTasksBtn');

    if (importTasksBtn) {
        importTasksBtn.addEventListener('click', function() {
            alert('导入任务功能将在后续实现');
        });
    }

    if (exportTasksBtn) {
        exportTasksBtn.addEventListener('click', function() {
            alert('导出任务功能将在后续实现');
        });
    }

    // 创建第一个任务按钮
    const createFirstTaskBtn = document.getElementById('createFirstTaskBtn');
    if (createFirstTaskBtn) {
        createFirstTaskBtn.addEventListener('click', function() {
            document.querySelector('.task-creation-card')?.scrollIntoView({ behavior: 'smooth' });
        });
    }
}