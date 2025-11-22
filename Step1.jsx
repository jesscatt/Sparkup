export default function Step1({ setStep, setForm, form }) {
  return (
    <div>
      <h2>Sobre sua empresa</h2>
      <input
        type="text"
        placeholder="Nome da marca"
        value={form.businessName || ""}
        onChange={e => setForm({...form, businessName: e.target.value })}
      />
      <button onClick={() => setStep(2)}>Próximo</button>
    </div>
  );
}
