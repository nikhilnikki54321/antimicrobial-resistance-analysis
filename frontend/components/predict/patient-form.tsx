"use client";

import { useState } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { ArrowRight } from "lucide-react";

interface PatientFormProps {
  data: {
    age: number;
    gender: number;
    diabetes: number;
    hypertension: number;
    hospital_before: number;
    infection_freq: number;
  };
  onChange: (data: PatientFormProps["data"]) => void;
  onNext: () => void;
}

export function PatientForm({ data, onChange, onNext }: PatientFormProps) {
  const [errors, setErrors] = useState<Record<string, string>>({});

  const update = (field: string, value: number) => {
    onChange({ ...data, [field]: value });
    // Clear error for this field when user changes it
    if (errors[field]) {
      setErrors((prev) => {
        const next = { ...prev };
        delete next[field];
        return next;
      });
    }
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!data.age || data.age <= 0 || data.age > 120) {
      newErrors.age = "Age is required (1-120)";
    }

    if (data.gender !== 0 && data.gender !== 1) {
      newErrors.gender = "Please select gender";
    }

    if (data.infection_freq < 0) {
      newErrors.infection_freq = "Must be 0 or more";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleNext = () => {
    if (validate()) {
      onNext();
    }
  };

  return (
    <Card className="max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Patient Information</CardTitle>
        <CardDescription>Enter the patient&apos;s clinical details. Fields marked * are required.</CardDescription>
      </CardHeader>

      <CardContent className="space-y-6">
        <div className="space-y-2">
          <Label htmlFor="age">Age *</Label>
          <Input
            id="age"
            type="number"
            min={1}
            max={120}
            value={data.age || ""}
            onChange={(e) => update("age", Number(e.target.value))}
            placeholder="Enter patient age"
            className={errors.age ? "border-red-500" : ""}
          />
          {errors.age && <p className="text-xs text-red-500">{errors.age}</p>}
        </div>

        <div className="space-y-2">
          <Label>Gender *</Label>
          <RadioGroup
            value={data.gender >= 0 ? String(data.gender) : undefined}
            onValueChange={(v) => update("gender", Number(v))}
            className="flex gap-4"
          >
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="1" id="male" />
              <Label htmlFor="male">Male</Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="0" id="female" />
              <Label htmlFor="female">Female</Label>
            </div>
          </RadioGroup>
          {errors.gender && <p className="text-xs text-red-500">{errors.gender}</p>}
        </div>

        <div className="flex items-center justify-between">
          <Label htmlFor="hypertension">Hypertension</Label>
          <Switch
            id="hypertension"
            checked={data.hypertension === 1}
            onCheckedChange={(v) => update("hypertension", v ? 1 : 0)}
          />
        </div>

        <div className="flex items-center justify-between">
          <Label htmlFor="diabetes">Diabetes</Label>
          <Switch
            id="diabetes"
            checked={data.diabetes === 1}
            onCheckedChange={(v) => update("diabetes", v ? 1 : 0)}
          />
        </div>

        <div className="flex items-center justify-between">
          <Label htmlFor="hospital">Previous Hospitalization</Label>
          <Switch
            id="hospital"
            checked={data.hospital_before === 1}
            onCheckedChange={(v) => update("hospital_before", v ? 1 : 0)}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="infection_freq">Infection Frequency</Label>
          <Input
            id="infection_freq"
            type="number"
            min={0}
            step={1}
            value={data.infection_freq || ""}
            onChange={(e) => update("infection_freq", Number(e.target.value))}
            placeholder="How many times infected before"
            className={errors.infection_freq ? "border-red-500" : ""}
          />
          {errors.infection_freq && <p className="text-xs text-red-500">{errors.infection_freq}</p>}
        </div>
      </CardContent>

      <CardFooter className="flex justify-end">
        <button
          onClick={handleNext}
          className="inline-flex items-center gap-2 px-6 py-2.5 rounded-md bg-white text-sm font-medium text-black hover:bg-zinc-200 transition-colors cursor-pointer"
        >
          Continue
          <ArrowRight className="h-4 w-4" />
        </button>
      </CardFooter>
    </Card>
  );
}
