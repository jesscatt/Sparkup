export default function Step2({ setStep, setForm, form }) {
  return (
    <div>
      <h2>Qual seu público-alvo?</h2>
      <textarea
        value={form.target || ""}
        onChange={e => setForm({ ...form, target: e.target.value })}
      />
      <button onClick={() => setStep(3)}>Próximo</button>
    </div>
  );
}
