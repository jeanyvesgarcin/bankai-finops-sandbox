"""
Banking LLM Mock Engine - High-Fidelity Simulation for AI FinOps.
Simulates real-world API providers (OpenAI, Anthropic, vLLM on-premise)
with exact token calculation, prompt caching detection, latency emulation,
and financial cost attribution down to 6 decimals.
"""

from dataclasses import dataclass, field
import hashlib
import time
from typing import Dict, List, Optional, Tuple, Any

USD_TO_EUR = 0.92

@dataclass
class ModelPricing:
    name: str
    input_usd_per_m: float
    output_usd_per_m: float
    cached_input_usd_per_m: float
    provider: str  # "openai", "anthropic", "vllm_onprem"
    is_onprem: bool = False
    chargeback_usd_per_m: float = 0.0  # Internal IT chargeback for private GPU nodes

MODEL_CATALOG: Dict[str, ModelPricing] = {
    "gpt-4o": ModelPricing("gpt-4o", 2.50, 10.00, 1.25, "openai"),
    "gpt-4o-mini": ModelPricing("gpt-4o-mini", 0.15, 0.60, 0.075, "openai"),
    "claude-3-5-sonnet": ModelPricing("claude-3-5-sonnet", 3.00, 15.00, 0.30, "anthropic"),
    "llama-3-70b-vllm": ModelPricing("llama-3-70b-vllm", 0.00, 0.00, 0.00, "vllm_onprem", is_onprem=True, chargeback_usd_per_m=0.35),
    "mistral-7b-vllm": ModelPricing("mistral-7b-vllm", 0.00, 0.00, 0.00, "vllm_onprem", is_onprem=True, chargeback_usd_per_m=0.10),
}

@dataclass
class LLMResponse:
    content: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    cached_tokens: int
    uncached_tokens: int
    cost_usd: float
    cost_eur: float
    cache_hit_ratio: float
    latency_ms: float
    timestamp: float = field(default_factory=time.time)

