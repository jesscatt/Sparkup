import express from "express";
import cors from "cors";

const app = express();
app.use(express.json());
app.use(cors());

app.post("/brand", (req, res) => {
  const { businessName, audience, color, tone } = req.body;

  const result = `
Marca: ${businessName}
Público: ${audience}
Cor principal: ${color}
Tom de comunicação: ${tone}

Resumo:
${businessName} é uma marca criada para ${audience}, com identidade visual baseada na cor ${color} e comunicação em um tom ${tone}.
  `;

  res.json({ result });
});

app.listen(4000, () => {
  console.log("API rodando em http://localhost:4000");
});
