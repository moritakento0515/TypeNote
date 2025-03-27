// Description: スコア入力フィールドに Numpad を表示するスクリプト

function numpad(inputId) {
    // スコア入力フィールドを取得
    const scoreInput = document.getElementById(inputId);
    // 要素が見つからない場合はエラーメッセージを表示して処理を中断
    if (!scoreInput) {
        console.error(`Numpad target element with ID "${inputId}" not found.`);
        return;
    }

    const numpadContainer = createNumpad();
    // Numpad の表示状態を管理するフラグ
    let isNumpadVisible = false;

    /**
     * スコア入力フィールドの後に Numpad を挿入
     * nextSibling プロパティ: 指定した要素の直後の要素を取得 (ない場合は null)
     * insertBefore メソッド: 指定した要素を、対象の要素の前に挿入 (nextSibling が null の場合、末尾に追加)
     */
    scoreInput.parentNode.insertBefore(numpadContainer, scoreInput.nextSibling);
    
    /**
     * スコア入力時に Numpad を表示/非表示に切り替え
     */
    scoreInput.addEventListener('click', toggleNumpad);
    
    /**
     * Numpad のクリックイベントを handleNumpadClick 関数で処理
     */
    numpadContainer.addEventListener('click', handleNumpadClick);
    
    
    // --------------------------------------------
    // Functions
    // --------------------------------------------

    /**
     * Numpad の作成
     */
    function createNumpad() {
        const container = document.createElement('div');
        container.className = 'hidden bg-gray-50 rounded-lg p-4 mt-4';
        container.innerHTML = `
            <div class="flex justify-end mb-2">
                <button type="button" class="text-gray-500 hover:text-gray-700" id="close-numpad">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M18 6 6 18"/>
                        <path d="m6 6 12 12"/>
                    </svg>
                </button>
            </div>
            <div class="grid grid-cols-3 gap-2">
                ${[1,2,3,4,5,6,7,8,9].map(num => `
                    <button type="button" class="num-button bg-white text-xl font-semibold p-4 rounded-lg shadow hover:bg-purple-50 active:bg-purple-100 transition-colors">
                        ${num}
                    </button>
                `).join('')}
                <button type="button" class="bg-white text-xl font-semibold p-4 rounded-lg shadow hover:bg-red-50 active:bg-red-100 transition-colors" data-action="clear">
                    C
                </button>
                <button type="button" class="num-button bg-white text-xl font-semibold p-4 rounded-lg shadow hover:bg-purple-50 active:bg-purple-100 transition-colors">
                    0
                </button>
                <button type="button" class="bg-white text-xl font-semibold p-4 rounded-lg shadow hover:bg-yellow-50 active:bg-yellow-100 transition-colors" data-action="delete">
                    ←
                </button>
            </div>
        `;
        return container;
    }
    
    /**
     * Numpad の表示/非表示を切り替える関数
     */
    function toggleNumpad() {
        isNumpadVisible = !isNumpadVisible;
        // isNumpadVisible が true のときは hidden クラスを除去、false のときは追加
        numpadContainer.classList.toggle('hidden', !isNumpadVisible);
    }
    
    /**
     * Numpad 内のクリックイベントを処理する関数
     */
    function handleNumpadClick(event) {
        const target = event.target.closest('button');
        if (!target) return;
        
        if (target.id === 'close-numpad') {
            toggleNumpad();
        } else if (target.dataset.action === 'clear') {
            scoreInput.value = '';
        } else if (target.dataset.action === 'delete') {
            scoreInput.value = scoreInput.value.slice(0, -1);
        } else if (target.classList.contains('num-button')) {
            scoreInput.value += target.textContent.trim();
        }
    }
};


/**
 *  DOMContentLoaded イベント: HTML が読み込まれ、解析された後に発生
 *  このイベントが発生した時点で、DOM が操作可能になる
 */
document.addEventListener('DOMContentLoaded', () => {
    const possibleInputIds = [
        'id_score',
        'id_target_score',
    ];

    possibleInputIds.forEach(inputId => {
        // ★★★ inputId を持つ要素が存在するかどうかを確認 ★★★
        const element = document.getElementById(inputId);
        if (element) {
            // 要素が存在する場合のみ numpad() を呼び出す
            numpad(inputId);
        }
    });

});