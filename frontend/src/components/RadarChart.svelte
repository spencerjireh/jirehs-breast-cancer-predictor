<script lang="ts">
  import { prediction, radarCategories } from '../lib/stores';
  import type { PredictionResult } from '../lib/types';

  let container: HTMLDivElement;
  let Plotly: any = $state(null);
  let categories: string[] = $state([]);
  let pred: PredictionResult | null = $state(null);

  radarCategories.subscribe((v) => (categories = v));
  prediction.subscribe((v) => (pred = v));

  function getTraces(p: PredictionResult, cats: string[]) {
    return [
      {
        type: 'scatterpolar',
        r: p.radar_data.mean,
        theta: cats,
        fill: 'toself',
        name: 'Mean Value',
        line: { color: '#0d9488', width: 2 },
        fillcolor: 'rgba(13, 148, 136, 0.12)',
        marker: { size: 4 },
      },
      {
        type: 'scatterpolar',
        r: p.radar_data.se,
        theta: cats,
        fill: 'toself',
        name: 'Standard Error',
        line: { color: '#f59e0b', width: 2 },
        fillcolor: 'rgba(245, 158, 11, 0.1)',
        marker: { size: 4 },
      },
      {
        type: 'scatterpolar',
        r: p.radar_data.worst,
        theta: cats,
        fill: 'toself',
        name: 'Worst Value',
        line: { color: '#f43f5e', width: 2 },
        fillcolor: 'rgba(244, 63, 94, 0.1)',
        marker: { size: 4 },
      },
    ];
  }

  const layout = {
    polar: {
      radialaxis: {
        visible: true,
        range: [0, 1],
        tickfont: { size: 9, color: '#94a3b8', family: 'DM Sans' },
        gridcolor: '#e2e8f0',
        linecolor: '#e2e8f0',
      },
      angularaxis: {
        tickfont: { size: 10, color: '#64748b', family: 'DM Sans' },
        gridcolor: '#e2e8f0',
        linecolor: '#e2e8f0',
      },
      bgcolor: 'transparent',
    },
    showlegend: true,
    legend: {
      orientation: 'h',
      y: -0.15,
      x: 0.5,
      xanchor: 'center',
      font: { size: 11, color: '#64748b', family: 'DM Sans' },
    },
    margin: { t: 30, b: 50, l: 50, r: 50 },
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    font: { family: 'DM Sans, sans-serif' },
  };

  const config = { displayModeBar: false, responsive: true };

  $effect(() => {
    if (!container) return;

    import('plotly.js-dist-min').then((mod) => {
      Plotly = mod.default;
      if (pred && categories.length) {
        Plotly.newPlot(container, getTraces(pred, categories), layout, config);
      }
    });
  });

  $effect(() => {
    if (Plotly && pred && categories.length && container) {
      Plotly.react(container, getTraces(pred, categories), layout, config);
    }
  });
</script>

<div class="card p-5 h-full">
  <div class="flex items-center justify-between mb-3">
    <div>
      <h2 class="text-sm font-semibold text-slate-700">Feature Radar</h2>
      <p class="text-[11px] text-slate-400 mt-0.5">Normalized measurement distribution</p>
    </div>
    <div class="flex items-center gap-3">
      <div class="flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-primary"></span>
        <span class="text-[10px] text-slate-500">Mean</span>
      </div>
      <div class="flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-amber-400"></span>
        <span class="text-[10px] text-slate-500">SE</span>
      </div>
      <div class="flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-malignant"></span>
        <span class="text-[10px] text-slate-500">Worst</span>
      </div>
    </div>
  </div>
  <div bind:this={container} class="w-full" style="min-height: 380px;"></div>
</div>
