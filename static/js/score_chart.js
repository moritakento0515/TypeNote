// DOMが完全に読み込まれた後に実行する処理
document.addEventListener("DOMContentLoaded", () => {
  // Chart.jsが正しく読み込まれているか確認
  if (typeof Chart === "undefined") {
    console.error("Chart.jsが読み込まれていません。スクリプトタグを確認してください。")
    return
  }

  // Progateスタイルのカラーパレット
  const colors = {
    primary: "#2E75B6", // Progateのメインブルー
    primaryLight: "#4A90E2", // 明るめのブルー
    success: "#55C500", // 達成時の緑（Progateの完了色）
    successLight: "#88D840", // 明るめの緑
    warning: "#A464C4", // 未達成時の紫
    warningLight: "#B57EDC", // 明るめの紫
    target: "#FF5252", // 目標ライン（赤）
    gridLine: "#EAEDF2", // グリッドライン
    textDark: "#333F4D", // テキスト（濃い色）
    textLight: "#8492A6", // テキスト（薄い色）
  }

  fetch(scoreHistoryUrl)
    .then((response) => response.json())
    .then((data) => {
      const labels = data.timestamps.map((ts) => {
        const date = new Date(ts)
        return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, "0")}`
      })

      const scores = data.scores
      const targetScore = data.target_score // 目標スコアを取得

      // スコアが存在しない場合は何もしない
      if (scores.length === 0) return

      const ctx = document.getElementById("scoreChart").getContext("2d")

      // Y軸の範囲を設定（スコアの変動を見やすく）
      const minScore = Math.min(...scores, targetScore)
      const maxScore = Math.max(...scores, targetScore)
      const yMin = Math.floor(minScore * 0.9) // 最小値を少し下げる
      const yMax = Math.ceil(maxScore * 1.1) // 最大値を少し上げる

      // 目標スコアの相対位置を計算（0〜1の範囲）
      const targetRatio = (targetScore - yMin) / (yMax - yMin)

      // フォントスタイルを設定
      Chart.defaults.font.family = "'Hiragino Kaku Gothic Pro', 'メイリオ', sans-serif"
      Chart.defaults.font.size = 12

      // アニメーションの設定
      const animationOptions = {
        duration: 1500,
        easing: "easeOutQuart",
      }

      // グラフを描画
      new Chart(ctx, {
        type: "line",
        data: {
          labels: labels,
          datasets: [
            {
              label: "スコア推移",
              data: scores,
              borderColor: colors.primary,
              borderWidth: 3,
              fill: true, // 塗りつぶしを有効化
              backgroundColor: (context) => {
                const chart = context.chart
                const { ctx, chartArea } = chart

                if (!chartArea) {
                  // チャートエリアがまだ利用できない場合
                  return null
                }

                // チャートの高さを取得
                const chartHeight = chartArea.bottom - chartArea.top

                // 目標スコアのY座標を計算
                const targetY = chartArea.bottom - targetRatio * chartHeight

                // グラデーションを作成
                const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom)

                // 目標スコアの位置を0〜1の範囲に変換
                const normalizedTargetY = (targetY - chartArea.top) / chartHeight

                // 目標スコア以上の領域（緑系）- Progateスタイル
                gradient.addColorStop(0, "rgba(85, 197, 0, 0.4)") // 上部（緑）
                gradient.addColorStop(normalizedTargetY - 0.001, "rgba(136, 216, 64, 0.15)") // 目標スコア直前

                // 目標スコア未満の領域（紫系）- Progateスタイル
                gradient.addColorStop(normalizedTargetY, "rgba(164, 100, 196, 0.2)") // 目標スコア直後
                gradient.addColorStop(1, "rgba(181, 126, 220, 0.05)") // 下部（薄紫）

                return gradient
              },
              tension: 0.4, // 曲線をより滑らかに
              pointBackgroundColor: "white",
              pointBorderColor: colors.primary,
              pointBorderWidth: 2,
              pointRadius: 4,
              pointHoverRadius: 6,
              pointHoverBackgroundColor: colors.primary,
              pointHoverBorderColor: "white",
              pointHoverBorderWidth: 2,
            },
            {
              label: "目標スコア",
              data: Array(scores.length).fill(targetScore),
              borderColor: colors.target,
              borderWidth: 2,
              borderDash: [6, 4],
              fill: false,
              pointRadius: 0,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: animationOptions,
          interaction: {
            mode: "index",
            intersect: false,
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "日付",
                color: colors.textDark,
                font: {
                  weight: "bold",
                  size: 13,
                },
                padding: { top: 10, bottom: 0 },
              },
              ticks: {
                autoSkip: true,
                maxTicksLimit: 10,
                color: colors.textLight,
                callback: function (value, index, values) {
                  return index % Math.ceil(values.length / 10) === 0 ? this.getLabelForValue(value) : ""
                },
              },
              grid: {
                color: colors.gridLine,
                drawBorder: false,
              },
            },
            y: {
              title: {
                display: true,
                text: "スコア",
                color: colors.textDark,
                font: {
                  weight: "bold",
                  size: 13,
                },
                padding: { top: 0, bottom: 10 },
              },
              min: yMin,
              max: yMax,
              ticks: {
                color: colors.textLight,
                font: {
                  size: 11,
                },
                padding: 8,
              },
              grid: {
                color: colors.gridLine,
                drawBorder: false,
              },
            },
          },
          plugins: {
            legend: {
              labels: {
                usePointStyle: true,
                pointStyle: "circle",
                boxWidth: 6,
                boxHeight: 6,
                color: colors.textDark,
                font: {
                  size: 13,
                },
                padding: 20,
              },
            },
            tooltip: {
              backgroundColor: "rgba(255, 255, 255, 0.95)",
              titleColor: colors.textDark,
              bodyColor: colors.textDark,
              borderColor: "rgba(0, 0, 0, 0.1)",
              borderWidth: 1,
              cornerRadius: 8,
              padding: 12,
              boxPadding: 6,
              usePointStyle: true,
              callbacks: {
                label: (context) => {
                  const score = context.raw
                  let label = context.datasetIndex === 0 ? `スコア: ${score}` : `目標スコア: ${score}`

                  if (context.datasetIndex === 0) {
                    if (score >= targetScore) {
                      label += ` (目標達成: +${(score - targetScore).toFixed(1)})`
                    } else {
                      label += ` (目標まで: ${(targetScore - score).toFixed(1)})`
                    }
                  }

                  return label
                },
                labelTextColor: (context) => {
                  const score = context.raw
                  // スコアデータセットの場合、目標達成かどうかで色を変える
                  if (context.datasetIndex === 0) {
                    return score >= targetScore ? colors.success : colors.warning
                  }
                  return colors.target // 目標スコアの場合
                },
              },
            },
          },
        },
      })
    })
    .catch((error) => console.error("データ取得エラー:", error))
})

