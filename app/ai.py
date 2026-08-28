import os

import httpx


async def ask_ai(prompt: str) -> str:
    """Call an OpenAI-compatible chat endpoint when configured.

    Configure AI_API_URL, AI_API_KEY and AI_MODEL in the environment.
    This keeps secrets out of the repository and also allows local compatible
    servers to be used.
    """
    url = os.getenv("AI_API_URL")
    key = os.getenv("AI_API_KEY")
    model = os.getenv("AI_MODEL", "gpt-4o-mini")
    if not url or not key:
        return "AI is not configured yet. Set AI_API_URL, AI_API_KEY and AI_MODEL to enable it."

    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": [
        {"role": "system", "content": "You are DevDesk, a concise developer productivity assistant."},
        {"role": "user", "content": prompt},
    ]}
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    return data["choices"][0]["message"]["content"]
