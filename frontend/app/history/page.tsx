"use client";

import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { getHistory } from "@/lib/api";
import { HistoryRecord } from "@/lib/types";

export default function HistoryPage() {
  const [records, setRecords] = useState<HistoryRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getHistory()
      .then(setRecords)
      .catch(() => setRecords([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-semibold tracking-tight mb-2">
        Prediction History
      </h1>
      <p className="text-muted-foreground mb-6">
        Browse past AMR predictions.
      </p>

      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-16 w-full rounded-xl" />
          ))}
        </div>
      ) : records.length === 0 ? (
        <div className="text-center py-20 text-muted-foreground">
          No predictions saved yet. <a href="/predict" className="underline">Start one</a>.
        </div>
      ) : (
        <div className="rounded-xl border border-border overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border bg-muted/50">
                <th className="text-left text-xs font-medium text-muted-foreground p-3">#</th>
                <th className="text-left text-xs font-medium text-muted-foreground p-3">Date</th>
                <th className="text-left text-xs font-medium text-muted-foreground p-3">Patient</th>
                <th className="text-left text-xs font-medium text-muted-foreground p-3">Best Drug</th>
                <th className="text-left text-xs font-medium text-muted-foreground p-3">Drugs</th>
                <th className="text-left text-xs font-medium text-muted-foreground p-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              {records.map((rec, i) => {
                const input = rec.input;
                const bestDrug = rec.result?.best_drug;
                const gender = input?.gender === 1 ? "M" : "F";
                const date = rec.timestamp
                  ? new Date(rec.timestamp).toLocaleDateString()
                  : "—";

                return (
                  <tr
                    key={rec.id || i}
                    className="border-b border-border last:border-0 hover:bg-muted/50 transition-colors"
                  >
                    <td className="p-3 text-sm text-muted-foreground">{i + 1}</td>
                    <td className="p-3 text-sm">{date}</td>
                    <td className="p-3">
                      <div className="flex gap-1.5 flex-wrap">
                        <Badge variant="secondary" className="text-xs">
                          {gender}, {input?.age}
                        </Badge>
                        {input?.hypertension === 1 && (
                          <Badge variant="secondary" className="text-xs bg-red-500/10 text-red-500">
                            HT
                          </Badge>
                        )}
                        {input?.diabetes === 1 && (
                          <Badge variant="secondary" className="text-xs bg-red-500/10 text-red-500">
                            DM
                          </Badge>
                        )}
                      </div>
                    </td>
                    <td className="p-3">
                      {bestDrug && (
                        <Badge className="bg-amber-400/10 text-amber-400 border-amber-400/20">
                          {bestDrug.drug_name}
                        </Badge>
                      )}
                    </td>
                    <td className="p-3 text-sm text-muted-foreground">
                      {rec.result?.all_drugs?.length || 15} screened
                    </td>
                    <td className="p-3">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => {
                          const params = new URLSearchParams({
                            data: JSON.stringify({ input: rec.input, result: rec.result }),
                          });
                          window.location.href = `/result?${params.toString()}`;
                        }}
                      >
                        View
                      </Button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
