// 自动信息任务管理增强功能

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 初始化重复选项增强功能
    initEnhancedRepeatOptions();

    // 初始化其他新功能
    initOtherFeatures();
});

// 重复选项增强功能
function initEnhancedRepeatOptions() {
    const repeatBtn = document.querySelector('.repeat-btn');
    const currentRepeat = repeatBtn ? repeatBtn.querySelector('.current-repeat') : null;
    const repeatOptions = document.querySelector('.repeat-options');
    const customRepeat = document.querySelector('.repeat-option.custom-repeat');
    const customDays = document.querySelector('.custom-days');
    const confirmCustom = document.querySelector('.confirm-custom');

    if (repeatBtn && currentRepeat && repeatOptions && customRepeat && customDays && confirmCustom) {
        // 点击自定义重复选项
        customRepeat.addEventListener('click', function(e) {
            e.stopPropagation();
            customDays.style.display = 'block';
        });

        // 确认自定义重复
        confirmCustom.addEventListener('click', function(e) {
            e.stopPropagation();

            const selectedDays = Array.from(document.querySelectorAll('.day-selector input[type="checkbox"]:checked'))
                .map(checkbox => checkbox.nextElementSibling.textContent.trim());

            const interval = document.getElementById('customInterval').value;
            const intervalType = document.getElementById('intervalType').value;

            let repeatText = '';

            if (selectedDays.length > 0) {
                // 按天重复
                repeatText = `每 ${interval} ${getIntervalText(intervalType)} 的 ${selectedDays.join('、')}`;
            } else {
                // 按间隔重复
                repeatText = `每 ${interval} ${getIntervalText(intervalType)}`;
            }

            currentRepeat.textContent = repeatText;
            customDays.style.display = 'none';
            repeatOptions.style.display = 'none';
        });
    }
}

// 获取间隔文本
function getIntervalText(type) {
    const intervalMap = {
        'days': '天',
        'weeks': '周',
        'months': '月',
        'years': '年'
    };
    return intervalMap[type] || '天';
}

// 初始化其他新功能
function initOtherFeatures() {
    // 停止所有任务按钮
    const stopAllTasksBtn = document.getElementById('stopAllTasksBtn');
    if (stopAllTasksBtn) {
        stopAllTasksBtn.addEventListener('click', function() {
            const runningTasks = document.querySelectorAll('.task-item[data-status="running"]');

            if (runningTasks.length === 0) {
                showNotification('没有正在运行的任务', 'info');
                return;
            }

            runningTasks.forEach(task => {
                const taskId = task.dataset.id;
                // 这里应该有实际停止任务的逻辑
                // 模拟停止任务
                task.dataset.status = 'pending';
                const statusElement = task.querySelector('.task-status');
                const statusIcon = task.querySelector('.status-icon');
                const statusText = task.querySelector('.status-text');

                statusElement.className = 'task-status status-pending';
                statusIcon.textContent = '⏱️';
                statusIcon.style.animation = 'none';
                statusText.textContent = '待执行';
            });

            saveAutoInfoTasks(); // 调用main.js中的函数
            showNotification('所有任务已停止', 'success');
        });
    }

    // 创建后启用任务复选框
    const enableTaskCheckbox = document.getElementById('enableTask');
    if (enableTaskCheckbox) {
        // 可以在这里添加相关逻辑
    }

    // 任务完成后删除复选框
    const autoDeleteCheckbox = document.getElementById('autoDelete');
    if (autoDeleteCheckbox) {
        // 可以在这里添加相关逻辑
    }
}

// 显示通知（复用main.js中的函数，如果不存在则创建）
function showNotification(message, type = 'info') {
    if (window.showNotification) {
        window.showNotification(message, type);
    } else {
        // 如果main.js中没有实现，这里提供一个简单的实现
        const notificationContainer = document.createElement('div');
        notificationContainer.className = `notification ${type} animate-fade-in`;
        notificationContainer.textContent = message;

        document.body.appendChild(notificationContainer);

        setTimeout(() => {
            notificationContainer.classList.add('fade-out');
            setTimeout(() => {
                document.body.removeChild(notificationContainer);
            }, 300);
        }, 3000);
    }
}

// 确保能访问到main.js中的saveAutoInfoTasks函数
if (!window.saveAutoInfoTasks && typeof saveAutoInfoTasks === 'function') {
    window.saveAutoInfoTasks = saveAutoInfoTasks;
}

// 添加CSS样式
const style = document.createElement('style');
style.textContent = `
    .phone-tag {
        display: inline-flex;
        align-items: center;
        background-color: #e9ecef;
        padding: 4px 8px;
        border-radius: 4px;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    .remove-phone-btn {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 14px;
        color: #6c757d;
    }

    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 4px;
        color: white;
        z-index: 1000;
    }

    .notification.info {
        background-color: #17a2b8;
    }

    .notification.success {
        background-color: #28a745;
    }

    .notification.error {
        background-color: #dc3545;
    }

    .animate-fade-in {
        animation: fadeIn 0.3s ease-in;
    }

    .fade-out {
        animation: fadeOut 0.3s ease-out;
        opacity: 0;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeOut {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 0; transform: translateY(-10px); }
    }
`;

document.head.appendChild(style);