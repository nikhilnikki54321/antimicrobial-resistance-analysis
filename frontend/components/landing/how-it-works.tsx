"use client";

import { motion } from "framer-motion";
import { User, Bug, FileText } from "lucide-react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";

const steps = [
  {
    number: "01",
    icon: User,
    title: "Patient Info",
    description:
      "Enter age, gender, hypertension, diabetes, and hospital history. These clinical factors affect resistance patterns.",
  },
  {
    number: "02",
    icon: Bug,
    title: "Microbe Data",
    description:
      "Select the microbe type and enter genomic or lab features like MIC values, zone diameters, and gene markers.",
  },
  {
    number: "03",
    icon: FileText,
    title: "Full AMR Report",
    description:
      "Auto-generated S/R prediction for ALL 15 drugs. Includes best drug recommendation, avoid list, and clinical summary.",
  },
];

export function HowItWorks() {
  return (
    <section className="py-16 px-4">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-2xl font-semibold tracking-tight mb-8 text-center">
          How It Works
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {steps.map((step, i) => (
            <motion.div
              key={step.number}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: i * 0.1 }}
            >
              <Card className="h-full hover:border-ring/50 transition-all">
                <CardHeader>
                  <span className="text-4xl font-bold text-muted-foreground/30">
                    {step.number}
                  </span>
                  <step.icon className="h-6 w-6 text-emerald-500 mt-2" />
                </CardHeader>
                <CardContent>
                  <h3 className="font-medium text-lg mb-2">{step.title}</h3>
                  <p className="text-sm text-muted-foreground">
                    {step.description}
                  </p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
