export interface PredictInput {
  age: number;
  gender: number;
  diabetes: number;
  hypertension: number;
  hospital_before: number;
  infection_freq: number;
  microbe_name?: string;
}

export interface DrugResult {
  drug_code: string;
  drug_name: string;
  result: "S" | "R";
  confidence: number;
}

export interface PredictResponse {
  all_drugs: DrugResult[];
  best_drug: DrugResult | null;
  sensitive: DrugResult[];
  resistant: DrugResult[];
}

export interface HistoryRecord {
  id: number;
  timestamp: string;
  input: PredictInput;
  result: PredictResponse;
}
