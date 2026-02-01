document.addEventListener('DOMContentLoaded', function() {
    var easyMDE = new EasyMDE({
        element: document.getElementById('textEditor'),
        spellChecker: false,
        autosave: {
            enabled: true,
            uniqueId: "my-editor",
            delay: 1000
        },
        toolbar: [
            "bold", "italic", "heading", "|",
            "quote", "unordered-list", "ordered-list", "|",
            "link", "image", "|",
            "preview", "side-by-side", "fullscreen", "|",
            "guide"
        ]
    });
    // Инициализация
    updateStats();
});

// Функции форматирования
function formatText(type) {
    const textarea = document.getElementById('textEditor');
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selectedText = textarea.value.substring(start, end);

    let formattedText = selectedText;
    switch(type) {
        case 'bold':
            formattedText = `**${selectedText}**`;
            break;
        case 'italic':
            formattedText = `*${selectedText}*`;
            break;
        case 'underline':
            formattedText = `<u>${selectedText}</u>`;
            break;
    }

    textarea.value = textarea.value.substring(0, start) +
                    formattedText +
                    textarea.value.substring(end);

    textarea.focus();
    textarea.setSelectionRange(start, start + formattedText.length);
    updateStats();
    updatePreview();
}

function insertText(text, cursorOffset = text.length) {
    const textarea = document.getElementById('textEditor');
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;

    textarea.value = textarea.value.substring(0, start) +
                    text +
                    textarea.value.substring(end);

    textarea.focus();
    const newPos = start + cursorOffset;
    textarea.setSelectionRange(newPos, newPos);
    updateStats();
}

// Статистика
function updateStats() {
    const text = document.getElementById('textEditor').value;

    // Символы
    document.getElementById('charCount').textContent = text.length;

    // Слова
    const words = text.trim().split(/\s+/).filter(word => word.length > 0);
    document.getElementById('wordCount').textContent = words.length;

    // Строки
    const lines = text.split('\n').filter(line => line.trim().length > 0);
    document.getElementById('lineCount').textContent = lines.length || 1;
}

// Поиск и замена
function findText() {
    const modal = new bootstrap.Modal(document.getElementById('findReplaceModal'));
    modal.show();
}

function replaceText() {
    findText();
    setTimeout(() => {
        document.getElementById('replaceInput').focus();
    }, 500);
}

function performFind() {
    const textarea = document.getElementById('textEditor');
    const findText = document.getElementById('findInput').value;
    const caseSensitive = document.getElementById('caseSensitive').checked;

    if (!findText) return;

    const content = textarea.value;
    let searchContent = content;
    let searchText = findText;

    if (!caseSensitive) {
        searchContent = content.toLowerCase();
        searchText = findText.toLowerCase();
    }

    const index = searchContent.indexOf(searchText);

    if (index !== -1) {
        textarea.focus();
        textarea.setSelectionRange(index, index + findText.length);
        textarea.scrollTop = (index / content.length) * textarea.scrollHeight;
    } else {
        alert('Текст не найден');
    }
}

function performReplace() {
    const textarea = document.getElementById('textEditor');
    const findText = document.getElementById('findInput').value;
    const replaceText = document.getElementById('replaceInput').value;

    if (!findText) return;

    const selectedText = textarea.value.substring(
        textarea.selectionStart,
        textarea.selectionEnd
    );

    if (selectedText === findText) {
        textarea.value = textarea.value.substring(0, textarea.selectionStart) +
                       replaceText +
                       textarea.value.substring(textarea.selectionEnd);
        performFind(); // Найти следующее вхождение
    } else {
        performFind();
    }

    updateStats();
}

function performReplaceAll() {
    const textarea = document.getElementById('textEditor');
    const findText = document.getElementById('findInput').value;
    const replaceText = document.getElementById('replaceInput').value;
    const caseSensitive = document.getElementById('caseSensitive').checked;

    if (!findText) return;

    let content = textarea.value;
    const flags = caseSensitive ? 'g' : 'gi';
    const regex = new RegExp(findText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), flags);

    const matches = content.match(regex);
    if (!matches) {
        alert('Текст не найден');
        return;
    }

    if (confirm(`Заменить все вхождения (${matches.length})?`)) {
        textarea.value = content.replace(regex, replaceText);
        updateStats();
        alert(`Заменено ${matches.length} вхождений`);
    }
}

// Дополнительные функции
async function downloadText() {
    const text = document.getElementById('textEditor').value;

    try {
        // Запрашиваем разрешение на сохранение
        fileHandle = await window.showSaveFilePicker({
            suggestedName: 'document.txt',
            types: [{
                description: 'Text files',
                accept: {'text/plain': ['.txt']},
            }],
        });

        // Создаем поток для записи
        const writable = await fileHandle.createWritable();
        await writable.write(text);
        await writable.close();

    } catch (err) {
        if (err.name !== 'AbortError') {
            console.error('Ошибка:', err);
            alert('Ошибка сохранения файла');
        }
    }
}

function shareText() {
    const text = document.getElementById('textEditor').value;
    if (navigator.share) {
        navigator.share({
            title: '{{ file.filename if file else "Текст" }}',
            text: text.substring(0, 100) + '...',
            url: window.location.href
        });
    } else {
        navigator.clipboard.writeText(window.location.href).then(() => {
            showMessage('success', 'Ссылка скопирована в буфер обмена');
        });
    }
}

function changeFontSize(size) {
    document.getElementById('textEditor').style.fontSize = size + 'px';
}

// Вспомогательные функции
function showMessage(type, text) {
    // Создаем элемент сообщения
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-auto-hide alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '1000';
    alertDiv.style.minWidth = '300px';
    alertDiv.innerHTML = `
        ${text}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;

    document.body.appendChild(alertDiv);

    // Автоматическое удаление через 5 секунд
    setTimeout(() => {
        if (alertDiv.parentElement) {
            alertDiv.remove();
        }
    }, 5000);
}

// Обновление статистики файла
function updateFileStats(stats) {
    // Обновляем информацию о файле если есть
    const sizeElement = document.querySelector('.file-meta .meta-item:nth-child(2)');
    if (sizeElement && stats.size) {
        sizeElement.innerHTML = `<i class="bi bi-hdd me-1"></i>Размер: ${formatFileSize(stats.size)}`;
    }
}