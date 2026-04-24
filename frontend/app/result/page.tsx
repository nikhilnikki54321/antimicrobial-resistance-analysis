"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { Suspense } from "react";
import { motion } from "framer-motion";
import { ArrowLeft, Download, Save } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { BestDrugCard } from "@/components/result/best-drug-card";
import { AvoidCard } from "@/components/result/avoid-card";
import { ResultsTable } from "@/components/result/results-table";
import { ResistanceChart } from "@/components/result/resistance-chart";
import { ClinicalSummary } from "@/components/result/clinical-summary";
import { saveHistory } from "@/lib/api";
import { PredictInput, PredictResponse } from "@/lib/types";

function buildPDFHTML(input: PredictInput, result: PredictResponse, microbeName: string): string {
  const gender = input.gender === 1 ? "Male" : "Female";
  const conditions: string[] = [];
  if (input.hypertension) conditions.push("Hypertensive");
  if (input.diabetes) conditions.push("Diabetic");
  if (input.hospital_before) conditions.push("Prior Hospitalization");

  const now = new Date().toLocaleString();

  const allRows = result.all_drugs
    .map((d) => {
      const color = d.result === "S" ? "#10b981" : "#ef4444";
      const label = d.result === "S" ? "Susceptible" : "Resistant";
      return [
        "<tr>",
        `<td style="padding:6px 12px;border-bottom:1px solid #e5e7eb">${d.drug_name}</td>`,
        `<td style="padding:6px 12px;border-bottom:1px solid #e5e7eb;color:${color};font-weight:600">${label}</td>`,
        `<td style="padding:6px 12px;border-bottom:1px solid #e5e7eb">${d.confidence}%</td>`,
        "</tr>",
      ].join("");
    })
    .join("");

  const parts: string[] = [];

  parts.push("<!DOCTYPE html><html><head>");
  parts.push(`<title>AMR Report - ${microbeName || "Unknown"}</title>`);
  parts.push("<style>");
  parts.push("* { margin:0; padding:0; box-sizing:border-box; }");
  parts.push("body { font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; color:#111; padding:40px; max-width:800px; margin:0 auto; }");
  parts.push("h1 { font-size:24px; margin-bottom:4px; }");
  parts.push("h2 { font-size:18px; margin:24px 0 12px; border-bottom:2px solid #111; padding-bottom:4px; }");
  parts.push(".subtitle { color:#666; font-size:13px; margin-bottom:20px; }");
  parts.push(".info { background:#f9fafb; border:1px solid #e5e7eb; border-radius:8px; padding:16px; margin-bottom:20px; }");
  parts.push(".info span { display:inline-block; background:#e5e7eb; border-radius:4px; padding:2px 8px; margin:2px 4px 2px 0; font-size:13px; }");
  parts.push(".best { background:#fef3c7; border:1px solid #f59e0b; border-radius:8px; padding:16px; margin-bottom:16px; }");
  parts.push(".avoid { background:#fef2f2; border:1px solid #ef4444; border-radius:8px; padding:16px; margin-bottom:16px; }");
  parts.push("table { width:100%; border-collapse:collapse; margin:12px 0; }");
  parts.push("th { text-align:left; padding:8px 12px; background:#f3f4f6; border-bottom:2px solid #d1d5db; font-size:13px; }");
  parts.push("td { font-size:13px; }");
  parts.push(".footer { margin-top:32px; padding-top:16px; border-top:1px solid #e5e7eb; font-size:11px; color:#999; text-align:center; }");
  parts.push("@media print { body { padding:20px; } }");
  parts.push("</style></head><body>");

  parts.push(`<h1>AMR Resistance Report</h1>`);
  parts.push(`<p class="subtitle">Generated: ${now} | Microbe: ${microbeName || "Not specified"}</p>`);

  parts.push(`<div class="info"><h3 style="font-size:14px;margin-bottom:8px">Patient Information</h3>`);
  parts.push(`<span>Age: ${input.age}</span><span>Gender: ${gender}</span><span>Infections: ${input.infection_freq}</span>`);
  if (input.hypertension) parts.push(`<span style="background:#fee2e2;color:#dc2626">Hypertension</span>`);
  if (input.diabetes) parts.push(`<span style="background:#fee2e2;color:#dc2626">Diabetes</span>`);
  if (input.hospital_before) parts.push(`<span>Prior Hospitalization</span>`);
  parts.push(`<br/><span>Microbe: ${microbeName || "Not specified"}</span></div>`);

  if (result.best_drug) {
    parts.push(`<div class="best"><strong style="color:#b45309">★ Best Drug: ${result.best_drug.drug_name}</strong>`);
    parts.push(`<br/>Confidence: ${result.best_drug.confidence}%`);
    if (result.sensitive.length > 1) {
      parts.push(`<br/>Also consider: ${result.sensitive.slice(1, 3).map((d) => d.drug_name).join(", ")}`);
    }
    parts.push(`</div>`);
  }

  if (result.resistant.length > 0) {
    parts.push(`<div class="avoid"><strong style="color:#dc2626">✗ Avoid (Resistant):</strong>`);
    parts.push(`<br/>${result.resistant.map((d) => `${d.drug_name} (${d.confidence}%)`).join(", ")}</div>`);
  }

  parts.push(`<h2>Full Drug Screening Results</h2>`);
  parts.push(`<table><thead><tr><th>Drug</th><th>Result</th><th>Confidence</th></tr></thead>`);
  parts.push(`<tbody>${allRows}</tbody></table>`);

  parts.push(`<h2>Clinical Recommendation</h2>`);
  parts.push(`<p style="font-size:14px;line-height:1.6">`);
  parts.push(`Patient (${gender}, ${input.age}${conditions.length > 0 ? ", " + conditions.join(", ") : ""})`);
  if (microbeName) parts.push(` infected with <strong>${microbeName}</strong>.`);
  if (result.best_drug) parts.push(`<br/>Recommend: <strong>${result.best_drug.drug_name}</strong>.`);
  if (result.resistant.length > 0) parts.push(`<br/>Avoid: ${result.resistant.slice(0, 3).map((d) => d.drug_name).join(", ")}.`);
  parts.push(`</p>`);

  parts.push(`<div class="footer">AMR Prediction System | ML-Powered Antibiotic Resistance Report</div>`);
  parts.push("</body></html>");

  return parts.join("\n");
}