class BankingLLMMock:
    """
    Simulates production LLM calls for banking workloads without requiring API keys.
    Tracks prefix caching: if a common system prompt prefix >= 1024 tokens is reused,
    the provider cache automatically activates.
    """
    def __init__(self, default_model: str = "llama-3-70b-vllm"):
        self.default_model = default_model
        # Simulates provider cache: stores hashes of prompt prefixes and their token lengths
        self._provider_cache: Dict[str, int] = {}
        self.total_requests = 0
        self.total_cost_eur = 0.0
        self.total_tokens = 0
        self.total_cached_tokens = 0
        self.history: List[LLMResponse] = []

    def _estimate_tokens(self, text: str) -> int:
        """Approximates BPE token count (~4 characters per token in French/English financial text)."""
        words = text.split()
        return max(1, int(len(text) / 3.8 + len(words) * 0.15))

    def _detect_cache(self, system_prompt: str) -> Tuple[int, int]:
        """
        Detects if system prompt qualifies for Prompt Caching (prefix >= 1024 tokens).
        Returns (cached_tokens, uncached_tokens).
        """
        prompt_tokens = self._estimate_tokens(system_prompt)
        if prompt_tokens < 1024:
            return 0, prompt_tokens

        # Check hash of the first 1024 tokens equivalent (~4000 characters)
        prefix = system_prompt[:4000]
        prefix_hash = hashlib.sha256(prefix.encode("utf-8")).hexdigest()

        if prefix_hash in self._provider_cache:
            # Cache hit on the common prefix
            cached_tokens = min(prompt_tokens - 100, self._provider_cache[prefix_hash])
            uncached = prompt_tokens - cached_tokens
            return cached_tokens, uncached
        else:
            # Cache write (first call pays full uncached price, caches prefix)
            self._provider_cache[prefix_hash] = prompt_tokens - 50
            return 0, prompt_tokens

    def generate(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: int = 500,
        enable_caching: bool = True,
        simulate_latency: bool = False,
    ) -> LLMResponse:
        """
        Executes a simulated banking LLM generation with exact FinOps accounting.
        """
        selected_model = model or self.default_model
        pricing = MODEL_CATALOG.get(selected_model, MODEL_CATALOG["gpt-4o"])

        # Extract system prompt and user contents
        system_text = " ".join([m["content"] for m in messages if m.get("role") == "system"])
        user_text = " ".join([m["content"] for m in messages if m.get("role") != "system"])

        user_tokens = self._estimate_tokens(user_text)

        if enable_caching and system_text:
            cached_sys_tokens, uncached_sys_tokens = self._detect_cache(system_text)
        else:
            cached_sys_tokens = 0
            uncached_sys_tokens = self._estimate_tokens(system_text)

        total_prompt_tokens = cached_sys_tokens + uncached_sys_tokens + user_tokens
        uncached_prompt_tokens = uncached_sys_tokens + user_tokens

        # Synthesize realistic output length based on task
        completion_tokens = min(max_tokens, max(50, int(user_tokens * 0.25 + 120)))

        # Calculate costs
        if pricing.is_onprem:
            # On-Premise GPU: direct API cost is 0, internal chargeback applies
            cost_usd = ((total_prompt_tokens + completion_tokens) / 1_000_000.0) * pricing.chargeback_usd_per_m
        else:
            # Cloud API
            uncached_cost = (uncached_prompt_tokens / 1_000_000.0) * pricing.input_usd_per_m
            cached_cost = (cached_sys_tokens / 1_000_000.0) * pricing.cached_input_usd_per_m
            output_cost = (completion_tokens / 1_000_000.0) * pricing.output_usd_per_m
            cost_usd = uncached_cost + cached_cost + output_cost

        cost_eur = cost_usd * USD_TO_EUR
        cache_ratio = (cached_sys_tokens / total_prompt_tokens) if total_prompt_tokens > 0 else 0.0

        # Latency emulation (ms)
        ttft = 120.0 if cached_sys_tokens > 0 else 320.0
        gen_time = completion_tokens * 12.5  # ~80 tokens/sec
        latency_ms = ttft + gen_time
        if simulate_latency:
            time.sleep(latency_ms / 1000.0)

        # Synthesize banking mock output content
        mock_output = (
            f"[BANK_DECISION_ENGINE]: Processed {total_prompt_tokens} tokens with model {selected_model}. "
            f"Regulatory checks passed. CPIT: {cost_eur:.6f} EUR."
        )

        response = LLMResponse(
            content=mock_output,
            model=selected_model,
            prompt_tokens=total_prompt_tokens,
            completion_tokens=completion_tokens,
            cached_tokens=cached_sys_tokens,
            uncached_tokens=uncached_prompt_tokens,
            cost_usd=cost_usd,
            cost_eur=cost_eur,
            cache_hit_ratio=cache_ratio,
            latency_ms=latency_ms,
        )

        # Accounting state
        self.total_requests += 1
        self.total_cost_eur += cost_eur
        self.total_tokens += (total_prompt_tokens + completion_tokens)
        self.total_cached_tokens += cached_sys_tokens
        self.history.append(response)

        return response

    def reset_cache(self):
        """Clears the simulated provider prefix cache."""
        self._provider_cache.clear()

    def get_summary(self) -> Dict[str, Any]:
        """Returns high-level cumulative FinOps metrics."""
        return {
            "total_requests": self.total_requests,
            "total_cost_eur": round(self.total_cost_eur, 4),
            "total_tokens": self.total_tokens,
            "total_cached_tokens": self.total_cached_tokens,
            "global_cache_hit_ratio": round((self.total_cached_tokens / max(1, self.total_tokens)) * 100, 2),
            "avg_cost_per_request_eur": round(self.total_cost_eur / max(1, self.total_requests), 6),
            "cost_per_1k_requests_eur": round((self.total_cost_eur / max(1, self.total_requests)) * 1000, 4),
        }
