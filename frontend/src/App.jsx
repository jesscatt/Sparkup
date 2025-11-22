import { useState } from "react";
import Step1 from "./components/Step1";
import Step2 from "./components/Step2";
import Step3 from "./components/Step3";
import Step4 from "./components/Step4";
import Result from "./components/Result";

export default function App() {
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({});

  return (
    <div className="app-container">
      {step === 1 && <Step1 setStep={setStep} setForm={setForm} form={form} />}
      {step === 2 && <Step2 setStep={setStep} setForm={setForm} form={form} />}
      {step === 3 && <Step3 setStep={setStep} setForm={setForm} form={form} />}
      {step === 4 && <Step4 setStep={setStep} setForm={setForm} form={form} />}
      {step === 5 && <Result form={form} />}
    </div>
  );
}
