<script lang="ts">
  import { prediction, predicting } from '../lib/stores';
  import type { PredictionResult } from '../lib/types';

  let pred: PredictionResult | null = $state(null);
  let loading: boolean = $state(false);

  prediction.subscribe((v) => (pred = v));
  predicting.subscribe((v) => (loading = v));

  // SVG gauge constants
  const GAUGE_RADIUS = 80;
  const GAUGE_CIRCUMFERENCE = Math.PI * GAUGE_RADIUS; // half circle
  const GAUGE_STROKE = 10;

  function getGaugeOffset(probability: number): number {
    return GAUGE_CIRCUMFERENCE * (1 - probability);
  }

  function getGaugeColor(probability: number): string {
    if (probability < 0.3) return 'var(--color-benign)';
    if (probability < 0.6) return '#f59e0b';
    return 'var(--color-malignant)';
  }

  function getRiskLabel(probability: number): string {
    if (probability < 0.2) return 'Very Low';
    if (probability < 0.4) return 'Low';
    if (probability < 0.6) return 'Moderate';
    if (probability < 0.8) return 'High';
    return 'Very High';
  }
</script>

<div class="card p-4 sm:p-5 h-full flex flex-col relative">
  <h2 class="text-sm font-semibold text-slate-700 mb-1">Prediction Result</h2>
  <p class="text-[11px] text-slate-400 mb-3 sm:mb-4">Logistic regression classification</p>

  {#if pred}
    <div
      class="flex-1 flex flex-col items-center transition-opacity duration-200"
      class:opacity-50={loading}
      class:pointer-events-none={loading}
    >
      <!-- Risk Gauge -->
      <div class="relative mb-3 sm:mb-4">
        <svg class="w-[160px] h-[92px] sm:w-[200px] sm:h-[115px]" viewBox="0 0 200 115">
          <!-- Background arc -->
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke="#f1f5f9"
            stroke-width={GAUGE_STROKE}
            stroke-linecap="round"
          />
          <!-- Filled arc -->
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke={getGaugeColor(pred.probability_malignant)}
            stroke-width={GAUGE_STROKE}
            stroke-linecap="round"
            stroke-dasharray={GAUGE_CIRCUMFERENCE}
            stroke-dashoffset={getGaugeOffset(pred.probability_malignant)}
            style="transition: stroke-dashoffset 0.8s ease-out, stroke 0.4s ease; animation: gauge-fill 1s ease-out;"
          />
          <!-- Tick marks -->
          {#each [0, 0.25, 0.5, 0.75, 1] as tick}
            {@const angle = Math.PI * (1 - tick)}
            {@const x = 100 + 92 * Math.cos(angle)}
            {@const y = 100 - 92 * Math.sin(angle)}
            <circle cx={x} cy={y} r="1.5" fill="#cbd5e1" />
          {/each}
        </svg>

        <!-- Center text -->
        <div class="absolute inset-0 flex flex-col items-center justify-end pb-2">
          <span
            class="text-2xl sm:text-3xl font-bold tabular-nums"
            style="color: {getGaugeColor(pred.probability_malignant)}"
          >
            {(pred.probability_malignant * 100).toFixed(1)}%
          </span>
          <span class="text-[10px] font-medium text-slate-400 uppercase tracking-wider mt-0.5">
            Malignancy Risk
          </span>
        </div>
      </div>

      <!-- Prediction badge -->
      <div class="w-full mb-4">
        <div
          class="w-full py-2.5 rounded-xl text-center text-sm font-semibold transition-all duration-500"
          style="
            background: {pred.prediction === 'Benign'
            ? 'var(--color-benign-light)'
            : 'var(--color-malignant-light)'};
            color: {pred.prediction === 'Benign'
            ? 'var(--color-benign-dark)'
            : 'var(--color-malignant-dark)'};
          "
        >
          {pred.prediction}
          <span class="font-normal opacity-70">
            -- {getRiskLabel(pred.probability_malignant)} Risk
          </span>
        </div>
      </div>

      <!-- Probability bars -->
      <div class="w-full space-y-3">
        <div>
          <div class="flex justify-between items-center mb-1.5">
            <div class="flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-benign"></span>
              <span class="text-xs font-medium text-slate-600">Benign</span>
            </div>
            <span class="text-xs font-mono font-semibold text-slate-700 tabular-nums">
              {(pred.probability_benign * 100).toFixed(1)}%
            </span>
          </div>
          <div class="w-full h-2 bg-slate-50 rounded-full overflow-hidden">
            <div
              class="h-full rounded-full transition-all duration-500"
              style="width: {pred.probability_benign *
                100}%; background: linear-gradient(90deg, var(--color-benign), var(--color-benign-dark));"
            ></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center mb-1.5">
            <div class="flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-malignant"></span>
              <span class="text-xs font-medium text-slate-600">Malignant</span>
            </div>
            <span class="text-xs font-mono font-semibold text-slate-700 tabular-nums">
              {(pred.probability_malignant * 100).toFixed(1)}%
            </span>
          </div>
          <div class="w-full h-2 bg-slate-50 rounded-full overflow-hidden">
            <div
              class="h-full rounded-full transition-all duration-500"
              style="width: {pred.probability_malignant *
                100}%; background: linear-gradient(90deg, var(--color-malignant), var(--color-malignant-dark));"
            ></div>
          </div>
        </div>
      </div>

      <!-- Disclaimer -->
      <div class="mt-5 pt-4 border-t border-slate-50 w-full">
        <p class="text-[10px] text-slate-400 leading-relaxed text-center">
          This tool assists medical professionals and should not substitute professional diagnosis.
          Always consult a qualified healthcare provider.
        </p>
      </div>
    </div>
    <!-- Small overlay spinner when updating -->
    {#if loading}
      <div class="absolute inset-0 flex items-center justify-center">
        <div class="relative">
          <div class="w-8 h-8 rounded-full border-2 border-slate-200/50"></div>
          <div
            class="absolute inset-0 w-8 h-8 rounded-full border-2 border-transparent border-t-primary animate-spin-slow"
          ></div>
        </div>
      </div>
    {/if}
  {:else if loading}
    <!-- First-load spinner (no previous data to show) -->
    <div class="flex-1 flex items-center justify-center py-8">
      <div class="relative">
        <div class="w-10 h-10 rounded-full border-2 border-slate-100"></div>
        <div
          class="absolute inset-0 w-10 h-10 rounded-full border-2 border-transparent border-t-primary animate-spin-slow"
        ></div>
      </div>
    </div>
  {:else}
    <!-- Empty state (before any interaction) -->
    <div class="flex-1 flex flex-col items-center justify-center py-8">
      <div class="w-12 h-12 rounded-xl bg-slate-50 flex items-center justify-center mb-3">
        <svg
          class="w-6 h-6 text-slate-300"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="1.5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M10.5 6h9.75M10.5 6a1.5 1.5 0 11-3 0m3 0a1.5 1.5 0 10-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m-9.75 0h9.75"
          />
        </svg>
      </div>
      <p class="text-sm text-slate-400 text-center">
        Adjust the sliders to<br />generate a prediction
      </p>
    </div>
  {/if}
</div>
