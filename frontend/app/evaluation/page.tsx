"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { getModelComparison } from "@/lib/api";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { FileSpreadsheet } from "lucide-react";

interface ModelMetrics {
  accuracy: number;
  f1: number;
  precision: number;
  recall: number;
}

interface ModelData {
  name: string;
  per_drug: Record<string, ModelMetrics>;
}

export default function EvaluationPage() {
  const [data, setData] = useState<Record<string, ModelData> | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeModel, setActiveModel] = useState<string>("");

  useEffect(() => {
    getModelComparison()
      .then((raw: Record<string, unknown>) => {
        const models: Record<string, ModelData> = {};
        for (const [k, v] of Object.entries(raw)) {
          if (k.startsWith("_")) continue;
          models[k] = v as ModelData;
        }
        setData(models);
        if (Object.keys(models).length > 0) {
          setActiveModel(Object.keys(models)[0]);
        }
      })
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-8 space-y-4">
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-10 w-full" />
        <Skeleton className="h-[400px] w-full rounded-xl" />
      </div>
    );
  }

  if (!data || Object.keys(data).length === 0) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-8 text-center text-muted-foreground">
        No evaluation data available. Please train your models first.
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-semibold tracking-tight mb-2 flex items-center gap-2">
        <FileSpreadsheet className="h-8 w-8 text-emerald-500" />
        Detailed Evaluation Matrices
      </h1>
      <p className="text-muted-foreground mb-8">
        Examine the per-drug evaluation matrices for all tested models. Provides a deep dive into Accuracy, F1-Score, Precision, and Recall for each antibiotic.
      </p>

      <Tabs value={activeModel} onValueChange={setActiveModel} className="w-full">
        <div className="border-b border-border/50 mb-6 overflow-x-auto pb-2 scrollbar-hide">
          <TabsList className="inline-flex h-10 items-center justify-center rounded-md bg-zinc-900 p-1 text-muted-foreground flex-nowrap shrink-0">
            {Object.entries(data).map(([k, m]) => (
              <TabsTrigger key={k} value={k} className="whitespace-nowrap px-4 py-1.5 text-sm font-medium transition-all data-[state=active]:bg-zinc-800 data-[state=active]:text-emerald-400 data-[state=active]:shadow-sm">
                {m.name}
              </TabsTrigger>
            ))}
          </TabsList>
        </div>

        {Object.entries(data).map(([k, model]) => (
          <TabsContent key={k} value={k} className="mt-0 outline-none">
            <Card className="border-zinc-800 bg-zinc-950/50 shadow-lg">
              <CardHeader>
                <CardTitle className="text-xl">{model.name} — Class-wise Metrics</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="rounded-md border border-zinc-800 bg-zinc-900/20">
                  <Table>
                    <TableHeader>
                      <TableRow className="border-zinc-800 hover:bg-transparent">
                        <TableHead className="w-[300px] font-semibold text-zinc-300">Drug Name</TableHead>
                        <TableHead className="text-right font-semibold text-zinc-300">Accuracy (%)</TableHead>
                        <TableHead className="text-right text-emerald-500 font-bold">F1 Score (%)</TableHead>
                        <TableHead className="text-right font-semibold text-zinc-300">Precision (%)</TableHead>
                        <TableHead className="text-right font-semibold text-zinc-300">Recall (%)</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {Object.entries(model.per_drug).map(([drug, metrics]) => (
                        <TableRow key={drug} className="border-zinc-800/50 hover:bg-zinc-800/50 font-mono transition-colors">
                          <TableCell className="font-sans font-medium text-zinc-400">
                            {drug}
                          </TableCell>
                          <TableCell className="text-right text-zinc-500">
                            {metrics.accuracy.toFixed(2)}
                          </TableCell>
                          <TableCell className="text-right font-bold text-emerald-400">
                            {metrics.f1.toFixed(2)}
                          </TableCell>
                          <TableCell className="text-right text-zinc-500">
                            {metrics.precision.toFixed(2)}
                          </TableCell>
                          <TableCell className="text-right text-zinc-500">
                            {metrics.recall.toFixed(2)}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        ))}
      </Tabs>
    </div>
  );
}
