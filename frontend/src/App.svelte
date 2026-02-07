<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchFeatures, fetchPrediction } from './lib/api';
  import { featuresMeta, featureValues, prediction, predicting, radarCategories } from './lib/stores';
  import { debounce } from './lib/debounce';
  import SliderPanel from './components/SliderPanel.svelte';
  import RadarChart from './components/RadarChart.svelte';
  import PredictionPanel from './components/PredictionPanel.svelte';

  let initialized = $state(false);

  const debouncedPredict = debounce(async (vals: Record<string, number>) => {
    predicting.set(true);
    try {
      const result = await fetchPrediction(vals);
      prediction.set(result);
    } catch (err) {
      console.error('Prediction error:', err);
    } finally {
      predicting.set(false);
    }
  }, 300);

  onMount(async () => {
    try {
      const data = await fetchFeatures();
      featuresMeta.set(data.features);
      radarCategories.set(data.radar_categories);

      const defaults: Record<string, number> = {};
      for (const f of data.features) {
        defaults[f.key] = f.mean;
      }
      featureValues.set(defaults);
      initialized = true;

      // Trigger initial prediction
      debouncedPredict(defaults);
    } catch (err) {
      console.error('Failed to load features:', err);
    }
  });

  // React to slider changes
  featureValues.subscribe((vals) => {
    if (initialized && Object.keys(vals).length > 0) {
      debouncedPredict(vals);
    }
  });
</script>

<div class="min-h-screen flex flex-col">
  <!-- Header -->
  <header class="bg-accent text-white px-6 py-4 shadow-md">
    <h1 class="text-lg font-semibold">Breast Cancer Predictor</h1>
    <p class="text-xs text-white/70 mt-0.5">
      Machine learning-assisted cytology analysis
    </p>
  </header>

  <!-- Body -->
  <div class="flex-1 flex flex-col lg:flex-row">
    <!-- Sidebar -->
    <aside
      class="w-full lg:w-80 xl:w-96 bg-white border-b lg:border-b-0 lg:border-r border-gray-200 overflow-y-auto lg:max-h-[calc(100vh-72px)]"
    >
      <SliderPanel />
    </aside>

    <!-- Main content -->
    <main class="flex-1 p-4 lg:p-6 space-y-4 lg:space-y-6 overflow-y-auto lg:max-h-[calc(100vh-72px)]">
      <div class="max-w-4xl mx-auto space-y-4 lg:space-y-6">
        <p class="text-sm text-gray-500 leading-relaxed">
          A predictor for cancer malignancy in breast tissue samples meant to be
          used in conjunction with measurements from a cytology lab. Uses a
          Machine Learning Model based on Logistic Regression. Use the sliders to
          update measurements from observations.
        </p>

        <RadarChart />
        <PredictionPanel />
      </div>
    </main>
  </div>
</div>
