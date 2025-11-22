import express from "express";
import cors from "cors";
import brandRouter from "./routes/brand.js";

const app = express();
app.use(cors());
app.use(express.json());

app.use("/brand", brandRouter);

const PORT = 4000;
app.listen(PORT, () => {
  console.log("API rodando na porta " + PORT);
});
