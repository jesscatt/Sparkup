export default function Step3({ setStep, setForm, form }) {
  return (
    <div>
      <h2>Descrição da empresa</h2>
      <textarea
        value={form.description || ""}
        onChange={e => setForm({ ...form, description: e.target.value })}
      />
      <button onClick={() => setStep(4)}>Próximo</button>
    </div>
  );
}
