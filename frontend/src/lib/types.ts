export interface FeatureInfo {
  key: string;
  label: string;
  group: 'mean' | 'se' | 'worst';
  description: string;
  min: number;
  max: number;
  mean: number;
}

export interface RadarData {
  mean: number[];
  se: number[];
  worst: number[];
}

export interface PredictionResult {
  prediction: 'Benign' | 'Malignant';
  probability_benign: number;
  probability_malignant: number;
  radar_data: RadarData;
}

export interface Preset {
  label: string;
  values: Record<string, number>;
}

export interface GroupedFeatures {
  mean: FeatureInfo[];
  se: FeatureInfo[];
  worst: FeatureInfo[];
}
