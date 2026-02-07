import { writable, derived } from 'svelte/store';
import type { FeatureInfo, PredictionResult, GroupedFeatures } from './types';

export const featuresMeta = writable<FeatureInfo[]>([]);
export const featureValues = writable<Record<string, number>>({});
export const prediction = writable<PredictionResult | null>(null);
export const predicting = writable<boolean>(false);
export const radarCategories = writable<string[]>([]);

export const groupedFeatures = derived(featuresMeta, ($meta): GroupedFeatures => {
  return {
    mean: $meta.filter((f) => f.group === 'mean'),
    se: $meta.filter((f) => f.group === 'se'),
    worst: $meta.filter((f) => f.group === 'worst'),
  };
});
