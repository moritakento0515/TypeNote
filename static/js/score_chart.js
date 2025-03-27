/**
 * スコア履歴をグラフ表示するためのChart.jsコード
 * 目標スコア以上と以下で背景色が変わります
 */

// グローバル設定
Chart.defaults.font.family = "'Hiragino Kaku Gothic Pro', 'メイリオ', sans-serif";
Chart.defaults.font.size = 14;

// スコア履歴データを取得して表示する関数
async function displayScoreChart() {
  try {
    // データの取得
    const response = await fetch(window.scoreHistoryUrl);
    const data = await response.json();
    
    // データの検証
    if (!data || !Array.isArray(data.scores) || data.scores.length === 0) {
      console.warn("有効なスコアデータがありません。");
      return;
    }

    // Y軸の範囲計算
    const yMin = Math.floor(Math.min(...data.scores, data.target_score) * 0.9);
    const yMax = Math.ceil(Math.max(...data.scores, data.target_score) * 1.1);
    
    // 目標ラインの相対位置を計算（グラデーション表示用）
    const targetRatio = (data.target_score - yMin) / (yMax - yMin);
    
    // Canvas要素の取得
    const canvas = document.getElementById('scoreChart');
    const ctx = canvas.getContext('2d');
    
    // チャートの描画
    const chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.timestamps.map(timestamp => formatDate(timestamp)),
        datasets: [
          // スコアデータ
          {
            label: 'スコア',
            data: data.scores,
            borderColor: '#2E75B6',
            backgroundColor: (context) => createGradientBackground(context, targetRatio),
            borderWidth: 3,
            fill: true,
            tension: 0.4,
            pointBackgroundColor: 'white',
            pointBorderColor: '#2E75B6',
            pointBorderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6,
            pointHoverBackgroundColor: '#2E75B6',
          },
          // 目標スコアライン
          {
            label: '目標スコア',
            data: Array(data.scores.length).fill(data.target_score),
            borderColor: '#FF5252',
            borderWidth: 2,
            borderDash: [6, 4],
            fill: false,
            pointRadius: 0
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 1500,
          easing: 'easeOutQuart'
        },
        interaction: {
          mode: 'nearest',
          intersect: false
        },
        scales: {
          x: {
            title: {
              display: true,
              text: '日付',
              color: '#333F4D',
              font: { weight: 'bold', size: 13 }
            },
            ticks: {
              color: '#8492A6',
              maxTicksLimit: 10
            },
            grid: {
              color: '#EAEDF2',
              drawBorder: false
            }
          },
          y: {
            title: {
              display: true,
              text: 'スコア',
              color: '#333F4D',
              font: { weight: 'bold', size: 13 }
            },
            min: yMin,
            max: yMax,
            ticks: {
              color: '#8492A6',
              font: { size: 11 },
              padding: 8
            },
            grid: {
              color: '#EAEDF2',
              drawBorder: false
            }
          }
        },
        plugins: {
          legend: {
            labels: {
              usePointStyle: true,
              pointStyle: 'circle',
              boxWidth: 6,
              boxHeight: 6,
              color: '#333F4D',
              font: { size: 13 },
              padding: 20
            }
          },
          tooltip: {
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            titleColor: '#333F4D',
            bodyColor: '#333F4D',
            borderColor: 'rgba(0, 0, 0, 0.1)',
            borderWidth: 1,
            cornerRadius: 8,
            padding: 12,
            boxPadding: 6,
            usePointStyle: true,
            callbacks: {
              label: (context) => formatTooltipLabel(context, data.target_score),
              labelTextColor: (context) => getTooltipTextColor(context, data.target_score)
            }
          }
        }
      }
    });
    
  } catch (error) {
    console.error("チャート初期化エラー:", error);
  }
}

/**
 * タイムスタンプを表示形式に変換
 */
function formatDate(timestamp) {
  const date = new Date(timestamp);
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const hours = date.getHours();
  const minutes = String(date.getMinutes()).padStart(2, "0");//1 桁の数字の場合に先頭に「0」を追加
  return `${month}/${day} ${hours}:${minutes}`;
}

/**
 * グラデーション背景を作成（目標スコアを基準に色分け）
 */
function createGradientBackground(context, targetRatio) {
  const { ctx, chartArea } = context.chart;
  if (!chartArea) return null;

  // グラデーションの位置計算
  const chartHeight = chartArea.bottom - chartArea.top;
  const targetY = chartArea.bottom - targetRatio * chartHeight;
  const normalizedTargetY = (targetY - chartArea.top) / chartHeight;

  // グラデーションの作成
  const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
  
  // 目標より上：成功色（緑）
  gradient.addColorStop(0, "rgba(85, 197, 0, 0.4)");
  gradient.addColorStop(normalizedTargetY - 0.001, "rgba(136, 216, 64, 0.15)");
  
  // 目標より下：警告色（紫）
  gradient.addColorStop(normalizedTargetY, "rgba(164, 100, 196, 0.2)");
  gradient.addColorStop(1, "rgba(181, 126, 220, 0.05)");
  
  return gradient;
}

/**
 * ツールチップのラベルをフォーマット
 */
function formatTooltipLabel(context, targetScore) {
  const score = context.raw;
  // データセットによってラベルを変更
  let label = context.datasetIndex === 0 ? `スコア: ${score}` : `目標スコア: ${score}`;
  
  // スコアデータの場合、目標との差分を表示
  if (context.datasetIndex === 0) {
    // 目標達成しているかどうかで表示を変える
    label += score >= targetScore
      ? ` (目標達成: +${(score - targetScore).toFixed(1)})`
      : ` (目標まで: ${(targetScore - score).toFixed(1)})`;
  }
  return label;
}

/**
 * ツールチップのテキスト色を取得
 */
function getTooltipTextColor(context, targetScore) {
  const score = context.raw;
  // データセットと値によって色を変更
  if (context.datasetIndex === 0) {
    return score >= targetScore ? '#55C500' : '#A464C4'; // 達成で緑、未達成で紫
  } else {
    return '#FF5252'; // 目標線は赤
  }
}

// ページ読み込み完了時にチャートを表示
document.addEventListener('DOMContentLoaded', displayScoreChart);