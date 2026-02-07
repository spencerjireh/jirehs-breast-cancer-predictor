<script lang="ts">
  import { prediction, predicting } from '../lib/stores';
  import type { PredictionResult } from '../lib/types';

  let pred: PredictionResult | null = $state(null);
  let loading: boolean = $state(false);

  prediction.subscribe((v) => (pred = v));
  predicting.subscribe((v) => (loading = v));
</script>

<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
  <h2 class="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-4">
    Cell Cluster Prediction
  </h2>

  {#if loading}
    <div class="flex items-center justify-center py-8">
      <div
        class="w-8 h-8 border-4 border-gray-200 border-t-accent rounded-full animate-spin"
      ></div>
    </div>
  {:else if pred}
    <div class="space-y-4">
      <div>
        <p class="text-sm text-gray-500 mb-1">The cell cluster is:</p>
        <span
          class="inline-block px-3 py-1 rounded-md text-white text-sm font-semibold {pred.prediction ===
          'Benign'
            ? 'bg-benign'
            : 'bg-malignant'}"
        >
          {pred.prediction}
        </span>
      </div>

      <div class="space-y-2">
        <div>
          <div class="flex justify-between text-sm mb-1">
            <span>Benign</span>
            <span class="font-mono">{(pred.probability_benign * 100).toFixed(1)}%</span>
          </div>
          <div class="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
            <div
              class="h-full bg-benign rounded-full transition-all duration-500"
              style="width: {pred.probability_benign * 100}%"
            ></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between text-sm mb-1">
            <span>Malignant</span>
            <span class="font-mono">{(pred.probability_malignant * 100).toFixed(1)}%</span>
          </div>
          <div class="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
            <div
              class="h-full bg-malignant rounded-full transition-all duration-500"
              style="width: {pred.probability_malignant * 100}%"
            ></div>
          </div>
        </div>
      </div>

      <p class="text-xs text-gray-400 mt-4 leading-relaxed">
        This app is intended to assist medical professionals in making a
        diagnosis, but should not be used as a substitute for a professional
        diagnosis.
      </p>
    </div>
  {:else}
    <p class="text-sm text-gray-400 py-8 text-center">
      Adjust the sliders to get a prediction.
    </p>
  {/if}
</div>
