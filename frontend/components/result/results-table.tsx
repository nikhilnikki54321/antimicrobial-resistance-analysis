"use client";

import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { DrugResult } from "@/lib/types";

interface ResultsTableProps {
  drugs: DrugResult[];
}

export function ResultsTable({ drugs }: ResultsTableProps) {
  const sorted = [...drugs].sort((a, b) => b.confidence - a.confidence);

  return (
    <div className="rounded-xl border border-border overflow-hidden">
      <table className="w-full">
        <thead>
          <tr className="border-b border-border bg-muted/50">
            <th className="text-left text-xs font-medium text-muted-foreground p-3">
              Drug
            </th>
            <th className="text-left text-xs font-medium text-muted-foreground p-3">
              Result
            </th>
            <th className="text-left text-xs font-medium text-muted-foreground p-3">
              Confidence
            </th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((drug) => (
            <tr
              key={drug.drug_code}
              className="border-b border-border last:border-0 hover:bg-muted/50 transition-colors"
            >
              <td className="p-3">
                <div>
                  <span className="text-sm font-medium">{drug.drug_name}</span>
                  <span className="text-xs text-muted-foreground ml-2">
                    ({drug.drug_code})
                  </span>
                </div>
              </td>
              <td className="p-3">
                <Badge
                  variant="secondary"
                  className={
                    drug.result === "S"
                      ? "bg-emerald-500/10 text-emerald-500 border-emerald-500/20"
                      : "bg-red-500/10 text-red-500 border-red-500/20"
                  }
                >
                  <span className="mr-1.5 text-[8px]">●</span>
                  {drug.result === "S" ? "Susceptible" : "Resistant"}
                </Badge>
              </td>
              <td className="p-3">
                <div className="flex items-center gap-3">
                  <Progress
                    value={drug.confidence}
                    className="h-2 w-24"
                  />
                  <span className="text-sm font-mono text-muted-foreground">
                    {drug.confidence}%
                  </span>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
