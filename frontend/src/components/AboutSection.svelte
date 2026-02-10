<script lang="ts">
  import katex from 'katex';
  import 'katex/dist/katex.min.css';

  function tex(latex: string): string {
    return katex.renderToString(latex, { displayMode: true, throwOnError: false });
  }

  const features = [
    {
      name: 'Radius',
      desc: 'Mean distance from the center of the nucleus to points on its perimeter, averaged across all nuclei in the image.',
    },
    {
      name: 'Texture',
      desc: 'Standard deviation of gray-scale pixel intensities, capturing surface roughness of the nucleus.',
    },
    {
      name: 'Perimeter',
      desc: 'Total boundary length of the nucleus contour in the digitized image.',
    },
    {
      name: 'Area',
      desc: 'Total area enclosed by the nucleus contour, measured in pixels squared.',
    },
    {
      name: 'Smoothness',
      desc: 'Local variation in radius lengths, quantifying how irregular the nuclear boundary is.',
    },
    {
      name: 'Compactness',
      desc: 'Computed as (perimeter\u00B2 / area) \u2212 1. Higher values indicate more irregular shapes.',
    },
    {
      name: 'Concavity',
      desc: 'Severity of concave portions of the nucleus contour, measuring how deeply the boundary folds inward.',
    },
    {
      name: 'Concave Points',
      desc: 'Number of concave (inward-bending) segments along the nucleus contour.',
    },
    {
      name: 'Symmetry',
      desc: 'Difference in length between lines perpendicular to the major axis on either side of the nucleus.',
    },
    {
      name: 'Fractal Dimension',
      desc: 'Boundary complexity measured via the "coastline approximation" \u2212 1. Higher values indicate more complex, jagged edges.',
    },
  ];

  const methodologyTopics = [
    {
      title: 'Logistic Regression',
      paragraphs: [
        'Logistic regression models the probability of a binary outcome (benign vs. malignant) by passing a linear combination of features through the sigmoid function. Unlike linear regression, the output is bounded between 0 and 1, making it interpretable as a probability.',
        'The model learns a weight (coefficient) for each of the 30 features. A positive weight means higher values of that feature push the prediction toward malignant; a negative weight pushes toward benign. This transparency is valuable in medical contexts.',
        'The decision boundary is linear in feature space: a hyperplane separating the two classes. Despite this simplicity, logistic regression performs well on WDBC because the classes are largely linearly separable after standardization.',
      ],
      formula:
        '\\sigma(z) = \\frac{1}{1 + e^{-z}}, \\quad z = w_0 + w_1 x_1 + w_2 x_2 + \\cdots + w_{30} x_{30}',
    },
    {
      title: 'Feature Standardization',
      paragraphs: [
        'StandardScaler transforms each feature to have zero mean and unit variance using the z-score formula. This is critical because the 30 features have vastly different scales -- radius is measured in microns while fractal dimension is a small decimal.',
        'Without standardization, features with larger numeric ranges would dominate the gradient updates during training, preventing the optimizer from converging efficiently. Standardization ensures all features contribute proportionally.',
        'The scaler is fit only on training data and then applied to test data, preventing data leakage. CytoLens stores the fitted scaler alongside the model so that user inputs are transformed identically at inference time.',
      ],
      formula:
        'z = \\frac{x - \\mu}{\\sigma}, \\quad \\mu = \\text{sample mean},\\; \\sigma = \\text{sample std dev}',
    },
    {
      title: 'L2 Regularization (Ridge)',
      paragraphs: [
        'L2 regularization adds a penalty term proportional to the squared magnitude of the model weights. This discourages any single coefficient from growing too large, which reduces overfitting -- especially important with only 569 samples.',
        'The WDBC features are highly correlated (e.g., radius, perimeter, and area all measure nuclear size). Without regularization, correlated features can produce unstable, inflated coefficients. L2 shrinks them toward zero smoothly.',
        'The regularization strength is controlled by the inverse parameter C. Smaller C means stronger regularization. scikit-learn defaults to C=1.0, which provides moderate regularization suitable for this dataset.',
      ],
      formula:
        '\\mathcal{L} = \\underbrace{-\\sum_{i} \\left[ y_i \\log(\\hat{y}_i) + (1 - y_i) \\log(1 - \\hat{y}_i) \\right]}_{\\text{cross-entropy loss}} + \\underbrace{\\frac{1}{2C} \\sum_j w_j^2}_{\\text{L2 penalty}}',
    },
    {
      title: 'LBFGS Optimization',
      paragraphs: [
        'Limited-memory Broyden-Fletcher-Goldfarb-Shanno (L-BFGS) is a quasi-Newton optimization method. Unlike basic gradient descent, which uses only first-order gradient information, L-BFGS approximates the inverse Hessian matrix to find better search directions.',
        'This curvature information allows L-BFGS to converge in far fewer iterations than gradient descent, making it well-suited for moderately sized problems like WDBC (569 samples, 30 features).',
        'L-BFGS stores only a few vectors to approximate the Hessian rather than the full matrix, keeping memory usage low -- hence "limited-memory." It is the default solver for logistic regression in scikit-learn when L2 penalty is used.',
      ],
      formula: null,
    },
    {
      title: 'Evaluation Metrics',
      paragraphs: [
        'Precision measures the fraction of predicted positives that are actually positive. In cancer screening, high precision for "malignant" means fewer false alarms -- patients predicted malignant almost certainly have malignant cells.',
        'Recall (sensitivity) measures the fraction of actual positives that are correctly identified. High recall for "benign" (0.99) means almost no benign cases are misclassified as malignant, reducing unnecessary patient anxiety and invasive procedures.',
        'F1 score is the harmonic mean of precision and recall, providing a single metric that balances both concerns. The harmonic mean penalizes extreme imbalances, so a high F1 requires both precision and recall to be strong.',
      ],
      formula:
        'F_1 = \\frac{2 \\times \\text{Precision} \\times \\text{Recall}}{\\text{Precision} + \\text{Recall}}, \\quad \\text{Precision} = \\frac{TP}{TP + FP}, \\quad \\text{Recall} = \\frac{TP}{TP + FN}',
    },
    {
      title: 'Train-Test Split',
      paragraphs: [
        'The dataset is split 80/20: 455 samples for training and 114 for testing. The model never sees test data during training, providing an unbiased estimate of generalization performance.',
        'A fixed random_state seed ensures reproducibility -- the same split is used every time the model is retrained, making experiments comparable and results verifiable.',
        'Standardization parameters (mean and standard deviation) are computed from training data only, then applied to both sets. Fitting the scaler on the full dataset would leak information from the test set into the model, producing over-optimistic accuracy estimates.',
      ],
      formula: null,
    },
    {
      title: 'Feature Statistics (Mean, SE, Worst)',
      paragraphs: [
        'Each of the 10 base morphological features is summarized with three statistics, yielding 30 total features. The mean captures the central tendency across all nuclei in the FNA sample.',
        'Standard error (SE) quantifies the variability of measurements across nuclei. High SE in a feature like radius suggests heterogeneous nuclear sizes, which can be a hallmark of malignancy.',
        'The "worst" value is the mean of the three largest nuclei for each feature. This captures the most abnormal cells in the sample, which are often the most diagnostically informative since malignant tumors tend to produce outlier nuclei.',
      ],
      formula:
        'SE = \\frac{s}{\\sqrt{n}}, \\quad s = \\text{sample std dev},\\; n = \\text{number of nuclei}',
    },
  ];

  const metrics = {
    headline: [
      { label: 'Accuracy', value: '97.4%' },
      { label: 'Precision', value: '0.97' },
      { label: 'F1 Score', value: '0.97' },
    ],
    perClass: [
      { label: 'Benign', precision: '0.97', recall: '0.99', f1: '0.98', support: 71 },
      { label: 'Malignant', precision: '0.98', recall: '0.95', f1: '0.96', support: 43 },
    ],
  };

  const limitations = [
    {
      title: 'Not a clinical diagnostic tool',
      desc: 'CytoLens has not been validated for clinical decision-making and must not be used to diagnose or treat any medical condition.',
    },
    {
      title: 'Limited dataset',
      desc: 'The WDBC dataset contains 569 samples from a single institution (University of Wisconsin). Performance on data from other populations, imaging equipment, or preparation methods is unknown.',
    },
    {
      title: 'Linear classifier',
      desc: 'Logistic Regression was chosen for its interpretability, but it assumes a linear decision boundary. More complex models (e.g., gradient-boosted trees, neural networks) may capture non-linear patterns.',
    },
    {
      title: 'No uncertainty quantification',
      desc: 'The model outputs a single probability estimate without confidence intervals or calibration guarantees.',
    },
    {
      title: 'Manual slider inputs',
      desc: 'Users manually set feature values via sliders rather than extracting them from actual cell images. In a clinical workflow, feature extraction would be automated from microscopy images.',
    },
  ];
