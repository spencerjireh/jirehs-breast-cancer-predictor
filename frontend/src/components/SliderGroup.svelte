<script lang="ts">
  import type { FeatureInfo } from '../lib/types';

  let {
    label,
    description = '',
    icon = '',
    features,
    values,
    onchange,
    defaultOpen = false,
    alwaysOpen = false,
  }: {
    label: string;
    description?: string;
    icon?: string;
    features: FeatureInfo[];
    values: Record<string, number>;
    onchange: (key: string, value: number) => void;
    defaultOpen?: boolean;
    alwaysOpen?: boolean;
  } = $props();

  let collapsed = $state(!defaultOpen && !alwaysOpen);

  function onInput(key: string, e: Event) {
    const target = e.target as HTMLInputElement;
    onchange(key, parseFloat(target.value));
  }

  function getPercent(feature: FeatureInfo): number {
    const val = values[feature.key] ?? feature.mean;
    return Math.min(100, Math.max(0, (val / feature.max) * 100));
  }
</script>

<div class="card overflow-hidden">
  <!-- Header -->
  {#if alwaysOpen}
    <div class="flex items-center gap-3 p-3.5">
      <div
        class="w-8 h-8 rounded-lg bg-primary-50 text-primary flex items-center justify-center flex-shrink-0"
      >
        {@html icon}
      </div>
      <div class="flex-1">
        <div class="text-sm font-semibold text-slate-700">{label}</div>
        <div class="text-[11px] text-slate-400 leading-snug">{description}</div>
      </div>
      <span class="text-[10px] font-medium text-slate-400 bg-slate-50 px-2 py-0.5 rounded-full">
        {features.length}
      </span>
    </div>
  {:else}
    <button
      class="w-full flex items-center gap-3 p-3.5 hover:bg-surface-hover transition-colors duration-150 cursor-pointer"
      onclick={() => (collapsed = !collapsed)}
    >
      <div
        class="w-8 h-8 rounded-lg bg-primary-50 text-primary flex items-center justify-center flex-shrink-0"
      >
        {@html icon}
      </div>
      <div class="flex-1 text-left">
        <div class="text-sm font-semibold text-slate-700">{label}</div>
        <div class="text-[11px] text-slate-400 leading-snug">{description}</div>
      </div>
      <div class="flex items-center gap-2">
        <span class="text-[10px] font-medium text-slate-400 bg-slate-50 px-2 py-0.5 rounded-full">
          {features.length}
        </span>
        <svg
          class="w-4 h-4 text-slate-400 transition-transform duration-200 {collapsed
            ? ''
            : 'rotate-180'}"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
        </svg>
      </div>
    </button>
  {/if}

  <!-- Slider content -->
  {#if alwaysOpen || !collapsed}
    <div class="border-t border-slate-50 px-4 py-3 space-y-4 animate-fade-in">
      {#each features as feature (feature.key)}
        <div class="group">
          <div class="flex justify-between items-baseline mb-0.5">
            <span class="text-xs font-medium text-slate-600">{feature.label}</span>
            <span class="text-xs font-mono text-primary font-medium tabular-nums">
              {(values[feature.key] ?? feature.mean).toFixed(4)}
            </span>
          </div>
          {#if feature.description}
            <div class="text-[10px] text-slate-400 leading-snug mb-1.5">{feature.description}</div>
          {/if}
          <div class="relative">
            <div
              class="absolute inset-0 h-1.5 top-[7px] rounded-full bg-slate-100 overflow-hidden pointer-events-none"
            >
              <div
                class="h-full rounded-full transition-all duration-150"
                style="width: {getPercent(
                  feature,
                )}%; background: linear-gradient(90deg, var(--color-primary-100), var(--color-primary));"
              ></div>
            </div>
            <input
              type="range"
              min={0}
              max={feature.max}
              step={feature.max / 200}
              value={values[feature.key] ?? feature.mean}
              oninput={(e) => onInput(feature.key, e)}
              class="relative z-10"
              style="background: transparent;"
            />
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