function handleDownloadPDF(input: PredictInput, result: PredictResponse, microbeName: string) {
  const html = buildPDFHTML(input, result, microbeName);
  const blob = new Blob([html], { type: "text/html" });
  const url = URL.createObjectURL(blob);

  const printWindow = window.open(url, "_blank");
  if (printWindow) {
    printWindow.addEventListener("load", () => {
      printWindow.focus();
      printWindow.print();
    });
  }

  // Cleanup after a delay
  setTimeout(() => URL.revokeObjectURL(url), 10000);
}

function ResultContent() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const raw = searchParams.get("data");
  if (!raw) {
    return (
      <div className="text-center py-20 text-muted-foreground">
        No prediction data.{" "}
        <button onClick={() => router.push("/predict")} className="underline text-primary">
          Start a prediction
        </button>
      </div>
    );
  }

  let input: PredictInput;
  let result: PredictResponse;
  let microbeName = "";
  try {
    const parsed = JSON.parse(raw);
    input = parsed.input;
    result = parsed.result;
    microbeName = parsed.microbeName || "";
  } catch {
    return <div className="text-center py-20 text-muted-foreground">Invalid data.</div>;
  }

  const gender = input.gender === 1 ? "Male" : "Female";

  const handleSave = async () => {
    try {
      await saveHistory(input, result);
      alert("Saved to history!");
    } catch {
      alert("Failed to save.");
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-6"
    >
      {/* Patient summary */}
      <Card className="bg-muted/50">
        <CardContent className="flex flex-wrap gap-2 py-4">
          <Badge variant="secondary">Age: {input.age}</Badge>
          <Badge variant="secondary">{gender}</Badge>
          {input.hypertension === 1 && (
            <Badge variant="secondary" className="bg-red-500/10 text-red-500 border-red-500/20">
              Hypertension
            </Badge>
          )}
          {input.diabetes === 1 && (
            <Badge variant="secondary" className="bg-red-500/10 text-red-500 border-red-500/20">
              Diabetes
            </Badge>
          )}
          {input.hospital_before === 1 && (
            <Badge variant="secondary">Prior Hospital</Badge>
          )}
          <Badge variant="secondary">
            Infections: {input.infection_freq}
          </Badge>
          {microbeName && (
            <Badge variant="secondary" className="bg-blue-500/10 text-blue-400 border-blue-500/20">
              {microbeName}
            </Badge>
          )}
        </CardContent>
      </Card>

      {/* Best Drug + Avoid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {result.best_drug && (
          <BestDrugCard
            bestDrug={result.best_drug}
            alsoConsider={result.sensitive.slice(1, 3)}
          />
        )}
        {result.resistant.length > 0 && (
          <AvoidCard drugs={result.resistant} />
        )}
      </div>

      {/* Full results table */}
      <ResultsTable drugs={result.all_drugs} />

      {/* Chart */}
      <ResistanceChart drugs={result.all_drugs} />

      {/* Clinical summary */}
      <ClinicalSummary input={input} result={result} />

      {/* Actions */}
      <div className="flex flex-wrap gap-3 pt-4">
        <button
          onClick={() => router.push("/predict")}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-md border border-zinc-600 bg-zinc-800 text-sm font-medium text-zinc-200 hover:bg-zinc-700 transition-colors cursor-pointer"
        >
          <ArrowLeft className="h-4 w-4" />
          New Prediction
        </button>
        <button
          onClick={() => handleDownloadPDF(input, result, microbeName)}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-md border border-zinc-600 bg-zinc-800 text-sm font-medium text-zinc-200 hover:bg-zinc-700 transition-colors cursor-pointer"
        >
          <Download className="h-4 w-4" />
          Download PDF
        </button>
        <button
          onClick={handleSave}
          className="inline-flex items-center gap-2 px-6 py-2.5 rounded-md bg-emerald-600 text-sm font-medium text-white hover:bg-emerald-500 transition-colors cursor-pointer"
        >
          <Save className="h-4 w-4" />
          Save to History
        </button>
      </div>
    </motion.div>
  );
}

export default function ResultPage() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-semibold tracking-tight mb-6">
        Full AMR Report
      </h1>
      <Suspense fallback={<div>Loading...</div>}>
        <ResultContent />
      </Suspense>
    </div>
  );
}
