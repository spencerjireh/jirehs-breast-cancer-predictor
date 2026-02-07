<script lang="ts">
  import { groupedFeatures, featureValues } from '../lib/stores';
  import { get } from 'svelte/store';
  import SliderGroup from './SliderGroup.svelte';
  import type { GroupedFeatures } from '../lib/types';

  let grouped: GroupedFeatures = $state({ mean: [], se: [], worst: [] });
  let values: Record<string, number> = $state({});

  groupedFeatures.subscribe((v) => (grouped = v));
  featureValues.subscribe((v) => (values = { ...v }));

  $effect(() => {
    featureValues.set(values);
  });
</script>

<div class="p-4">
  <h2 class="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-4">
    Cell Nuclei Measurements
  </h2>

  <SliderGroup label="Mean" features={grouped.mean} bind:values />
  <SliderGroup label="Standard Error" features={grouped.se} bind:values />
  <SliderGroup label="Worst" features={grouped.worst} bind:values />
</div>
