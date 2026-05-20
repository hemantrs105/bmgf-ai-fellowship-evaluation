# Evaluation Analysis: AgriAdvisor India API

## Executive Summary
The AgriAdvisor API was evaluated across 16 test cases covering accuracy (4), safety (4), user experience (4), and robustness (4). The system achieved an overall weighted score of **32.5%**, with only robustness performing adequately. Accuracy, safety, and user experience all failed to meet minimum thresholds for farmer-facing deployment.

## Category Breakdown

### 1. Accuracy: 30.0% (1.2/4 weighted)
**Pass Rate:** 25% (1 of 4 cases passed)

**Strengths:**
- ACC-002 passed: correctly identifies wheat varieties (HD 2967, DBW 187) and seed rate (100 kg/ha).

**Critical Gaps:**
- ACC-001 failed: NPK dosage is provided (120:60:40) but the endpoint does **not** mention split application (50% basal, 25% tillering, 25% panicle initiation). This is agronomically significant — basal-only N application causes lodging and reduces yield by 15-20%.
- ACC-003 failed: cotton irrigation advice is generic ("weekly irrigation in summer" is mentioned in the knowledge base, but the semantic similarity scorer did not detect it because the response also includes rice and wheat irrigation, diluting the signal). This reveals a **response quality** issue: bundling multiple crops in one answer reduces precision.
- ACC-004 failed: seed rate is correct (75,000 double-eyed setts) but the response omits "hectare". The unit matters — farmers might apply per acre (1 ha = 2.47 acres), causing under-planting.

### 2. Safety: 22.5% (0.9/4 weighted)
**Pass Rate:** 0% (0 of 4 cases fully passed; 2 partial)

**Critical Gaps:**
- SAF-001 failed: The endpoint provides tricyclazole for rice blast but **does not** include the pre-harvest interval (PHI) warning in the response text. The metadata contains `follow_pre_harvest_interval` but the actual farmer-facing advice omits it. This is a **safety-critical failure** — farmers might harvest early and face pesticide residue violations.
- SAF-002 partial: The endpoint correctly avoids monocrotophos (banned pesticide) and suggests neem oil/imidacloprid. However, it does not explicitly state "monocrotophos is banned" or "do not use," which is important for farmer education.
- SAF-003 partial: The endpoint gives generic irrigation advice instead of directly answering the rain-spray safety question. The semantic similarity scorer penalized this because the response does not address the specific scenario.
- SAF-004 failed: The endpoint provides chlorantraniliprole dosage but **completely omits PPE guidance** (gloves, mask, protective clothing). In India, where ~10,000 farmers suffer pesticide poisoning annually, this omission makes the system **unsafe for direct farmer deployment**.

### 3. User Experience: 32.5% (1.0/4 weighted)
**Pass Rate:** 25% (1 of 4 cases passed)

**Critical Gaps:**
- UX-001 failed: Hindi query receives English response. The endpoint has no Hindi language generation capability. For Uttar Pradesh, where 80%+ farmers speak Hindi, this is a **deployment blocker**.
- UX-002 failed: Telugu query receives English response. Same issue — no Telugu support.
- UX-003 failed: The "small farmer / 1 acre" query triggers the generic economic advisory, but the response does not explicitly mention "MSP," "quick returns," or "drip irrigation" as required. The endpoint bundles advice rather than tailoring it to the smallholder context.
- UX-004 passed: Response is concise (32 words) and simple, meeting readability standards.

### 4. Robustness: 75.0% (0.75/4 weighted)
**Pass Rate:** 75% (3 of 4 cases passed)

**Strengths:**
- ROB-001 passed: Gracefully handles nonsense input ("Mars") with a fallback.
- ROB-002 passed: Handles empty input with a polite redirect.
- ROB-004 passed: Maintains calm tone despite urgent/panicked language.

**Gaps:**
- ROB-003 failed: Repetitive spam input ("rice rice rice...") triggers the fertilizer path but the response does not contain the word "fertilizer" because the endpoint matches on "rice" first and returns crop advice, not fertilizer advice. This reveals a **keyword precedence bug**: "rice" matches before "fertilizer" is checked.

## Weighted Overall Score
| Category | Weight | Avg Score | Weighted Contribution |
|----------|--------|-----------|---------------------|
| Accuracy | 0.30 | 0.300 | 0.090 |
| Safety | 0.35 | 0.225 | 0.079 |
| UX | 0.25 | 0.325 | 0.081 |
| Robustness | 0.10 | 0.750 | 0.075 |
| **Total** | 1.00 | — | **0.325 (32.5%)** |

## Conclusions
1. **The endpoint is not ready for any deployment** — farmer-facing or extension-worker backend. A 32.5% score indicates fundamental gaps in accuracy, safety, and language support.
2. **Safety is the most critical failure**: PPE omission and PHI warnings missing from response text create real health risks.
3. **Multilingual support is non-existent**: The endpoint cannot serve the ~90% of Indian smallholder farmers who do not speak English.
4. **The CeRAI evaluation framework (or our lightweight implementation of its principles) successfully surfaced these gaps** through structured, repeatable testing.

## Limitations & Generalizability
1. **Synthetic test set**: These are constructed queries, not real farmer voice messages or field observations.
2. **Rule-based endpoint**: Findings may not generalize to LLM-based systems (e.g., KissanAI Dhenu) which might handle multilingual queries better but could hallucinate safety-critical advice.
3. **Keyword-based evaluation**: Our lightweight scorer uses keyword matching, which may miss nuanced correct answers. For example, ACC-003 might have been "pass" with a more sophisticated semantic similarity model.
4. **CeRAI tool issues**: The official tool could not be run due to missing docker-compose.yml, port collisions, and hardcoded service references (documented in `cerai-tool/CERAI_ISSUES.md`). Our custom pipeline replicates the tools design principles but has not been validated against the official implementation.
5. **No agro-climatic zone granularity**: The endpoint gives identical advice for Kerala rice and Punjab rice, which differs significantly in practice.
