export default function Result({ form }) {
  return (
    <div>
      <h2>Resultado</h2>
      <pre>{form.result.summary}</pre>
    </div>
  );
}
