"use client";

import { cn } from "@/lib/utils";

interface StepIndicatorProps {
  currentStep: number;
}

const steps = [
  { number: 1, label: "Patient Info" },
  { number: 2, label: "Microbe Data" },
  { number: 3, label: "AMR Report" },
];

export function StepIndicator({ currentStep }: StepIndicatorProps) {
  return (
    <div className="flex items-center justify-center mb-8">
      {steps.map((step, i) => (
        <div key={step.number} className="flex items-center">
          {/* Step circle + label */}
          <div className="flex flex-col items-center">
            <div
              className={cn(
                "w-9 h-9 rounded-full flex items-center justify-center text-sm font-semibold transition-colors border-2",
                currentStep > step.number
                  ? "bg-emerald-500 border-emerald-500 text-white"
                  : currentStep === step.number
                  ? "bg-primary border-primary text-primary-foreground"
                  : "bg-zinc-800 border-zinc-600 text-zinc-400"
              )}
            >
              {currentStep > step.number ? "✓" : step.number}
            </div>
            <span
              className={cn(
                "text-xs mt-2 font-medium",
                currentStep >= step.number
                  ? "text-foreground"
                  : "text-muted-foreground"
              )}
            >
              {step.label}
            </span>
          </div>

          {/* Connecting line */}
          {i < steps.length - 1 && (
            <div
              className={cn(
                "w-20 md:w-32 h-[2px] mx-3 mb-6",
                currentStep > step.number ? "bg-emerald-500" : "bg-zinc-700"
              )}
            />
          )}
        </div>
      ))}
    </div>
  );
}
