"use client";

import { XCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DrugResult } from "@/lib/types";

interface AvoidCardProps {
  drugs: DrugResult[];
}

export function AvoidCard({ drugs }: AvoidCardProps) {
  return (
    <Card className="border-l-4 border-l-red-500">
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center gap-2 text-red-500 text-sm">
          <XCircle className="h-4 w-4" />
          Avoid
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-1">
          {drugs.map((d) => (
            <li key={d.drug_code} className="text-sm text-muted-foreground">
              {d.drug_name} ({d.confidence}%)
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}
