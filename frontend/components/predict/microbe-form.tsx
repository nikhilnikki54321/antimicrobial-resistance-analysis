"use client";

import { useState, useEffect, useRef } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ArrowLeft, FileText, Loader2, ChevronDown, Search } from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { getMicrobes } from "@/lib/api";

interface MicrobeFormProps {
  microbeName: string;
  onMicrobeChange: (name: string) => void;
  onBack: () => void;
  onSubmit: () => void;
  loading: boolean;
}

export function MicrobeForm({ microbeName, onMicrobeChange, onBack, onSubmit, loading }: MicrobeFormProps) {
  const [error, setError] = useState("");
  const [microbeList, setMicrobeList] = useState<string[]>([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [search, setSearch] = useState("");
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getMicrobes().then(setMicrobeList);
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setShowDropdown(false);
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const filtered = microbeList.filter((m) =>
    m.toLowerCase().includes(search.toLowerCase())
  );

  const handleSelect = (name: string) => {
    onMicrobeChange(name);
    setSearch("");
    setShowDropdown(false);
    if (error) setError("");
  };

  const handleSubmit = () => {
    if (!microbeName.trim()) {
      setError("Please select a microbe");
      return;
    }
    setError("");
    onSubmit();
  };

  return (
    <Card className="max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Microbe Information</CardTitle>
        <CardDescription>
          Select the microbe identified from the lab culture.
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Searchable dropdown */}
        <div className="space-y-2">
          <Label>Microbe / Bacteria Name *</Label>
          <div className="relative" ref={dropdownRef}>
            {/* Selected value or search input */}
            <div
              onClick={() => setShowDropdown(!showDropdown)}
              className={`flex items-center justify-between h-10 w-full rounded-md border px-3 py-2 text-sm cursor-pointer transition-colors ${
                error
                  ? "border-red-500"
                  : showDropdown
                  ? "border-zinc-400 ring-1 ring-zinc-400"
                  : "border-zinc-600 hover:border-zinc-400"
              } bg-transparent`}
            >
              <span className={microbeName ? "text-foreground" : "text-muted-foreground"}>
                {microbeName || "Select a microbe..."}
              </span>
              <ChevronDown className={`h-4 w-4 text-muted-foreground transition-transform ${showDropdown ? "rotate-180" : ""}`} />
            </div>

            {/* Dropdown */}
            {showDropdown && (
              <div className="absolute z-50 mt-1 w-full rounded-md border border-zinc-600 bg-zinc-900 shadow-lg">
                {/* Search inside dropdown */}
                <div className="flex items-center gap-2 px-3 py-2 border-b border-zinc-700">
                  <Search className="h-4 w-4 text-muted-foreground" />
                  <input
                    type="text"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    placeholder="Search microbe..."
                    className="w-full bg-transparent text-sm outline-none placeholder:text-muted-foreground"
                    autoFocus
                  />
                </div>

                {/* Options */}
                <div className="max-h-48 overflow-y-auto">
                  {filtered.length === 0 ? (
                    <div className="px-3 py-3 text-sm text-muted-foreground text-center">
                      No microbes found
                    </div>
                  ) : (
                    filtered.map((m) => (
                      <div
                        key={m}
                        onClick={() => handleSelect(m)}
                        className={`px-3 py-2.5 text-sm cursor-pointer transition-colors hover:bg-zinc-800 ${
                          microbeName === m ? "bg-zinc-800 text-emerald-400 font-medium" : "text-zinc-200"
                        }`}
                      >
                        {m}
                      </div>
                    ))
                  )}
                </div>
              </div>
            )}
          </div>
          {error && <p className="text-xs text-red-500">{error}</p>}
        </div>

        <Alert>
          <FileText className="h-4 w-4" />
          <AlertDescription>
            The system will automatically test{" "}
            {microbeName ? <strong>{microbeName}</strong> : "the selected microbe"}{" "}
            against <strong>all 15 antibiotics</strong> and generate a complete
            resistance report.
          </AlertDescription>
        </Alert>

        <div className="rounded-lg border border-zinc-700 p-4 bg-zinc-800/50">
          <h4 className="text-sm font-medium mb-3">15 Drugs to be screened:</h4>
          <div className="flex flex-wrap gap-2">
            {[
              "Amoxicillin/Ampicillin", "Amoxicillin-Clavulanate", "Cefazolin",
              "Cefoxitin", "Cefotaxime/Ceftriaxone", "Imipenem", "Gentamicin",
              "Amikacin", "Nalidixic Acid", "Ofloxacin", "Ciprofloxacin",
              "Chloramphenicol", "Co-trimoxazole", "Nitrofurantoin", "Colistin"
            ].map((drug) => (
              <span
                key={drug}
                className="text-xs px-2.5 py-1 rounded-full bg-zinc-900 border border-zinc-600 text-zinc-300"
              >
                {drug}
              </span>
            ))}
          </div>
        </div>
      </CardContent>

      <CardFooter className="flex justify-between">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-md border border-zinc-600 bg-zinc-800 text-sm font-medium text-zinc-200 hover:bg-zinc-700 transition-colors cursor-pointer"
        >
          <ArrowLeft className="h-4 w-4" />
          Back
        </button>
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="inline-flex items-center gap-2 px-6 py-2.5 rounded-md bg-emerald-600 text-sm font-medium text-white hover:bg-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors cursor-pointer"
        >
          {loading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Analyzing...
            </>
          ) : (
            <>
              <FileText className="h-4 w-4" />
              Generate Full AMR Report
            </>
          )}
        </button>
      </CardFooter>
    </Card>
  );
}
