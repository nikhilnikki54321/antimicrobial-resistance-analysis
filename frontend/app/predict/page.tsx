"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { StepIndicator } from "@/components/predict/step-indicator";
import { PatientForm } from "@/components/predict/patient-form";
import { MicrobeForm } from "@/components/predict/microbe-form";
import { Skeleton } from "@/components/ui/skeleton";
import { Progress } from "@/components/ui/progress";
import { predictAMR } from "@/lib/api";
import { PredictInput } from "@/lib/types";

export default function PredictPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [microbeName, setMicrobeName] = useState("");

  const [formData, setFormData] = useState<PredictInput>({
    age: 0,
    gender: -1,
    diabetes: 0,
    hypertension: 0,
    hospital_before: 0,
    infection_freq: 0,
  });

  const handleSubmit = async () => {
    setLoading(true);
    setStep(3);
    setLoadingProgress(30);

    try {
      const progressInterval = setInterval(() => {
        setLoadingProgress((prev) => Math.min(prev + 10, 90));
      }, 200);

      const result = await predictAMR({ ...formData, microbe_name: microbeName });

      clearInterval(progressInterval);
      setLoadingProgress(100);

      const params = new URLSearchParams({
        data: JSON.stringify({ input: formData, result, microbeName }),
      });
      router.push(`/result?${params.toString()}`);
    } catch (err) {
      console.error("Prediction failed:", err);
      setLoading(false);
      setStep(2);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <StepIndicator currentStep={step} />

      <AnimatePresence mode="wait">
        {step === 1 && (
          <motion.div
            key="step1"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.2 }}
          >
            <PatientForm
              data={formData}
              onChange={setFormData}
              onNext={() => setStep(2)}
            />
          </motion.div>
        )}

        {step === 2 && (
          <motion.div
            key="step2"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.2 }}
          >
            <MicrobeForm
              microbeName={microbeName}
              onMicrobeChange={setMicrobeName}
              onBack={() => setStep(1)}
              onSubmit={handleSubmit}
              loading={loading}
            />
          </motion.div>
        )}

        {step === 3 && loading && (
          <motion.div
            key="loading"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="max-w-2xl mx-auto space-y-6"
          >
            <div className="text-center space-y-2">
              <p className="text-lg font-medium">Analyzing Resistance Patterns...</p>
              <p className="text-sm text-muted-foreground">
                Screening {microbeName || "microbe"} against all 15 antibiotics
              </p>
            </div>
            <Progress value={loadingProgress} className="h-2" />
            <div className="space-y-3">
              <Skeleton className="h-24 w-full rounded-xl" />
              <div className="grid grid-cols-2 gap-3">
                <Skeleton className="h-32 rounded-xl" />
                <Skeleton className="h-32 rounded-xl" />
              </div>
              <Skeleton className="h-48 w-full rounded-xl" />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
