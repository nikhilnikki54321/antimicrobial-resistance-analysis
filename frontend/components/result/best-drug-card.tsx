"use client";

import { Star } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DrugResult } from "@/lib/types";

interface BestDrugCardProps {
  bestDrug: DrugResult;
  alsoConsider: DrugResult[];
}

export function BestDrugCard({ bestDrug, alsoConsider }: BestDrugCardProps) {
  return (
    <Card className="border-l-4 border-l-amber-400">
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center gap-2 text-amber-400 text-sm">
          <Star className="h-4 w-4 fill-amber-400" />
          Best Drug
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-2xl font-bold">{bestDrug.drug_name}</p>
        <p className="text-sm text-muted-foreground">
          {bestDrug.confidence}% confidence
        </p>
        {alsoConsider.length > 0 && (
          <p className="text-sm text-muted-foreground mt-2">
            Also consider:{" "}
            {alsoConsider.map((d) => `${d.drug_name} (${d.confidence}%)`).join(", ")}
          </p>
        )}
      </CardContent>
    </Card>
  );
}
