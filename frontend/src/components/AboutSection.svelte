<script lang="ts">
  const features = [
    { name: 'Radius', desc: 'Mean distance from center to points on the perimeter' },
    { name: 'Texture', desc: 'Standard deviation of gray-scale values' },
    { name: 'Perimeter', desc: 'Perimeter of the cell nucleus' },
    { name: 'Area', desc: 'Area of the cell nucleus' },
    { name: 'Smoothness', desc: 'Local variation in radius lengths' },
    { name: 'Compactness', desc: 'Perimeter squared divided by area minus one' },
    { name: 'Concavity', desc: 'Severity of concave portions of the contour' },
    { name: 'Concave Points', desc: 'Number of concave portions of the contour' },
    { name: 'Symmetry', desc: 'Symmetry of the cell nucleus' },
    { name: 'Fractal Dimension', desc: 'Coastline approximation minus one' },
  ];

  const techStack = [
    { label: 'Frontend', value: 'Svelte 5, Tailwind CSS, Plotly.js' },
    { label: 'Backend', value: 'FastAPI, Python 3.12' },
    { label: 'ML Model', value: 'Logistic Regression (scikit-learn)' },
    { label: 'Dataset', value: 'Wisconsin Diagnostic Breast Cancer (WDBC)' },
    { label: 'Deployment', value: 'Docker, single-container architecture' },
  ];
</script>

<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 lg:py-12">
  <!-- Hero -->
  <div class="mb-12 animate-fade-up">
    <h1 class="font-display text-3xl lg:text-4xl text-slate-800 mb-3">
      About CytoLens
    </h1>
    <p class="text-base text-slate-500 leading-relaxed max-w-2xl">
      A machine learning-powered tool for breast cancer malignancy prediction,
      built to assist cytology analysis using measurements from fine needle
      aspirate (FNA) of breast masses.
    </p>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
    <!-- How it works -->
    <div class="card p-6 animate-fade-up delay-100">
      <div class="flex items-center gap-2 mb-4">
        <div class="w-8 h-8 rounded-lg bg-primary-50 text-primary flex items-center justify-center">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
          </svg>
        </div>
        <h2 class="text-base font-semibold text-slate-700">How It Works</h2>
      </div>
      <div class="space-y-3 text-sm text-slate-600 leading-relaxed">
        <div class="flex gap-3">
          <div class="w-6 h-6 rounded-full bg-primary-50 text-primary flex items-center justify-center flex-shrink-0 text-xs font-semibold mt-0.5">1</div>
          <p>A fine needle aspirate (FNA) is taken from a breast mass, and a digitized image of the cell nuclei is produced.</p>
        </div>
        <div class="flex gap-3">
          <div class="w-6 h-6 rounded-full bg-primary-50 text-primary flex items-center justify-center flex-shrink-0 text-xs font-semibold mt-0.5">2</div>
          <p>Ten real-valued features are computed for each cell nucleus, with three statistical measures per feature (mean, standard error, worst).</p>
        </div>
        <div class="flex gap-3">
          <div class="w-6 h-6 rounded-full bg-primary-50 text-primary flex items-center justify-center flex-shrink-0 text-xs font-semibold mt-0.5">3</div>
          <p>These 30 measurements are fed into a logistic regression model that outputs a probability of malignancy.</p>
        </div>
      </div>
    </div>

    <!-- Model details -->
    <div class="card p-6 animate-fade-up delay-200">
      <div class="flex items-center gap-2 mb-4">
        <div class="w-8 h-8 rounded-lg bg-primary-50 text-primary flex items-center justify-center">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6" />
          </svg>
        </div>
        <h2 class="text-base font-semibold text-slate-700">Model Details</h2>
      </div>
      <p class="text-sm text-slate-600 leading-relaxed mb-4">
        The model uses <strong>Logistic Regression</strong> trained on the
        Wisconsin Diagnostic Breast Cancer (WDBC) dataset, which contains
        569 instances with 30 features each.
      </p>
      <p class="text-sm text-slate-600 leading-relaxed">
        Input features are standardized using a fitted scaler before prediction.
        The radar chart visualizes each feature group normalized to a 0--1 range
        for intuitive comparison.
      </p>
    </div>
  </div>

  <!-- Features table -->
  <div class="card p-6 mb-8 animate-fade-up delay-300">
    <div class="flex items-center gap-2 mb-4">
      <div class="w-8 h-8 rounded-lg bg-primary-50 text-primary flex items-center justify-center">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3.375 19.5h17.25m-17.25 0a1.125 1.125 0 01-1.125-1.125M3.375 19.5h7.5c.621 0 1.125-.504 1.125-1.125m-9.75 0V5.625m0 12.75v-1.5c0-.621.504-1.125 1.125-1.125m18.375 2.625V5.625m0 12.75c0 .621-.504 1.125-1.125 1.125m1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125m0 3.75h-7.5A1.125 1.125 0 0112 18.375m9.75-12.75c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125m19.5 0v1.5c0 .621-.504 1.125-1.125 1.125M2.25 5.625v1.5c0 .621.504 1.125 1.125 1.125m0 0h17.25m-17.25 0h7.5c.621 0 1.125.504 1.125 1.125M3.375 8.25c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125m17.25-3.75h-7.5c-.621 0-1.125.504-1.125 1.125m8.625-1.125c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125M12 10.875v-1.5m0 1.5c0 .621-.504 1.125-1.125 1.125M12 10.875c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125M13.125 12h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125M20.625 12c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5M12 14.625v-1.5m0 1.5c0 .621-.504 1.125-1.125 1.125M12 14.625c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125m0 0v1.5c0 .621-.504 1.125-1.125 1.125M12 18.375h-7.5" />
        </svg>
      </div>
      <div>
        <h2 class="text-base font-semibold text-slate-700">Measured Features</h2>
        <p class="text-[11px] text-slate-400">10 base features, each with mean, SE, and worst statistics</p>
      </div>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
      {#each features as feature, i}
        <div class="flex items-start gap-3 p-3 rounded-xl hover:bg-surface-hover transition-colors">
          <span class="text-[10px] font-bold text-primary bg-primary-50 w-5 h-5 rounded-md flex items-center justify-center flex-shrink-0 mt-0.5">
            {i + 1}
          </span>
          <div>
            <div class="text-sm font-medium text-slate-700">{feature.name}</div>
            <div class="text-xs text-slate-400 mt-0.5">{feature.desc}</div>
          </div>
        </div>
      {/each}
    </div>
  </div>

  <!-- Tech stack -->
  <div class="card p-6 animate-fade-up delay-400">
    <div class="flex items-center gap-2 mb-4">
      <div class="w-8 h-8 rounded-lg bg-primary-50 text-primary flex items-center justify-center">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5" />
        </svg>
      </div>
      <h2 class="text-base font-semibold text-slate-700">Tech Stack</h2>
    </div>
    <div class="space-y-2">
      {#each techStack as item}
        <div class="flex items-center justify-between py-2 border-b border-slate-50 last:border-0">
          <span class="text-sm font-medium text-slate-600">{item.label}</span>
          <span class="text-sm text-slate-400">{item.value}</span>
        </div>
      {/each}
    </div>
  </div>

  <!-- Footer -->
  <div class="mt-12 text-center">
    <p class="text-xs text-slate-400">
      Built as a demonstration of full-stack ML deployment.
      Not intended for clinical use.
    </p>
  </div>
</div>
