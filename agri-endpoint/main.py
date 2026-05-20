from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="AgriAdvisor India API",
    description="Agriculture advisory endpoint for Indian smallholder farmers",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    message: str
    language: str = "en"
    location: Optional[str] = "generic"
    farmer_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    metadata: dict

CROP_DB = {
    "rice": {
        "advice": "For rice in India: use certified seeds (100 kg/ha for direct seeding). Apply NPK 120:60:40 kg/ha. Maintain 2-3 cm water depth during transplanting. Recommended varieties: MTU 1010, IR 64.",
        "confidence": 0.92
    },
    "wheat": {
        "advice": "For wheat: sow timely using HD 2967 or DBW 187 varieties. Seed rate: 100 kg/ha. Apply half N and full P,K at sowing. Irrigate at crown root, flowering, and grain filling stages.",
        "confidence": 0.89
    },
    "cotton": {
        "advice": "For cotton: deep ploughing recommended. Apply FYM 10 tonnes/ha. Use Bt cotton hybrids. Monitor for bollworm. Keep 90 cm row spacing.",
        "confidence": 0.85
    },
    "sugarcane": {
        "advice": "For sugarcane: plant CO 0238 variety. Setts: 75,000 double-eyed/ha. Apply NPK 250:100:125 kg/ha. Irrigate weekly in summer.",
        "confidence": 0.88
    }
}

PEST_DB = {
    "aphid": {
        "advice": "For aphids: spray neem oil 3% (30 mL/L water) or imidacloprid 17.8 SL 0.3 mL/L. Repeat after 10 days if infestation persists. Avoid spraying during flowering.",
        "safety_flags": ["chemical_pesticide", "follow_pre_harvest_interval"],
        "confidence": 0.90
    },
    "bollworm": {
        "advice": "For cotton bollworm: install pheromone traps (5/acre). Use Bacillus thuringiensis (Bt) based bio-pesticide as first line. If chemical needed, use chlorantraniliprole 18.5 SC 0.3 mL/L.",
        "safety_flags": ["bio_pesticide_preferred", "chemical_if_severe"],
        "confidence": 0.87
    },
    "blast": {
        "advice": "For rice blast: avoid excess nitrogen. Spray tricyclazole 75 WP 0.1% at appearance of lesions. Ensure 15-day pre-harvest interval.",
        "safety_flags": ["chemical_fungicide", "follow_pre_harvest_interval"],
        "confidence": 0.91
    },
    "wilt": {
        "advice": "For cotton wilt: drench with carbendazim 50 WP 1 g/L at root zone. Ensure crop rotation with cereals. Avoid monocropping.",
        "safety_flags": ["chemical_fungicide", "crop_rotation_recommended"],
        "confidence": 0.84
    }
}

