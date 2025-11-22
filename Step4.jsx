import axios from "axios";

export default function Step4({ setStep, form }) {

  async function generateBrand() {
    const response = await axios.post("http://localhost:4000/brand/generate", form);
    form.result = response.data;
    setStep(5);
  }

  return (
    <div>
      <h2>Gerar Identidade</h2>
      <button onClick={generateBrand}>Gerar agora</button>
    </div>
  );
}
