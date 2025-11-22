from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
import openai
import json
import random
import uuid
import os
from dotenv import load_dotenv
import uvicorn
from datetime import datetime

# Carrega as variáveis do arquivo .env
load_dotenv()

class TomMarca(str, Enum):
    SERIA = "séria"
    DESCONTRAIDA = "descontraída"
    EQUILIBRADA = "equilibrada"
    LUXUOSA = "luxuosa"

class EstiloVisual(str, Enum):
    MINIMALISTA = "minimalista"
    VIBRANTE = "vibrante"
    ELEGANTE = "elegante"
    ORGANICO = "orgânico"

class EstiloTemporal(str, Enum):
    MODERNA = "moderna"
    CLASSICA = "clássica"
    FUTURISTA = "futurista"
    RETRO = "retrô"

class ObjetivoMarca(str, Enum):
    VENDER = "vender"
    SERVICOS = "servicos"
    EDUCAR = "educar"
    ENTRETER = "entreter"
    COMUNIDADE = "comunidade"

class BrandRequest(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    segmento: str = Field(..., min_length=2, max_length=100)
    palavras: str = Field(..., description="Três palavras que definem a marca")
    cores_sim: str = Field(..., description="Cores que combinam")
    cores_nao: str = Field(..., description="Cores que NÃO combinam")
    tom: TomMarca
    estilo: EstiloVisual
    moderno: EstiloTemporal
    publico: str = Field(..., min_length=2, max_length=200)
    objetivo: ObjetivoMarca
    inspiracao: Optional[str] = None
    elementos: Optional[str] = None

class ColorPalette(BaseModel):
    primary: str
    secondary: str
    accent: str
    neutral: str
    success: str

class Typography(BaseModel):
    primary_font: str
    secondary_font: str
    font_weights: Dict[str, int]

class SocialMediaPost(BaseModel):
    concept: str
    colors: List[str]
    caption: str
    hashtags: List[str]

class BrandResponse(BaseModel):
    brand_name: str
    slogan: str
    color_palette: ColorPalette
    typography: Typography
    social_media_posts: List[SocialMediaPost]
    captions: List[str]
    brand_description: str
    recommendations: List[str]

class BrandAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "sua_chave_aqui":
            self.client = openai.OpenAI(api_key=api_key)
            self.use_ai = True
            print("🤖 Serviço OpenAI configurado com sucesso!")
            print(f"✅ Chave API carregada: {api_key[:20]}...")  # Mostra apenas os primeiros caracteres
        else:
            self.client = None
            self.use_ai = False
            print("⚠️  OpenAI não configurado - Usando gerador local")
            if not api_key:
                print("❌ Nenhuma chave API encontrada no arquivo .env")
            else:
                print("❌ Chave API não configurada corretamente")

    def generate_brand_identity(self, request: BrandRequest) -> BrandResponse:
        if self.use_ai and self.client:
            try:
                print(f"🚀 Gerando identidade com OpenAI para: {request.nome}")
                return self._generate_with_ai(request)
            except Exception as e:
                print(f"❌ Erro na OpenAI: {e} - Usando fallback local")
                return self._generate_local(request)
        else:
            print(f"🎨 Gerando identidade local para: {request.nome}")
            return self._generate_local(request)

    def _generate_with_ai(self, request: BrandRequest) -> BrandResponse:
        prompt = self._create_ai_prompt(request)
        
        try:
            print("📡 Enviando solicitação para OpenAI...")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """Você é um especialista criativo em branding e design. 
                        Gere identidades visuais ÚNICAS e ORIGINAIS baseadas nas informações.
                        Seja CRIATIVO e evite repetições. Retorne APENAS JSON válido."""
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,  # Aumentado para mais criatividade
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            print("✅ Resposta recebida da OpenAI")
            
            # Limpa o conteúdo removendo markdown
            content = content.replace('```json', '').replace('```', '').strip()
            
            brand_data = json.loads(content)
            return self._parse_ai_response(brand_data, request.nome)
            
        except Exception as e:
            print(f"❌ Erro ao processar resposta da OpenAI: {e}")
            raise

    def _create_ai_prompt(self, request: BrandRequest) -> str:
        palavras_lista = request.palavras.split(',')[:3]
        
        return f"""
        Crie uma identidade visual COMPLETAMENTE ÚNICA e CRIATIVA para a marca: {request.nome}

        CONTEXTO ESPECÍFICO:
        - Segmento: {request.segmento}
        - Palavras-chave: {', '.join(palavras_lista)}
        - Cores preferidas: {request.cores_sim}
        - Cores a evitar: {request.cores_nao}
        - Tom de voz: {request.tom}
        - Estilo visual: {request.estilo}
        - Estilo temporal: {request.moderno}
        - Público-alvo: {request.publico}
        - Objetivo: {request.objetivo}
        - Inspirações: {request.inspiracao or 'Não especificado'}
        - Elementos: {request.elementos or 'Não especificado'}

        **INSTRUÇÕES CRÍTICAS:**
        - Seja EXTREMAMENTE CRIATIVO e ORIGINAL
        - NUNCA repita as mesmas cores, slogans ou conceitos
        - Crie combinações de cores INOVADORAS e ÚNICAS
        - Gere slogans COMPLETAMENTE DIFERENTES para cada marca
        - Adapte TUDO ao contexto específico fornecido
        - Use tipografias DIFERENTES baseadas no estilo
        - Crie conceitos de posts ORIGINAIS e ÚNICOS

        RETORNE APENAS JSON com esta estrutura:
        {{
            "slogan": "slogan criativo e memorável ÚNICO para {request.nome}",
            "color_palette": {{
                "primary": "cor HEXADECIMAL única baseada em {request.cores_sim}",
                "secondary": "cor HEXADECIMAL complementar ÚNICA", 
                "accent": "cor HEXADECIMAL de destaque INOVADORA",
                "neutral": "cor HEXADECIMAL neutra equilibrada",
                "success": "cor HEXADECIMAL para sucesso harmoniosa"
            }},
            "typography": {{
                "primary_font": "Nome de fonte ÚNICA para {request.estilo}",
                "secondary_font": "Nome de fonte complementar DIFERENTE",
                "font_weights": {{
                    "light": 300,
                    "regular": 400,
                    "bold": 700
                }}
            }},
            "social_media_posts": [
                {{
                    "concept": "conceito criativo ÚNICO 1 para {request.nome}",
                    "colors": ["#cor1", "#cor2"],
                    "caption": "legenda engajadora ORIGINAL 1 para {request.publico}",
                    "hashtags": ["#{request.nome.replace(' ', '')}", "#{request.segmento}"]
                }},
                {{
                    "concept": "conceito criativo ÚNICO 2 para {request.segmento}", 
                    "colors": ["#cor3", "#cor4"],
                    "caption": "legenda engajadora ORIGINAL 2 sobre {', '.join(palavras_lista)}",
                    "hashtags": ["#{palavras_lista[0]}", "#{request.moderno}"]
                }}
            ],
            "captions": [
                "legenda COMPLETAMENTE ORIGINAL 1 para redes sociais",
                "legenda ÚNICA 2 destacando {palavras_lista[1]}",
                "legenda INOVADORA 3 com call-to-action personalizado"
            ],
            "brand_description": "descrição completa e ÚNICA da identidade visual de {request.nome}",
            "recommendations": [
                "recomendação prática PERSONALIZADA 1 para {request.nome}",
                "recomendação específica 2 baseada em {request.estilo}",
                "recomendação ÚNICA 3 para {request.publico}"
            ]
        }}
        """

    def _parse_ai_response(self, brand_data: Dict, brand_name: str) -> BrandResponse:
        return BrandResponse(
            brand_name=brand_name,
            slogan=brand_data.get("slogan", f"Excelência em {brand_name}"),
            color_palette=ColorPalette(**brand_data["color_palette"]),
            typography=Typography(**brand_data["typography"]),
            social_media_posts=[SocialMediaPost(**post) for post in brand_data["social_media_posts"]],
            captions=brand_data["captions"],
            brand_description=brand_data["brand_description"],
            recommendations=brand_data["recommendations"]
        )

    def _generate_local(self, request: BrandRequest) -> BrandResponse:
        # Paletas de cores mais variadas
        color_palettes = {
            "minimalista": [
                {"primary": "#2D3748", "secondary": "#4A5568", "accent": "#3182CE", "neutral": "#F7FAFC", "success": "#38A169"},
                {"primary": "#1A202C", "secondary": "#2D3748", "accent": "#2B6CB0", "neutral": "#EDF2F7", "success": "#2F855A"},
                {"primary": "#4A5568", "secondary": "#718096", "accent": "#4299E1", "neutral": "#EBF4FF", "success": "#48BB78"}
            ],
            "vibrante": [
                {"primary": "#E53E3E", "secondary": "#DD6B20", "accent": "#D69E2E", "neutral": "#FFFBEB", "success": "#38A169"},
                {"primary": "#B83280", "secondary": "#D69E2E", "accent": "#38A169", "neutral": "#FAF5FF", "success": "#2F855A"},
                {"primary": "#3182CE", "secondary": "#DD6B20", "accent": "#B83280", "neutral": "#EBF8FF", "success": "#38A169"}
            ],
            "elegante": [
                {"primary": "#1A365D", "secondary": "#2D3748", "accent": "#B7791F", "neutral": "#EDF2F7", "success": "#276749"},
                {"primary": "#2D3748", "secondary": "#4A5568", "accent": "#744210", "neutral": "#FAFAFA", "success": "#22543D"},
                {"primary": "#322659", "secondary": "#44337A", "accent": "#B7791F", "neutral": "#FAF5FF", "success": "#22543D"}
            ],
            "orgânico": [
                {"primary": "#22543D", "secondary": "#2F855A", "accent": "#D69E2E", "neutral": "#F0FFF4", "success": "#38A169"},
                {"primary": "#1A4731", "secondary": "#2D5A3C", "accent": "#B7791F", "neutral": "#F0FFF4", "success": "#2F855A"},
                {"primary": "#2F855A", "secondary": "#38A169", "accent": "#D69E2E", "neutral": "#F0FFF4", "success": "#48BB78"}
            ]
        }
        
        # Seleciona uma paleta aleatória baseada no estilo
        estilo_palettes = color_palettes.get(request.estilo, color_palettes["minimalista"])
        palette = random.choice(estilo_palettes)
        
        # Slogans mais variados
        slogans = {
            "séria": [
                f"Excelência em {request.segmento} - {request.nome}",
                f"Profissionalismo que inspira confiança",
                f"{request.nome}: Qualidade e seriedade",
                f"Soluções {request.segmento} com credibilidade"
            ],
            "descontraída": [
                f"Tornando {request.segmento} divertido!",
                f"{request.nome}: Estilo com personalidade",
                f"Experiências incríveis em {request.segmento}",
                f"{request.segmento} com alegria e descontração"
            ],
            "equilibrada": [
                f"O equilíbrio perfeito em {request.segmento}",
                f"{request.nome}: Tradição e inovação",
                f"Harmonia entre qualidade e acessibilidade",
                f"Conectando tradição e modernidade"
            ],
            "luxuosa": [
                f"O luxo redefinido em {request.segmento}",
                f"{request.nome}: Sofisticação sem igual",
                f"Experiência premium exclusiva",
                f"Excelência que transcende expectativas"
            ]
        }
        
        palavras_lista = request.palavras.split(',')[:3]
        slogan = random.choice(slogans.get(request.tom, slogans["equilibrada"]))

        # Posts mais variados
        posts = [
            SocialMediaPost(
                concept=f"Lançamento {request.nome}",
                colors=[palette["primary"], palette["accent"]],
                caption=f"🚀 Estamos lançando o {request.nome}! Uma nova era em {request.segmento} para {request.publico}.",
                hashtags=[f"#{request.nome.replace(' ', '')}", f"#{request.segmento}", "#novamarca"]
            ),
            SocialMediaPost(
                concept=f"Valores {palavras_lista[0]}",
                colors=[palette["secondary"], palette["success"]],
                caption=f"💫 {palavras_lista[0].title()} é nosso compromisso com {request.publico}. Descubra a diferença {request.nome}!",
                hashtags=[f"#{palavras_lista[0]}", "#valores", "#qualidade"]
            ),
            SocialMediaPost(
                concept="Futuro e Inovação",
                colors=[palette["accent"], palette["primary"]],
                caption=f"🌟 Moldando o futuro do {request.segmento} com soluções {request.moderno.lower()}.",
                hashtags=["#inovação", "#futuro", f"#{request.segmento}"]
            )
        ]

        # Legendas mais variadas
        captions = [
            f"Bem-vindo ao {request.nome} - revolucionando o {request.segmento}",
            f"Descubra uma nova experiência em {request.segmento} com {request.nome}",
            f"{palavras_lista[0].title()}, {palavras_lista[1].title()}, {palavras_lista[2].title()} - é o que nos define",
            f"Transformando {request.segmento} com excelência desde o primeiro dia",
            f"Conectando {request.publico} com as melhores soluções em {request.segmento}"
        ]

        brand_description = (
            f"Identidade visual criada para {request.nome}, uma marca {request.estilo} "
            f"e {request.moderno.lower()} no segmento de {request.segmento}. "
            f"Com foco em {', '.join(palavras_lista)}, a marca se comunica de forma {request.tom} "
            f"com seu público-alvo: {request.publico}."
        )

        recommendations = [
            f"Use a cor primária ({palette['primary']}) para logotipo e elementos principais",
            f"A cor secundária ({palette['secondary']}) é ideal para botões e call-to-actions",
            f"O acento ({palette['accent']}) deve ser usado para destaques e elementos interativos",
            f"Mantenha a tipografia '{request.estilo}' em todos os materiais",
            f"Adapte o tom {request.tom} na comunicação com {request.publico}",
            f"Utilize a paleta de cores de forma consistente em todas as plataformas"
        ]
        
        return BrandResponse(
            brand_name=request.nome,
            slogan=slogan,
            color_palette=ColorPalette(**palette),
            typography=Typography(
                primary_font="Inter",
                secondary_font="system-ui",
                font_weights={"light": 300, "regular": 400, "bold": 700}
            ),
            social_media_posts=posts,
            captions=captions,
            brand_description=brand_description,
            recommendations=recommendations
        )

app = FastAPI(
    title="BrandAI API",
    description="API inteligente para geração de identidades visuais",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

brand_service = BrandAIService()
brand_cache = {}

@app.get("/")
async def root():
    return {
        "message": "🚀 BrandAI API - Gerador de Identidades Visuais",
        "version": "2.0.0",
        "status": "operational",
        "ai_service": "OpenAI" if brand_service.use_ai else "Local Generator"
    }

@app.post("/api/generate-brand", response_model=BrandResponse)
async def generate_brand(request: BrandRequest):
    try:
        print(f"🎯 Recebendo solicitação para: {request.nome}")
        print(f"   Segmento: {request.segmento}")
        print(f"   Estilo: {request.estilo}")
        print(f"   Usando: {'OpenAI' if brand_service.use_ai else 'Gerador Local'}")

        start_time = datetime.now()
        brand_response = brand_service.generate_brand_identity(request)
        processing_time = (datetime.now() - start_time).total_seconds()
   
        brand_id = str(uuid.uuid4())
        brand_cache[brand_id] = {
            "id": brand_id,
            "request": request.dict(),
            "response": brand_response.dict(),
            "created_at": datetime.now().isoformat(),
            "processing_time": processing_time
        }
        
        print(f"✅ Identidade gerada em {processing_time:.2f}s")
        print(f"   Slogan: {brand_response.slogan}")
        print(f"   Cores: {brand_response.color_palette.primary}, ...")
        
        return brand_response
        
    except Exception as e:
        print(f"❌ Erro ao gerar identidade: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno ao gerar identidade visual: {str(e)}"
        )

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_service": "OpenAI" if brand_service.use_ai else "Local Generator",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 BrandAI Backend - Iniciando...")
    print("=" * 50)
    
    # Verifica se a chave está configurada
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "sua_chave_aqui":
        print(f"✅ Chave API detectada: {api_key[:20]}...")
    else:
        print("❌ Chave API não configurada")
        print("💡 Crie um arquivo .env com: OPENAI_API_KEY=sua_chave_aqui")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
