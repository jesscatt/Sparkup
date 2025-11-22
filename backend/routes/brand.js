import { Router } from "express";
const router = Router();

// Aqui entraria sua integração com IA futuramente
router.post("/generate", (req, res) => {
  const data = req.body;

  const result = {
    summary: `
Marca: ${data.businessName}
Descrição: ${data.description}
Público-alvo: ${data.target}
Paleta esperada: ${data.palette}
`,
  };

  res.json(result);
});

export default router;
