import { useState } from "react";

export default function App() {
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({
    businessName: "",
    audience: "",
    color: "",
    tone: "",
  });
  const [result, setResult] = useState("");

  const next = () => setStep(step + 1);
  const back = () => setStep(step - 1);

  const generate = async () => {
    const res = await fetch("http://localhost:4000/brand", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    const data = await res.json();
    setResult(data.result);
    next();
  };

  return (
    <div style={{ padding: 20, maxWidth: 600, margin: "auto" }}>

      <h1>Sparkup 🔥</h1>

      {/* PASSO 1 */}
      {step === 1 && (
        <>
          <p>Nome da empresa:</p>
          <input
            value={form.businessName}
            onChange={(e) => setForm({ ...form, businessName: e.target.value })}
          />
          <br /><br />
          <button onClick={next}>Continuar</button>
        </>
      )}

      {/* PASSO 2 */}
      {step === 2 && (
        <>
          <p>Público alvo:</p>
          <input
            value={form.audience}
            onChange={(e) => setForm({ ...form, audience: e.target.value })}
          />
          <br /><br />
          <button onClick={back}>Voltar</button>
          <button onClick={next}>Continuar</button>
        </>
      )}

      {/* PASSO 3 */}
      {step === 3 && (
        <>
          <p>Cor principal da marca:</p>
          <input
            value={form.color}
            onChange={(e) => setForm({ ...form, color: e.target.value })}
          />
          <br /><br />
          <button onClick={back}>Voltar</button>
          <button onClick={next}>Continuar</button>
        </>
      )}

      {/* PASSO 4 */}
      {step === 4 && (
        <>
          <p>Tom da comunicação (ex: divertido, formal, etc):</p>
          <input
            value={form.tone}
            onChange={(e) => setForm({ ...form, tone: e.target.value })}
          />
          <br /><br />
          <button onClick={back}>Voltar</button>
          <button onClick={generate}>Gerar marca</button>
        </>
      )}

      {/* RESULTADO */}
      {step === 5 && (
        <>
          <h2>Resultado da sua marca</h2>
          <pre>{result}</pre>
          <button onClick={() => setStep(1)}>Criar outra</button>
        </>
      )}
    </div>
  );
}
