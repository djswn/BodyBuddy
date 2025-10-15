document.addEventListener('DOMContentLoaded', function () {
    try {
        // 1) Chart 로드 확인
        if (typeof Chart === 'undefined') {
            console.error('[weights_chart] Chart.js가 로드되지 않았습니다.');
            return;
        }

        // 2) canvas 확인
        const canvas = document.getElementById('weightsChart');
        if (!canvas) {
            console.error('[weights_chart] canvas #weightsChart를 찾을 수 없습니다.');
            return;
        }
        const ctx = canvas.getContext('2d');

        // 내부 함수: 데이터 불러와서 렌더
        let chart = null;
        function fetchAndRender() {
            fetch('/weights/data')
                .then(res => {
                    if (!res.ok) throw new Error('[weights_chart] /weights/data fetch failed: ' + res.status);
                    return res.json();
                })
                .then(data => {
                    let labels = Array.isArray(data.labels) ? data.labels.slice() : [];
                    let values = Array.isArray(data.values) ? data.values.slice() : [];

                    // 정렬(혹시 서버에서 정렬이 안 되어 있으면) - 날짜 오름차순
                    // labels, values가 병렬 배열이라 가정
                    if (labels.length && labels.length === values.length) {
                        const pairs = labels.map((l, i) => ({ date: l, val: values[i] }));
                        pairs.sort((a, b) => a.date.localeCompare(b.date));
                        labels = pairs.map(p => p.date);
                        values = pairs.map(p => p.val);
                    }

                    // 데이터 길이에 따른 처리
                    if (labels.length === 0) {
                        labels = [''];
                        values = [0];
                    } else if (labels.length === 1) {
                        // x축에 더미 하나 추가해서 점/선이 보이도록 함
                        labels = [''].concat(labels);
                        values = [values[0], values[0]];
                    }

                    // Chart 옵션 (점이 확실히 보이도록)
                    const dataset = {
                        label: '체중(kg)',
                        data: values,
                        fill: false,
                        tension: 0.12,
                        borderColor: '#2069f3',
                        borderWidth: 2,
                        pointBackgroundColor: '#ff4d4f',
                        pointBorderColor: '#fff',
                        pointRadius: 6,
                        pointHoverRadius: 8,
                        spanGaps: true
                    };

                    if (chart) {
                        chart.data.labels = labels;
                        chart.data.datasets[0] = dataset;
                        chart.update();
                    } else {
                        chart = new Chart(ctx, {
                            type: 'line',
                            data: { labels: labels, datasets: [dataset] },
                            options: {
                                scales: {
                                    x: {
                                        display: true,
                                        title: { display: true, text: '날짜' }
                                    },
                                    y: {
                                        display: true,
                                        title: { display: true, text: '체중 (kg)' },
                                        beginAtZero: false
                                    }
                                },
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {
                                    legend: { display: true }
                                }
                            }
                        });
                    }
                })
                .catch(err => {
                    console.error('[weights_chart] fetch/render error:', err);
                });
        }

        // 처음 렌더
        fetchAndRender();

        // 필요하면 자동 갱신 (예: 폼 제출 직후 반영이 없을 때을 위해)
        // setInterval(fetchAndRender, 30000);

    } catch (err) {
        console.error('[weights_chart] unexpected error:', err);
    }
});
