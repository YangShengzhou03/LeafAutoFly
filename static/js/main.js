// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化任务列表交互
    initTaskList();

    // 处理按钮点击态

    // 处理按钮点击态
    const buttons = document.querySelectorAll('button');
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

// 添加CSS动画
const style = document.createElement('style');
style.textContent = `
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
`;
document.head.appendChild(style);