"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DrugResult } from "@/lib/types";

interface ResistanceChartProps {
  drugs: DrugResult[];
}

export function ResistanceChart({ drugs }: ResistanceChartProps) {
  const sorted = [...drugs].sort((a, b) => {
    if (a.result === "S" && b.result === "R") return -1;
    if (a.result === "R" && b.result === "S") return 1;
    return a.confidence - b.confidence;
  });

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Resistance Profile</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {sorted.map((drug) => {
          const isResistant = drug.result === "R";
          const barWidth = drug.confidence;
          const barColor = isResistant ? "#ef4444" : "#10b981";
          const label = isResistant ? "Resistant" : "Susceptible";

          return (
            <div key={drug.drug_code} className="flex items-center gap-3">
              <span className="text-xs text-muted-foreground w-36 truncate text-right">
                {drug.drug_name}
              </span>
              <div className="flex-1 h-4 rounded-full overflow-hidden" style={{ backgroundColor: "#27272a" }}>
                <div
                  className="h-full rounded-full transition-all"
                  style={{
                    width: `${barWidth}%`,
                    backgroundColor: barColor,
                  }}
                />
              </div>
              <span className="text-xs font-mono w-20 text-right">
                {barWidth}%{" "}
                <span style={{ color: barColor }}>
                  ({drug.result})
                </span>
              </span>
            </div>
          );
        })}

        <div className="flex justify-between text-xs text-muted-foreground pt-2 border-t border-zinc-800 mt-2">
          <span className="flex items-center gap-1.5">
            <span className="inline-block w-3 h-3 rounded-full" style={{ backgroundColor: "#10b981" }} />
            Susceptible
          </span>
          <span className="flex items-center gap-1.5">
            <span className="inline-block w-3 h-3 rounded-full" style={{ backgroundColor: "#ef4444" }} />
            Resistant
          </span>
        </div>
      </CardContent>
    </Card>
  );
}
