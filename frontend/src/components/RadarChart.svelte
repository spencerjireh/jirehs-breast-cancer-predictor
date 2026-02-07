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
        line: { color: '#553f6f' },
        fillcolor: 'rgba(85, 63, 111, 0.15)',
      },
      {
        type: 'scatterpolar',
        r: p.radar_data.se,
        theta: cats,
        fill: 'toself',
        name: 'Standard Error',
        line: { color: '#f59e0b' },
        fillcolor: 'rgba(245, 158, 11, 0.15)',
      },
      {
        type: 'scatterpolar',
        r: p.radar_data.worst,
        theta: cats,
        fill: 'toself',
        name: 'Worst Value',
        line: { color: '#ef4444' },
        fillcolor: 'rgba(239, 68, 68, 0.15)',
      },
    ];
  }

  const layout = {
    polar: {
      radialaxis: { visible: true, range: [0, 1] },
    },
    showlegend: true,
    margin: { t: 40, b: 40, l: 60, r: 60 },
    font: { family: 'Inter, sans-serif' },
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

<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
  <h2 class="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-2">
    Radar Chart
  </h2>
  <div bind:this={container} class="w-full" style="min-height: 400px;"></div>
</div>
