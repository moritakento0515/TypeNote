// DOMが完全に読み込まれた後に実行する処理
document.addEventListener("DOMContentLoaded", function () {
    // DjangoのURLパターンを指定して、スコア履歴データを取得
    fetch(scoreHistoryUrl)  // 'scoreHistoryUrl' は外部から受け取るDjangoのURL
        .then(response => response.json())  // 応答をJSON形式に変換
        .then(data => {
            // 取得したデータのタイムスタンプを日付形式に変換してラベルにする
            const labels = data.timestamps.map(ts => {
                const date = new Date(ts);  // UNIXタイムスタンプをDateオブジェクトに変換
                return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`;
                // "月-日 時:分" の形式でラベルを作成
            });

            // スコアのデータ（Y軸の値）を取得
            const scores = data.scores;

            // グラフを描画するためのキャンバスのコンテキストを取得
            const ctx = document.getElementById('scoreChart').getContext('2d');

            // Chart.jsを使って新しいグラフを作成
            new Chart(ctx, {
                type: 'line',  // グラフの種類：折れ線グラフ
                data: {
                    labels: labels,  // X軸に表示するラベル（日時）
                    datasets: [{
                        label: 'スコア推移',  // データセットのラベル
                        data: scores,  // Y軸に表示するスコアのデータ
                        borderColor: '#7b4b9a',  // 線の色
                        backgroundColor: 'rgba(123, 75, 154, 0.2)',  // 線下の塗りつぶし色（薄紫）
                        borderWidth: 2,  // 線の太さ
                        fill: true,  // 線下を塗りつぶす
                        tension: 0.3  // 線の滑らかさ（曲線の度合い）
                    }]
                },
                options: {
                    responsive: true,  // ウィンドウサイズに応じてグラフをリサイズ
                    scales: {
                        x: {
                            title: {
                                display: true,  // X軸のタイトルを表示
                                text: '日付',  // X軸のタイトル
                                color: '#333'  // タイトルの色
                            },
                            ticks: {
                                autoSkip: true,  // ラベルが重ならないように自動的に省略
                                maxTicksLimit: 10,  // 最大10個のラベルを表示
                                callback: function (value, index, values) {
                                    // すべてのラベルを表示せず、10個に分けて表示
                                    return index % Math.ceil(values.length / 10) === 0 ? this.getLabelForValue(value) : '';
                                }
                            }
                        },
                        y: {
                            title: {
                                display: true,  // Y軸のタイトルを表示
                                text: 'スコア',  // Y軸のタイトル
                                color: '#333'  // タイトルの色
                            },
                            beginAtZero: true  // Y軸は0から始める
                        }
                    }
                }
            });
        })
        .catch(error => console.error("データ取得エラー:", error));  // データ取得に失敗した場合のエラーハンドリング
});
