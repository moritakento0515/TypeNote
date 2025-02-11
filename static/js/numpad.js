document.addEventListener('DOMContentLoaded', function() {
    const scoreInput = document.getElementById('id_score');
    const numpadContainer = document.createElement('div');
    let isNumpadVisible = false;

    // スタイルの追加
    numpadContainer.className = 'hidden bg-gray-50 rounded-lg p-4 mt-4';
    numpadContainer.innerHTML = `
        <div class="flex justify-end mb-2">
            <button type="button" class="text-gray-500 hover:text-gray-700" id="close-numpad">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
            </button>
        </div>
        <div class="grid grid-cols-3 gap-2">
            ${[1,2,3,4,5,6,7,8,9].map(num => `
                <button type="button" class="num-button bg-white text-xl font-semibold p-4 rounded-lg shadow hover:bg-purple-50 active:bg-purple-100 transition-colors">
                    ${num}
                </button>
            `).join('')}
            <button type="button" class="bg-white text-xl font-semibold p-4 rounded-lg shadow hover:bg-red-50 active:bg-red-100 transition-colors" id="clear-button">
                C
            </button>
            <button type="button" class="num-button bg-white text-xl font-semibold p-4 rounded-lg shadow hover:bg-purple-50 active:bg-purple-100 transition-colors">
                0
            </button>
            <button type="button" class="bg-white text-xl font-semibold p-4 rounded-lg shadow hover:bg-yellow-50 active:bg-yellow-100 transition-colors" id="delete-button">
                ←
            </button>
        </div>
    `;

    // スコア入力フィールドの後にNumpadを挿入
    scoreInput.parentNode.insertBefore(numpadContainer, scoreInput.nextSibling);
    

    // イベントリスナーの設定
    scoreInput.addEventListener('click', function() {
        numpadContainer.classList.remove('hidden');
        isNumpadVisible = true;
    });

    document.getElementById('close-numpad').addEventListener('click', function() {
        numpadContainer.classList.add('hidden');
        isNumpadVisible = false;
    });

    document.querySelectorAll('.num-button').forEach(button => {
        button.addEventListener('click', function() {
            scoreInput.value += this.textContent.trim();
        });
    });

    document.getElementById('clear-button').addEventListener('click', function() {
        scoreInput.value = '';
    });

    document.getElementById('delete-button').addEventListener('click', function() {
        scoreInput.value = scoreInput.value.slice(0, -1);
    });
});