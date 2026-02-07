<script lang="ts">
  import { groupedFeatures, featureValues } from '../lib/stores';
  import SliderGroup from './SliderGroup.svelte';
  import type { GroupedFeatures } from '../lib/types';

  let grouped: GroupedFeatures = $state({ mean: [], se: [], worst: [] });
  let values: Record<string, number> = $state({});

  groupedFeatures.subscribe((v) => (grouped = v));
  featureValues.subscribe((v) => (values = v));

  function handleSliderChange(key: string, value: number) {
    featureValues.update((v) => ({ ...v, [key]: value }));
  }

  const groupIcons = {
    mean: `<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" /></svg>`,
    se: `<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M7.5 14.25v2.25m3-4.5v4.5m3-6.75v6.75m3-9v9M6 20.25h12A2.25 2.25 0 0020.25 18V6A2.25 2.25 0 0018 3.75H6A2.25 2.25 0 003.75 6v12A2.25 2.25 0 006 20.25z" /></svg>`,
    worst: `<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" /></svg>`,
  };

  const groupDescriptions: Record<string, string> = {
    mean: 'Average value of each measurement across the cell nuclei.',
    se: 'Standard error (variability) of each measurement.',
    worst: 'Largest (most extreme) value of each measurement.',
  };
</script>

<div class="p-4 lg:p-5">
  <!-- Header -->
  <div class="mb-5">
    <div class="flex items-center gap-2 mb-1">
      <svg
        class="w-4 h-4 text-primary"
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
      <h2 class="text-sm font-semibold text-slate-700">Cell Nuclei Measurements</h2>
    </div>
    <p class="text-xs text-slate-400 leading-relaxed">30 features grouped by statistical measure</p>
  </div>

  <div class="space-y-3">
    <SliderGroup
      label="Mean Values"
      description={groupDescriptions.mean}
      icon={groupIcons.mean}
      features={grouped.mean}
      {values}
      onchange={handleSliderChange}
      defaultOpen={true}
    />
    <SliderGroup
      label="Standard Error"
      description={groupDescriptions.se}
      icon={groupIcons.se}
      features={grouped.se}
      {values}
      onchange={handleSliderChange}
      defaultOpen={false}
    />
    <SliderGroup
      label="Worst Values"
      description={groupDescriptions.worst}
      icon={groupIcons.worst}
      features={grouped.worst}
      {values}
      onchange={handleSliderChange}
      defaultOpen={false}
    />
  </div>
</div>
