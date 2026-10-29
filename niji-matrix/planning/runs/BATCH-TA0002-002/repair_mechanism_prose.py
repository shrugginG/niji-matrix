from __future__ import annotations

from typing import Any

import integrate_remaining_execution as integration


def natural_mechanism(item: dict[str, str], ref: str) -> dict[str, Any]:
    effect_zh, effect_en = integration.MECHANISM_EFFECTS[item["ref"]]
    return {
        "mechanism_ref": item["ref"],
        "role": item["role"],
        "summary": {"zh": item["zh"], "en": item["en"]},
        "analysis": integration.prose(
            f"攻击者有意采用该行为设计，使{item['trace_zh']}。由此，{item['effect_zh']}，而{effect_zh}。不过，{item['residual_zh']}；跨层采集和因果关联能够削弱这种匿迹。",
            f"The adversary deliberately adopts this behavior design so that {item['trace_en']}. As a result, {item['effect_en']}. {effect_en}. However, {item['residual_en']}; cross-layer collection and causal correlation can weaken this stealth effect.",
        ),
        "evidence_refs": [ref],
        "confidence": item["confidence"],
    }


def repair_generator_source() -> None:
    path = integration.Path(integration.__file__)
    text = path.read_text(encoding="utf-8")
    old = "f\"攻击者有意采用该行为设计，使{item['trace_zh']}。防守方因此{item['effect_zh']}，{effect_zh}。不过，{item['residual_zh']}；跨层采集和因果关联能够削弱这种匿迹。\", f\"The adversary deliberately adopts this behavior design so that {item['trace_en']}. The defender therefore {item['effect_en']}; {effect_en}. However, {item['residual_en']}; cross-layer collection and causal correlation can weaken this stealth effect.\""
    new = "f\"攻击者有意采用该行为设计，使{item['trace_zh']}。由此，{item['effect_zh']}，而{effect_zh}。不过，{item['residual_zh']}；跨层采集和因果关联能够削弱这种匿迹。\", f\"The adversary deliberately adopts this behavior design so that {item['trace_en']}. As a result, {item['effect_en']}. {effect_en}. However, {item['residual_en']}; cross-layer collection and causal correlation can weaken this stealth effect.\""
    if old not in text:
        raise SystemExit("expected mechanism template not found")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> None:
    integration.mechanism = natural_mechanism
    integration.write_techniques("review")
    integration.write_handoffs()
    repair_generator_source()


if __name__ == "__main__":
    main()