</script>

<div class="max-w-4xl 2xl:max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 lg:py-12">
  <!-- Hero -->
  <div class="mb-12 animate-fade-up">
    <h1 class="font-display text-2xl sm:text-3xl lg:text-4xl 2xl:text-5xl text-slate-800 mb-3">
      About CytoLens
    </h1>
    <p
      class="text-sm sm:text-base 2xl:text-lg text-slate-500 leading-relaxed max-w-2xl 2xl:max-w-3xl mb-3"
    >
      CytoLens is an interactive machine learning tool that predicts breast cancer malignancy from
      cell nucleus measurements. Users adjust 30 morphological features via sliders and see
      real-time predictions with a radar chart visualization of the input data.
    </p>
    <p
      class="text-sm sm:text-base 2xl:text-lg text-slate-500 leading-relaxed max-w-2xl 2xl:max-w-3xl"
    >
      It covers end-to-end ML deployment: model training, a Python API, a modern reactive frontend,
      and containerized delivery -- all in a single, production-ready application.
    </p>
  </div>

  <!-- How It Works + The Dataset -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 mb-6 sm:mb-8">
    <!-- How it works -->
    <div class="card p-4 sm:p-6 animate-fade-up delay-100">
      <div class="flex items-center gap-2 mb-4">
        <div class="w-8 h-8 rounded-lg bg-primary-50 text-primary flex items-center justify-center">
          <svg
            class="w-4 h-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="1.5"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5"
            />
          </svg>
        </div>
        <h2 class="text-base font-semibold text-slate-700">How It Works</h2>
      </div>
      <div class="space-y-3 text-sm 2xl:text-base text-slate-600 leading-relaxed">
        <div class="flex gap-3">
          <div
            class="w-6 h-6 rounded-full bg-primary-50 text-primary flex items-center justify-center flex-shrink-0 text-xs font-semibold mt-0.5"
          >
            1
          </div>
          <p>
            A fine needle aspirate (FNA) is taken from a breast mass. The sample is stained and a
            digitized image of the cell nuclei is produced under a microscope.
          </p>
        </div>
        <div class="flex gap-3">
          <div
            class="w-6 h-6 rounded-full bg-primary-50 text-primary flex items-center justify-center flex-shrink-0 text-xs font-semibold mt-0.5"
          >
            2
          </div>
          <p>
            Ten real-valued features describing nuclear morphology are computed for each nucleus.
            Three statistics are recorded per feature -- mean, standard error, and worst (largest)
            -- yielding 30 measurements total.
          </p>
        </div>
        <div class="flex gap-3">
          <div
            class="w-6 h-6 rounded-full bg-primary-50 text-primary flex items-center justify-center flex-shrink-0 text-xs font-semibold mt-0.5"
          >
            3
          </div>
          <p>
            The 30 measurements are standardized and fed into a logistic regression model, which
            outputs a probability of malignancy. A radar chart visualizes the normalized feature
            values across all three statistic groups.
          </p>
        </div>
      </div>
    </div>

    <!-- The Dataset -->
    <div class="card p-4 sm:p-6 animate-fade-up delay-200">
      <div class="flex items-center gap-2 mb-4">
        <div class="w-8 h-8 rounded-lg bg-primary-50 text-primary flex items-center justify-center">
          <svg
            class="w-4 h-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="1.5"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6"
            />
          </svg>
        </div>
        <h2 class="text-base font-semibold text-slate-700">The Dataset</h2>
      </div>
      <p class="text-sm 2xl:text-base text-slate-600 leading-relaxed mb-3">
        The model is trained on the <strong>Wisconsin Diagnostic Breast Cancer (WDBC)</strong>
        dataset from the UCI Machine Learning Repository. It contains
        <strong>569 samples</strong> -- 357 benign and 212 malignant -- each described by 30 features
        derived from digitized FNA images.
      </p>
      <p class="text-sm 2xl:text-base text-slate-600 leading-relaxed mb-3">
        The 30 features come from 10 nuclear morphology measurements, each recorded as three
        statistics: mean value across all nuclei, standard error, and worst (mean of the three
        largest values).
      </p>
      <p class="text-sm 2xl:text-base text-slate-600 leading-relaxed">
        <strong>Training pipeline:</strong> features are standardized with
        <code class="text-xs bg-slate-50 px-1 py-0.5 rounded">StandardScaler</code>, then classified
        with Logistic Regression (L2 regularization, LBFGS solver, 80/20 train-test split).
      </p>
    </div>
  </div>

  <!-- Model Performance -->
  <div class="card p-4 sm:p-6 mb-8 animate-fade-up delay-200">
    <div class="flex items-center gap-2 mb-5">
      <div class="w-8 h-8 rounded-lg bg-primary-50 text-primary flex items-center justify-center">
        <svg
          class="w-4 h-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="1.5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.562.562 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.562.562 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z"
          />
        </svg>
      </div>
      <h2 class="text-base font-semibold text-slate-700">Model Performance</h2>
    </div>

    <!-- Headline stats -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4 mb-4 sm:mb-6">
      {#each metrics.headline as stat}
        <div
          class="flex sm:block items-center gap-3 sm:gap-0 sm:text-center p-3 rounded-xl bg-primary-50/50"
        >
          <div class="text-xl sm:text-2xl font-bold text-primary">{stat.value}</div>
          <div class="text-xs text-slate-500 sm:mt-1">{stat.label}</div>
        </div>
      {/each}
    </div>

    <!-- Per-class table -->
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-slate-100">
            <th
              class="text-left py-2 pr-4 text-xs font-medium text-slate-400 uppercase tracking-wider"
              >Class</th
            >
            <th
              class="text-center py-2 px-3 text-xs font-medium text-slate-400 uppercase tracking-wider"
              >Precision</th
            >
            <th
              class="text-center py-2 px-3 text-xs font-medium text-slate-400 uppercase tracking-wider"
              >Recall</th
            >
            <th
              class="text-center py-2 px-3 text-xs font-medium text-slate-400 uppercase tracking-wider"
              >F1</th
            >
            <th
              class="text-center py-2 pl-3 text-xs font-medium text-slate-400 uppercase tracking-wider"
              >Support</th
            >
          </tr>
        </thead>
        <tbody>
          {#each metrics.perClass as row}
            <tr class="border-b border-slate-50 last:border-0">
              <td class="py-2.5 pr-4">
                <div class="flex items-center gap-1.5">
                  <span
                    class="w-2 h-2 rounded-full {row.label === 'Benign'
                      ? 'bg-benign'
                      : 'bg-malignant'}"
                  ></span>
                  <span class="font-medium text-slate-700">{row.label}</span>
                </div>
              </td>
              <td class="text-center py-2.5 px-3 text-slate-600">{row.precision}</td>
              <td class="text-center py-2.5 px-3 text-slate-600">{row.recall}</td>
              <td class="text-center py-2.5 px-3 text-slate-600">{row.f1}</td>
              <td class="text-center py-2.5 pl-3 text-slate-600">{row.support}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    <p class="text-xs text-slate-400 mt-4 leading-relaxed">
      Evaluated on a held-out 20% test split (114 samples). High recall for benign (0.99) means very
      few benign cases are misclassified as malignant, while high precision for malignant (0.98)
      means the model rarely raises false alarms. The balanced F1 scores indicate consistent
      performance across both classes.
    </p>
  </div>

  <!-- Measured Features -->
  <div class="card p-4 sm:p-6 mb-8 animate-fade-up delay-300">
    <div class="flex items-center gap-2 mb-4">
      <div class="w-8 h-8 rounded-lg bg-primary-50 text-primary flex items-center justify-center">
        <svg
          class="w-4 h-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="1.5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M3.375 19.5h17.25m-17.25 0a1.125 1.125 0 01-1.125-1.125M3.375 19.5h7.5c.621 0 1.125-.504 1.125-1.125m-9.75 0V5.625m0 12.75v-1.5c0-.621.504-1.125 1.125-1.125m18.375 2.625V5.625m0 12.75c0 .621-.504 1.125-1.125 1.125m1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125m0 3.75h-7.5A1.125 1.125 0 0112 18.375m9.75-12.75c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125m19.5 0v1.5c0 .621-.504 1.125-1.125 1.125M2.25 5.625v1.5c0 .621.504 1.125 1.125 1.125m0 0h17.25m-17.25 0h7.5c.621 0 1.125.504 1.125 1.125M3.375 8.25c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125m17.25-3.75h-7.5c-.621 0-1.125.504-1.125 1.125m8.625-1.125c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125M12 10.875v-1.5m0 1.5c0 .621-.504 1.125-1.125 1.125M12 10.875c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125M13.125 12h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125M20.625 12c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5M12 14.625v-1.5m0 1.5c0 .621-.504 1.125-1.125 1.125M12 14.625c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125m0 0v1.5c0 .621-.504 1.125-1.125 1.125M12 18.375h-7.5"
          />
        </svg>
      </div>
      <div>
        <h2 class="text-base font-semibold text-slate-700">Measured Features</h2>
        <p class="text-[11px] text-slate-400">
          10 base features, each with mean, SE, and worst statistics
        </p>
      </div>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
      {#each features as feature, i}
        <div class="flex items-start gap-3 p-3 rounded-xl hover:bg-surface-hover transition-colors">
          <span
            class="text-[10px] font-bold text-primary bg-primary-50 w-5 h-5 rounded-md flex items-center justify-center flex-shrink-0 mt-0.5"
          >
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

  <!-- ML & Statistics Methodology -->
  <div class="card p-4 sm:p-6 mb-8 animate-fade-up delay-400">
    <div class="flex items-center gap-2 mb-4">
      <div class="w-8 h-8 rounded-lg bg-primary-50 text-primary flex items-center justify-center">
        <svg
          class="w-4 h-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="1.5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5"
          />
        </svg>
      </div>
      <div>
        <h2 class="text-base font-semibold text-slate-700">ML & Statistics Methodology</h2>
        <p class="text-[11px] text-slate-400">
          The statistical and algorithmic foundations behind the model
        </p>
      </div>
    </div>
    <div class="space-y-4">
      {#each methodologyTopics as topic, i}
        <div class="p-4 rounded-xl bg-surface-dim">
          <div class="flex items-start gap-3">
            <span
              class="text-[10px] font-bold text-primary bg-primary-50 w-5 h-5 rounded-md flex items-center justify-center flex-shrink-0 mt-0.5"
            >
              {i + 1}
            </span>
            <div class="min-w-0">
              <div class="text-sm font-medium text-slate-700 mb-2">{topic.title}</div>
              <div class="space-y-2">
                {#each topic.paragraphs as paragraph}
                  <p class="text-xs 2xl:text-sm text-slate-500 leading-relaxed">{paragraph}</p>
                {/each}
              </div>
              {#if topic.formula}
                <div
                  class="mt-3 p-3 rounded-lg bg-slate-50 border border-slate-100 overflow-x-auto"
                >
                  {@html tex(topic.formula)}
                </div>
              {/if}
            </div>
          </div>
        </div>
      {/each}
    </div>
  </div>

  <!-- Limitations -->
  <div class="card p-4 sm:p-6 mb-8 animate-fade-up delay-400">
    <div class="flex items-center gap-2 mb-4">
      <div class="w-8 h-8 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center">
        <svg
          class="w-4 h-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="1.5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z"
          />
        </svg>
      </div>
      <h2 class="text-base font-semibold text-slate-700">Limitations</h2>
    </div>
    <div class="space-y-3">
      {#each limitations as item, i}
        <div class="flex gap-3 p-3 rounded-xl bg-surface-dim">
          <span
            class="text-[10px] font-bold text-amber-600 bg-amber-50 w-5 h-5 rounded-md flex items-center justify-center flex-shrink-0 mt-0.5"
          >
            {i + 1}
          </span>
          <div>
            <div class="text-sm font-medium text-slate-700">{item.title}</div>
            <div class="text-xs text-slate-400 mt-0.5 leading-relaxed">{item.desc}</div>
          </div>
        </div>
      {/each}
    </div>
  </div>

  <!-- Acknowledgments -->
  <div class="card p-4 sm:p-6 mb-8 animate-fade-up delay-400">
    <div class="flex items-center gap-2 mb-4">
      <div class="w-8 h-8 rounded-lg bg-primary-50 text-primary flex items-center justify-center">
        <svg
          class="w-4 h-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="1.5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z"
          />
        </svg>
      </div>
      <h2 class="text-base font-semibold text-slate-700">Acknowledgments</h2>
    </div>
    <div class="space-y-3 text-sm 2xl:text-base text-slate-600 leading-relaxed">
      <p>
        This project was inspired by
        <a
          href="https://www.youtube.com/@alejaborgosnextaim"
          target="_blank"
          rel="noopener noreferrer"
          class="text-primary hover:text-primary-dark underline underline-offset-2"
          >Alejandro AO's</a
        >
        breast cancer predictor tutorial. CytoLens extends the original concept with a redesigned Svelte
        5 frontend, interactive radar chart, responsive layout, and containerized deployment.
      </p>
      <p>
        <strong>Dataset citation:</strong> Wolberg, W.H., Street, W.N., & Mangasarian, O.L. (1995). Breast
        Cancer Wisconsin (Diagnostic) Data Set. UCI Machine Learning Repository, University of Wisconsin-Madison.
      </p>
      <p>
        Built by <strong>Spencer Jireh Cebrian</strong>.
      </p>
    </div>
  </div>

  <!-- Footer -->
  <div class="mt-12 text-center">
    <p class="font-display text-lg text-slate-300 mb-1">CytoLens</p>
    <p class="text-xs text-slate-400">Not intended for clinical use.</p>
  </div>
</div>
