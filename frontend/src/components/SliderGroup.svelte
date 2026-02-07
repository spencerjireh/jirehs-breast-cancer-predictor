<script lang="ts">
  import type { FeatureInfo } from '../lib/types';

  let {
    label,
    features,
    values = $bindable(),
  }: {
    label: string;
    features: FeatureInfo[];
    values: Record<string, number>;
  } = $props();

  let collapsed = $state(false);

  function onInput(key: string, e: Event) {
    const target = e.target as HTMLInputElement;
    values[key] = parseFloat(target.value);
    values = values;
  }
</script>

<div class="mb-4">
  <button
    class="w-full flex items-center justify-between py-2 px-3 bg-accent text-white rounded-md text-sm font-medium hover:bg-accent-light transition-colors cursor-pointer"
    onclick={() => (collapsed = !collapsed)}
  >
    <span>{label}</span>
    <span class="text-xs">{collapsed ? '+' : '-'}</span>
  </button>

  {#if !collapsed}
    <div class="mt-2 space-y-3 px-1">
      {#each features as feature (feature.key)}
        <div>
          <div class="flex justify-between text-xs text-gray-600 mb-1">
            <span>{feature.label}</span>
            <span class="font-mono">{(values[feature.key] ?? feature.mean).toFixed(4)}</span>
          </div>
          <input
            type="range"
            min={0}
            max={feature.max}
            step={feature.max / 200}
            value={values[feature.key] ?? feature.mean}
            oninput={(e) => onInput(feature.key, e)}
          />
        </div>
      {/each}
    </div>
  {/if}
</div>
