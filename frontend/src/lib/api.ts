import type { FeatureInfo, Preset, PredictionResult } from './types';

export async function fetchFeatures(): Promise<{
  features: FeatureInfo[];
  radar_categories: string[];
  presets: Preset[];
}> {
  const res = await fetch('/api/features');
  if (!res.ok) throw new Error(`Failed to fetch features: ${res.status}`);
  return res.json();
}

export async function fetchPrediction(features: Record<string, number>): Promise<PredictionResult> {
  const res = await fetch('/api/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ features }),
  });
  if (!res.ok) throw new Error(`Failed to fetch prediction: ${res.status}`);
  return res.json();
}
