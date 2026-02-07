<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchFeatures, fetchPrediction } from './lib/api';
  import {
    featuresMeta,
    featureValues,
    prediction,
    predicting,
    radarCategories,
  } from './lib/stores';
  import { debounce } from './lib/debounce';
  import SliderPanel from './components/SliderPanel.svelte';
  import RadarChart from './components/RadarChart.svelte';
  import PredictionPanel from './components/PredictionPanel.svelte';
  import AboutSection from './components/AboutSection.svelte';

  let initialized = $state(false);
  let currentSection: 'predictor' | 'about' = $state('predictor');
  let mobileMenuOpen = $state(false);

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

      debouncedPredict(defaults);
    } catch (err) {
      console.error('Failed to load features:', err);
    }
  });

  featureValues.subscribe((vals) => {
    if (initialized && Object.keys(vals).length > 0) {
      debouncedPredict(vals);
    }
  });

  function navigate(section: 'predictor' | 'about') {
    currentSection = section;
    mobileMenuOpen = false;
  }
</script>

<div class="min-h-screen flex flex-col bg-surface-dim">
  <!-- Navigation -->
  <nav class="bg-surface/80 backdrop-blur-lg border-b border-slate-100 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <div
            class="w-9 h-9 rounded-xl bg-gradient-to-br from-primary to-primary-dark flex items-center justify-center shadow-sm"
          >
            <svg
              class="w-5 h-5 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="1.5"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M7.864 4.243A7.5 7.5 0 0119.5 10.5c0 2.92-.556 5.709-1.568 8.268M5.742 6.364A7.465 7.465 0 004 10.5a7.464 7.464 0 01-1.15 3.993m1.989 3.559A11.209 11.209 0 008.25 10.5a3.75 3.75 0 117.5 0c0 .527-.021 1.049-.064 1.565M12 10.5a14.94 14.94 0 01-3.6 9.75m6.633-4.596a18.666 18.666 0 01-2.485 5.33"
              />
            </svg>
          </div>
          <div>
            <h1 class="text-lg font-display text-slate-800 leading-tight">CytoLens</h1>
            <p class="text-[10px] text-slate-400 font-medium tracking-wider uppercase leading-none">
              Breast Cancer Predictor
            </p>
          </div>
        </div>

        <!-- Desktop Nav -->
        <div class="hidden sm:flex items-center gap-1">
          <button
            class="nav-link cursor-pointer {currentSection === 'predictor'
              ? 'nav-link-active'
              : ''}"
            onclick={() => navigate('predictor')}
          >
            Predictor
          </button>
          <button
            class="nav-link cursor-pointer {currentSection === 'about' ? 'nav-link-active' : ''}"
            onclick={() => navigate('about')}
          >
            About
          </button>
        </div>

        <!-- Mobile menu button -->
        <button
          class="sm:hidden p-2 rounded-lg text-slate-500 hover:bg-surface-hover transition-colors cursor-pointer"
          onclick={() => (mobileMenuOpen = !mobileMenuOpen)}
        >
          <svg
            class="w-5 h-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
          >
            {#if mobileMenuOpen}
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            {:else}
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M3.75 9h16.5m-16.5 6.75h16.5"
              />
            {/if}
          </svg>
        </button>
      </div>

      <!-- Mobile Nav -->
      {#if mobileMenuOpen}
        <div class="sm:hidden border-t border-slate-100 py-2 animate-fade-in">
          <button
            class="w-full text-left px-4 py-2.5 text-sm font-medium rounded-lg transition-colors cursor-pointer {currentSection ===
            'predictor'
              ? 'text-primary bg-primary-50'
              : 'text-slate-600 hover:bg-surface-hover'}"
            onclick={() => navigate('predictor')}
          >
            Predictor
          </button>
          <button
            class="w-full text-left px-4 py-2.5 text-sm font-medium rounded-lg transition-colors cursor-pointer {currentSection ===
            'about'
              ? 'text-primary bg-primary-50'
              : 'text-slate-600 hover:bg-surface-hover'}"
            onclick={() => navigate('about')}
          >
            About
          </button>
        </div>
      {/if}
    </div>
  </nav>

  <!-- Content -->
  {#if currentSection === 'predictor'}
    <div class="flex-1 flex flex-col lg:flex-row">
      <!-- Sidebar -->
      <aside
        class="w-full lg:w-[340px] xl:w-[380px] bg-surface border-b lg:border-b-0 lg:border-r border-slate-100 overflow-y-auto lg:max-h-[calc(100vh-64px)]"
      >
        <SliderPanel />
      </aside>

      <!-- Main content -->
      <main class="flex-1 p-4 lg:p-8 overflow-y-auto lg:max-h-[calc(100vh-64px)]">
        <div class="max-w-5xl mx-auto">
          <!-- Hero description -->
          <div class="mb-6 lg:mb-8 animate-fade-up">
            <h2 class="font-display text-2xl lg:text-3xl text-slate-800 mb-2">Cytology Analysis</h2>
            <p class="text-sm text-slate-500 leading-relaxed max-w-2xl">
              Adjust the cell nuclei measurements in the sidebar to generate a real-time malignancy
              prediction using a logistic regression model trained on the Wisconsin Diagnostic
              Breast Cancer dataset.
            </p>
          </div>

          <!-- Dashboard grid -->
          <div class="grid grid-cols-1 xl:grid-cols-3 gap-4 lg:gap-6">
            <div class="xl:col-span-2 animate-fade-up delay-100">
              <RadarChart />
            </div>
            <div class="animate-fade-up delay-200">
              <PredictionPanel />
            </div>
          </div>
        </div>
      </main>
    </div>
  {:else}
    <main class="flex-1 overflow-y-auto">
      <AboutSection />
    </main>
  {/if}
</div>