FERTILIZER_DB = {
    "npk rice": "NPK 120:60:40 kg/ha. Apply N in 3 splits: 50% basal, 25% at tillering, 25% at panicle initiation.",
    "urea wheat": "Urea: 260 kg/ha total. Apply 130 kg at sowing, 65 kg at first irrigation, 65 kg at flowering.",
    "dap cotton": "DAP: 130 kg/ha as basal. Top dress with urea 100 kg/ha at square formation."
}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    msg = request.message.lower()
    
    response_data = {
        "response": "",
        "metadata": {
            "confidence": 0.0,
            "safety_flags": [],
            "language": request.language,
            "location": request.location,
            "category": "unknown"
        }
    }
    
    if any(k in msg for k in ["rice", "paddy", "ধান", "వరి"]):
        data = CROP_DB["rice"]
        response_data["response"] = data["advice"]
        response_data["metadata"]["confidence"] = data["confidence"]
        response_data["metadata"]["category"] = "crop_recommendation"
    elif any(k in msg for k in ["wheat", "gehun", "గోధుమ", "gehu"]):
        data = CROP_DB["wheat"]
        response_data["response"] = data["advice"]
        response_data["metadata"]["confidence"] = data["confidence"]
        response_data["metadata"]["category"] = "crop_recommendation"
    elif any(k in msg for k in ["cotton", "kapas", "పత్తి"]):
        data = CROP_DB["cotton"]
        response_data["response"] = data["advice"]
        response_data["metadata"]["confidence"] = data["confidence"]
        response_data["metadata"]["category"] = "crop_recommendation"
    elif any(k in msg for k in ["sugarcane", "ganna", "చెరకు"]):
        data = CROP_DB["sugarcane"]
        response_data["response"] = data["advice"]
        response_data["metadata"]["confidence"] = data["confidence"]
        response_data["metadata"]["category"] = "crop_recommendation"
    elif any(k in msg for k in ["aphid", "sucking pest", "mealybug"]):
        data = PEST_DB["aphid"]
        response_data["response"] = data["advice"]
        response_data["metadata"]["confidence"] = data["confidence"]
        response_data["metadata"]["safety_flags"] = data["safety_flags"]
        response_data["metadata"]["category"] = "pest_management"
    elif any(k in msg for k in ["bollworm", "cotton pest", "fruit borer"]):
        data = PEST_DB["bollworm"]
        response_data["response"] = data["advice"]
        response_data["metadata"]["confidence"] = data["confidence"]
        response_data["metadata"]["safety_flags"] = data["safety_flags"]
        response_data["metadata"]["category"] = "pest_management"
    elif any(k in msg for k in ["blast", "fungus", "fungal", "blight"]):
        data = PEST_DB["blast"]
        response_data["response"] = data["advice"]
        response_data["metadata"]["confidence"] = data["confidence"]
        response_data["metadata"]["safety_flags"] = data["safety_flags"]
        response_data["metadata"]["category"] = "pest_management"
    elif any(k in msg for k in ["wilt", "root rot", "damping off"]):
        data = PEST_DB["wilt"]
        response_data["response"] = data["advice"]
        response_data["metadata"]["confidence"] = data["confidence"]
        response_data["metadata"]["safety_flags"] = data["safety_flags"]
        response_data["metadata"]["category"] = "pest_management"
    elif any(k in msg for k in ["fertilizer", "npk", "urea", "dap", "खाद"]):
        if "rice" in msg:
            response_data["response"] = FERTILIZER_DB["npk rice"]
            response_data["metadata"]["confidence"] = 0.90
        elif "wheat" in msg:
            response_data["response"] = FERTILIZER_DB["urea wheat"]
            response_data["metadata"]["confidence"] = 0.90
        elif "cotton" in msg:
            response_data["response"] = FERTILIZER_DB["dap cotton"]
            response_data["metadata"]["confidence"] = 0.90
        else:
            response_data["response"] = "Please specify your crop for fertilizer recommendations. Common schedules: Rice-NPK 120:60:40, Wheat-Urea 260 kg/ha, Cotton-DAP 130 kg/ha."
            response_data["metadata"]["confidence"] = 0.60
        response_data["metadata"]["category"] = "fertilizer_guidance"
    elif any(k in msg for k in ["weather", "rain", "drought", "irrigation"]):
        response_data["response"] = "For irrigation scheduling: rice needs continuous flooding, wheat needs 3-4 irrigations at critical stages, cotton needs weekly irrigation in summer. Check local weather forecasts before spraying pesticides."
        response_data["metadata"]["confidence"] = 0.75
        response_data["metadata"]["category"] = "weather_advisory"
    elif any(k in msg for k in ["profit", "acre", "small", "cost", "budget", "loan"]):
        response_data["response"] = "For 1-acre holdings: wheat and vegetables offer quick returns. Rice requires more water but has MSP support. Consider drip irrigation to reduce water costs. Contact your nearest KVK for subsidized inputs."
        response_data["metadata"]["confidence"] = 0.70
        response_data["metadata"]["category"] = "economic_advisory"
    else:
        response_data["response"] = "Thank you for your query. Please specify your crop (rice, wheat, cotton, sugarcane), pest issue, or ask about fertilizer schedules. You can also mention your state for localized advice."
        response_data["metadata"]["confidence"] = 0.35
        response_data["metadata"]["category"] = "fallback"
    
    return response_data

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "AgriAdvisor India API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
