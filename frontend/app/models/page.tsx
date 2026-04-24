"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { getModelComparison } from "@/lib/api";
import { Trophy, Clock, Target, Zap, BarChart3 } from "lucide-react";

interface ModelMetrics {
  accuracy: number;
  f1: number;
  precision: number;
  recall: number;
}

interface ModelData {
  name: string;
  overall: ModelMetrics;
  train_time_sec: number;
  predict_time_sec: number;
}

interface ShapFeature {
  feature: string;
  importance: number;
}

export default function ModelsPage() {
  const [data, setData] = useState<Record<string, ModelData> | null>(null);
  const [bestKey, setBestKey] = useState("");
  const [shap, setShap] = useState<Record<string, ShapFeature[]> | null>(null);
  const [selectedDrug, setSelectedDrug] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getModelComparison()
      .then((raw: Record<string, unknown>) => {
        const best = (raw["_best_model"] as string) || "";
        setBestKey(best);

        const shapData = raw["_shap"] as Record<string, ShapFeature[]> | undefined;
        if (shapData && Object.keys(shapData).length > 0) {
          setShap(shapData);
          setSelectedDrug(Object.keys(shapData)[0]);
        }

        const models: Record<string, ModelData> = {};
        for (const [k, v] of Object.entries(raw)) {
          if (k.startsWith("_")) continue;
          models[k] = v as ModelData;
        }
        setData(models);
      })
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-8 space-y-4">
        <Skeleton className="h-10 w-64" />
        {[1, 2, 3].map((i) => (
          <Skeleton key={i} className="h-24 w-full rounded-xl" />
        ))}
      </div>
    );
  }

  if (!data || Object.keys(data).length === 0) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-8 text-center text-muted-foreground">
        No model comparison data. Train models first.
      </div>
    );
  }

  const sorted = Object.entries(data).sort(
    ([, a], [, b]) => b.overall.f1 - a.overall.f1
  );

  const drugNames: Record<string, string> = {
    "AMX/AMP": "Amoxicillin", "AMC": "Amox-Clav", "CZ": "Cefazolin",
    "FOX": "Cefoxitin", "CTX/CRO": "Cefotaxime", "IPM": "Imipenem",
    "GEN": "Gentamicin", "AN": "Amikacin", "Acide nalidixique": "Nalidixic Acid",
    "ofx": "Ofloxacin", "CIP": "Ciprofloxacin", "C": "Chloramphenicol",
    "Co-trimoxazole": "Co-trimoxazole", "Furanes": "Nitrofurantoin",
    "colistine": "Colistin",
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-semibold tracking-tight mb-2">
        Model Comparison
      </h1>
      <p className="text-muted-foreground mb-8">
        {sorted.length} ML models trained on <strong>9,595 samples</strong> across{" "}
        <strong>15 drugs</strong> with 29 engineered features + SHAP explainability.
      </p>

      {/* Best model highlight */}
      {bestKey && data[bestKey] && (
        <Card className="mb-8 border-2" style={{ borderColor: "#f59e0b" }}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Trophy className="h-5 w-5" style={{ color: "#f59e0b" }} />
              Best Model: {data[bestKey].name}
              <Badge
                className="ml-2"
                style={{
                  backgroundColor: "rgba(245,158,11,0.15)",
                  color: "#f59e0b",
                  border: "1px solid rgba(245,158,11,0.3)",
                }}
              >
                Active
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <p className="text-2xl font-bold font-mono">
                  {data[bestKey].overall.accuracy}%
                </p>
                <p className="text-xs text-muted-foreground">Accuracy</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold font-mono">
                  {data[bestKey].overall.f1}%
                </p>
                <p className="text-xs text-muted-foreground">F1 Score</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold font-mono">
                  {data[bestKey].overall.precision}%
                </p>
                <p className="text-xs text-muted-foreground">Precision</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold font-mono">
                  {data[bestKey].overall.recall}%
                </p>
                <p className="text-xs text-muted-foreground">Recall</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Comparison table */}
      <div className="rounded-xl border border-zinc-700 overflow-hidden mb-8">
        <table className="w-full">
          <thead>
            <tr
              className="border-b border-zinc-700"
              style={{ backgroundColor: "rgba(39,39,42,0.5)" }}
            >
              <th className="text-left text-xs font-medium text-muted-foreground p-3">
                #
              </th>
              <th className="text-left text-xs font-medium text-muted-foreground p-3">
                Model
              </th>
              <th className="text-left text-xs font-medium text-muted-foreground p-3">
                <div className="flex items-center gap-1">
                  <Target className="h-3 w-3" />
                  Accuracy
                </div>
              </th>
              <th className="text-left text-xs font-medium text-muted-foreground p-3">
                <div className="flex items-center gap-1">
                  <Zap className="h-3 w-3" />
                  F1 Score
                </div>
              </th>
              <th className="text-left text-xs font-medium text-muted-foreground p-3">
                Precision
              </th>
              <th className="text-left text-xs font-medium text-muted-foreground p-3">
                Recall
              </th>
            </tr>
          </thead>
          <tbody>
            {sorted.map(([key, model], i) => {
              const isBest = key === bestKey;
              return (
                <tr
                  key={key}
                  className="border-b border-zinc-800 last:border-0 transition-colors hover:bg-zinc-800/50"
                  style={
                    isBest
                      ? { backgroundColor: "rgba(245,158,11,0.05)" }
                      : {}
                  }
                >
                  <td className="p-3 text-sm text-muted-foreground">
                    {i + 1}
                  </td>
                  <td className="p-3">
                    <span className="text-sm font-medium">{model.name}</span>
                    {isBest && (
                      <Badge
                        className="ml-2 text-xs"
                        style={{
                          backgroundColor: "rgba(16,185,129,0.15)",
                          color: "#10b981",
                          border: "1px solid rgba(16,185,129,0.3)",
                        }}
                      >
                        Best
                      </Badge>
                    )}
                  </td>
                  <td className="p-3">
                    <div className="flex items-center gap-2">
                      <div
                        className="w-16 h-2 rounded-full overflow-hidden"
                        style={{ backgroundColor: "#27272a" }}
                      >
                        <div
                          className="h-full rounded-full"
                          style={{
                            width: `${model.overall.accuracy}%`,
                            backgroundColor: isBest ? "#f59e0b" : "#a3a3a3",
                          }}
                        />
                      </div>
                      <span className="text-sm font-mono">
                        {model.overall.accuracy}%
                      </span>
                    </div>
                  </td>
                  <td className="p-3">
                    <span
                      className="text-sm font-mono font-semibold"
                      style={{ color: isBest ? "#10b981" : undefined }}
                    >
                      {model.overall.f1}%
                    </span>
                  </td>
                  <td className="p-3 text-sm font-mono">
                    {model.overall.precision}%
                  </td>
                  <td className="p-3 text-sm font-mono">
                    {model.overall.recall}%
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* SHAP Explainability */}
      {shap && Object.keys(shap).length > 0 && (
        <div className="mb-8">
          <h2 className="text-xl font-semibold tracking-tight mb-4 flex items-center gap-2">
            <BarChart3 className="h-5 w-5" style={{ color: "#8b5cf6" }} />
            SHAP Feature Importance
          </h2>
          <p className="text-sm text-muted-foreground mb-4">
            Shows which patient features most influence the S/R prediction for each drug.
            Computed on the best model ({data[bestKey]?.name}).
          </p>

          {/* Drug selector */}
          <div className="flex flex-wrap gap-2 mb-4">
            {Object.keys(shap).map((drug) => (
              <button
                key={drug}
                onClick={() => setSelectedDrug(drug)}
                className={`text-xs px-3 py-1.5 rounded-full border transition-colors cursor-pointer ${
                  selectedDrug === drug
                    ? "bg-purple-500/20 border-purple-500/50 text-purple-400"
                    : "bg-zinc-800 border-zinc-700 text-zinc-400 hover:border-zinc-500"
                }`}
              >
                {drugNames[drug] || drug}
              </button>
            ))}
          </div>

          {/* SHAP bars */}
          {selectedDrug && shap[selectedDrug] && (
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm text-muted-foreground">
                  Top features for: {drugNames[selectedDrug] || selectedDrug}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {shap[selectedDrug].map((item, idx) => {
                  const maxImp = shap[selectedDrug][0].importance;
                  const barWidth = maxImp > 0 ? (item.importance / maxImp) * 100 : 0;

                  return (
                    <div key={idx} className="flex items-center gap-3">
                      <span className="text-xs text-muted-foreground w-40 truncate text-right">
                        {item.feature}
                      </span>
                      <div
                        className="flex-1 h-3 rounded-full overflow-hidden"
                        style={{ backgroundColor: "#27272a" }}
                      >
                        <div
                          className="h-full rounded-full"
                          style={{
                            width: `${barWidth}%`,
                            backgroundColor: "#8b5cf6",
                          }}
                        />
                      </div>
                      <span className="text-xs font-mono w-14 text-right">
                        {item.importance.toFixed(4)}
                      </span>
                    </div>
                  );
                })}
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Legend */}
      <div
        className="rounded-lg border border-zinc-700 p-4"
        style={{ backgroundColor: "rgba(39,39,42,0.3)" }}
      >
        <h3 className="text-sm font-medium mb-2">What the metrics mean:</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs text-muted-foreground">
          <p>
            <strong>Accuracy</strong> — Overall correct predictions across all
            drugs
          </p>
          <p>
            <strong>F1 Score</strong> — Balance of precision and recall (main
            ranking metric)
          </p>
          <p>
            <strong>Precision</strong> — Of predicted Resistant, how many truly
            are
          </p>
          <p>
            <strong>Recall</strong> — Of actual Resistant, how many we caught
          </p>
          <p>
            <strong>SHAP</strong> — Shows which features push the model toward
            S or R for each drug
          </p>
        </div>
      </div>
    </div>
  );
}
