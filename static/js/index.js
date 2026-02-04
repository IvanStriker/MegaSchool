document.addEventListener('DOMContentLoaded', function() {
    const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('fileInput');
    const browseBtn = document.getElementById('browseBtn');
    const uploadForm = document.getElementById('uploadForm');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const submitBtn = document.getElementById('submitBtn');
    const submitText = document.getElementById('submitText');

    // Обработка клика по области загрузки
    browseBtn.addEventListener('click', function() {
        fileInput.click();
    });

    // Отображение имени выбранного файла
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            const fileName = this.files[0].name;
            dropArea.innerHTML = `
                <div class="upload-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" fill="currentColor" class="bi bi-file-earmark-check" viewBox="0 0 16 16">
                        <path d="M10.854 7.854a.5.5 0 0 0-.708-.708L7.5 9.793 6.354 8.646a.5.5 0 1 0-.708.708l1.5 1.5a.5.5 0 0 0 .708 0l3-3z"/>
                        <path d="M14 14V4.5L9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2zM9.5 3A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5v2z"/>
                    </svg>
                </div>
                <h4>Выбран файл:</h4>
                <p class="fw-bold">${fileName}</p>
                <p class="text-muted small">${(this.files[0].size / (1024 * 1024)).toFixed(2)} MB</p>
                <button type="button" id="changeFileBtn" class="btn btn-outline-secondary btn-sm">Изменить файл</button>
            `;

            document.getElementById('changeFileBtn').addEventListener('click', function() {
                fileInput.click();
            });
        }
    });

    // Drag and drop функциональность
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropArea.classList.add('dragover');
    }

    function unhighlight() {
        dropArea.classList.remove('dragover');
    }

    // Обработка drop
    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files;

        // Триггерим событие change для обновления UI
        const event = new Event('change');
        fileInput.dispatchEvent(event);
    }

    // Обработка отправки формы
    uploadForm.addEventListener('submit', function(e) {
        if (!fileInput.files.length) {
            e.preventDefault();
            alert('Пожалуйста, выберите файл для загрузки');
            return;
        }

        fileInput.style.display = 'block';

        // Показываем индикатор загрузки
        loadingSpinner.style.display = 'inline-block';
        submitBtn.disabled = true;
        submitText.textContent = 'Загрузка...';

        // В реальном приложении здесь будет AJAX запрос
        // Для демонстрации просто показываем индикатор 3 секунды
        setTimeout(() => {
            loadingSpinner.style.display = 'none';
            submitBtn.disabled = false;
            submitText.textContent = 'Загрузить файл';
        }, 3000);
    });

    // Анимация прогресса (для демонстрации)
    function simulateProgress() {
        const progressFill = document.createElement('div');
        progressFill.className = 'progress-fill';
        const progressBar = document.createElement('div');
        progressBar.className = 'progress-bar';
        progressBar.appendChild(progressFill);

        const fileItem = document.querySelector('.file-item:last-child');
        if (fileItem) {
            fileItem.appendChild(progressBar);

            let width = 0;
            const interval = setInterval(() => {
                if (width >= 100) {
                    clearInterval(interval);
                    progressFill.style.backgroundColor = '#28a745';
                } else {
                    width += 10;
                    progressFill.style.width = width + '%';
                }
            }, 200);
        }
    }

    // Инициализация симуляции прогресса
    if (document.querySelector('.file-item')) {
        simulateProgress();
    }
});