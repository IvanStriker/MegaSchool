let quill = new Quill('#editor', {
  modules: {
    toolbar: [
      [{ header: [1, 2, false] }],
      ['bold', 'italic', 'underline'],
      ['image', 'code-block'],
    ],
  },
  placeholder: 'Compose an epic...',
  theme: 'snow', // or 'bubble'
});

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
    const textarea = document.getElementById('editor');
    const findText = document.getElementById('findInput').value;
    const caseSensitive = document.getElementById('caseSensitive').checked;

    if (!findText) return;

    const content = quill.getText();
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
    const textarea = document.getElementById('editor');
    const findText = document.getElementById('findInput').value;
    const replaceText = document.getElementById('replaceInput').value;

    if (!findText) return;

    const selectedText = quill.getText().substring(
        textarea.selectionStart,
        textarea.selectionEnd
    );

    if (selectedText === findText) {
        quill.setText(textarea.value.substring(0, textarea.selectionStart) +
                       replaceText +
                       textarea.value.substring(textarea.selectionEnd));
        performFind(); // Найти следующее вхождение
    } else {
        performFind();
    }

}

function performReplaceAll() {
    const textarea = document.getElementById('editor');
    const findText = document.getElementById('findInput').value;
    const replaceText = document.getElementById('replaceInput').value;
    const caseSensitive = document.getElementById('caseSensitive').checked;

    if (!findText) return;

    let content = quill.getText();
    const flags = caseSensitive ? 'g' : 'gi';
    const regex = new RegExp(findText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), flags);

    const matches = content.match(regex);
    if (!matches) {
        alert('Текст не найден');
        return;
    }

    if (confirm(`Заменить все вхождения (${matches.length})?`)) {
        quill.setText(content.replace(regex, replaceText));
        alert(`Заменено ${matches.length} вхождений`);
    }
}

// Дополнительные функции
async function downloadText() {
    const filename = prompt("Enter full filename: ");
    let form = document.createElement('form');
    form.action = '/download';
    form.method = 'POST';
    form.style.display = 'none';
    form.innerHTML = '<textarea id="TempTextEditor" name="file"></textarea>'
    form.innerHTML += '<input id="TempSaveInput" name="filename"/>'
    document.getElementById('editor').appendChild(form);
    document.getElementById('TempTextEditor').value =
        quill.getText();
    document.getElementById('TempSaveInput').value = filename;
    form.submit();
    form.remove();
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