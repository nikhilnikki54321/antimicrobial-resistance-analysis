"use client";

import { FileText } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { PredictInput, PredictResponse } from "@/lib/types";

interface ClinicalSummaryProps {
  input: PredictInput;
  result: PredictResponse;
}

export function ClinicalSummary({ input, result }: ClinicalSummaryProps) {
  const gender = input.gender === 1 ? "Male" : "Female";
  const conditions = [];
  if (input.hypertension) conditions.push("Hypertensive");
  if (input.diabetes) conditions.push("Diabetic");
  if (input.hospital_before) conditions.push("Prior hospitalization");
  const condStr = conditions.length > 0 ? conditions.join(", ") : "No comorbidities";

  const sensitiveNames = result.sensitive
    .slice(0, 3)
    .map((d) => `${d.drug_name} (${d.confidence}%)`)
    .join(", ");

  const resistantNames = result.resistant
    .slice(0, 3)
    .map((d) => `${d.drug_name} (${d.confidence}%)`)
    .join(", ");

  return (
    <Alert>
      <FileText className="h-4 w-4" />
      <AlertTitle>Clinical Recommendation</AlertTitle>
      <AlertDescription className="mt-2 space-y-2 text-sm">
        <p>
          Patient ({gender}, {input.age}, {condStr}).
        </p>
        {result.sensitive.length > 0 && (
          <p>
            <strong className="text-emerald-500">Susceptible:</strong>{" "}
            {sensitiveNames}
          </p>
        )}
        {result.resistant.length > 0 && (
          <p>
            <strong className="text-red-500">Resistant:</strong>{" "}
            {resistantNames}
          </p>
        )}
        {result.best_drug && (
          <p>
            <strong className="text-amber-400">Recommendation:</strong>{" "}
            {result.best_drug.drug_name}
          </p>
        )}
      </AlertDescription>
    </Alert>
  );
}
