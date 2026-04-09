import os
import json
import asyncio
import string
import logging
from typing import Dict, Any, List
from dotenv import load_dotenv
from groq import AsyncGroq, GroqError

# Ensure environment variables are loaded
load_dotenv()

logger = logging.getLogger("backend")

class AIService:
    """Service to handle AI interactions using Groq (free tier)."""

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.warning("Groq API key is not set. Set GROQ_API_KEY in .env")
            self.client = None
        else:
            self.client = AsyncGroq(api_key=self.api_key)

    def _is_similar(self, desc1: str, desc2: str) -> bool:
        """Normalizes descriptions and performs semantic similarity matching."""
        def normalize(t: str) -> str:
            t = t.lower()
            return t.translate(str.maketrans('', '', string.punctuation)).strip()

        norm1 = normalize(desc1)
        norm2 = normalize(desc2)

        if not norm1 or not norm2:
            return False

        # Jaccard similarity for better deduplication
        words1 = set(norm1.split())
        words2 = set(norm2.split())

        stop_words = {"is", "are", "the", "a", "an", "this", "that", "it", "to", "in", "on", "of", "for", "and", "or", "found", "should", "could", "be"}
        words1 = words1 - stop_words
        words2 = words2 - stop_words

        if not words1 or not words2:
            return norm1 == norm2

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        score = len(intersection) / len(union)
        return score > 0.6 # Stricter threshold

    async def _analyze_chunk_with_retry(self, diff_chunk: str) -> Dict[str, Any]:
        """Calls Groq with JSON mode and system prompt."""
        system_prompt = """You are a Senior Code Quality and Security Engineer.
Analyze the code diff and return a JSON object with issues found.
STRICT RULES:
- Return ONLY valid JSON.
- limit output to MAX 5 issues per chunk.
- Label minor inefficiencies as 'low'.
- Label performance/bugs as 'medium'.
- Label security vulnerabilities as 'high'.
- Provide a REAL fix (actual code snippet for suggestion).
- 'file' MUST match the file path in the diff.
- 'line' MUST be the actual line number from the diff (int).
- If no issues found, return {"issues": []}.
- Detect Phrases like "no fix needed" and REJECT such issues entirely."""

        user_prompt = f"Code Diff Chunk:\n{diff_chunk}"

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.1,
                    response_format={"type": "json_object"}
                )

                content = response.choices[0].message.content.strip()
                parsed_json = json.loads(content)
                logger.info(f"[analyze_code] success on attempt {attempt + 1}")
                return parsed_json

            except (json.JSONDecodeError, GroqError, Exception) as e:
                logger.error(f"[analyze_code] error on attempt {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)

        logger.error("[analyze_code] Failed after retries, skipping chunk")
        return {"issues": []}

    def _get_line_aware_chunks(self, diff: str, max_size: int = 4000) -> list:
        """Splits diff into chunks without breaking lines."""
        lines = diff.splitlines()
        chunks = []
        current_chunk = []
        current_size = 0

        for line in lines:
            line_size = len(line) + 1
            if current_size + line_size > max_size and current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_size = 0

            current_chunk.append(line)
            current_size += line_size

        if current_chunk:
            chunks.append("\n".join(current_chunk))

        return chunks

    async def analyze_code(self, diff: str) -> Dict[str, Any]:
        """Analyzes code diff content using AI, handling large diff chunking."""
        if not diff:
            return {"status": "failed", "reason": "EMPTY_DIFF", "issues": []}

        if not self.client:
            return {"status": "failed", "reason": "CLIENT_NOT_INITIALIZED", "issues": []}

        chunks = self._get_line_aware_chunks(diff)
        all_issues = []
        seen_descriptions = []

        any_success = False

        for chunk in chunks:
            result = await self._analyze_chunk_with_retry(chunk)
            issues = result.get("issues", [])

            # If we got a result (even empty issues), it's a success for this chunk
            if isinstance(issues, list):
                any_success = True
            else:
                continue

            for issue in issues:
                desc = issue.get("description", "").strip()
                fix = issue.get("fix", "").strip()

                # Basic validation: must have desc and fix, and fix shouldn't be "no fix needed"
                if not desc or not fix or "no fix needed" in fix.lower():
                    continue

                is_duplicate = False
                for seen_desc in seen_descriptions:
                    if self._is_similar(desc, seen_desc):
                        is_duplicate = True
                        break

                if not is_duplicate:
                    seen_descriptions.append(desc)
                    all_issues.append(issue)

        if not any_success:
            return {"status": "failed", "reason": "AI_ANALYSIS_FAILED", "issues": []}

        status = "success" if len(chunks) == 1 or any_success else "partial"
        return {"status": status, "issues": all_issues}

def get_ai_service() -> AIService:
    return AIService()

_ai_service_instance = AIService()

async def analyze_code(diff: str) -> Dict[str, Any]:
    return await _ai_service_instance.analyze_code(diff)
