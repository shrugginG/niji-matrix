from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
path = ROOT.parent / "tool/niji-matrix-review/test/repository.test.mjs"
text = path.read_text(encoding="utf-8")

replacements = {
    '  assert.equal(snapshot.stats.technique, 40);\n  assert.equal(snapshot.stats["evasion-subtechnique"], 92);\n  assert.equal(snapshot.stats["detection-strategy"], 33);\n  assert.equal(snapshot.stats["detection-analytic"], 35);\n  assert.equal(snapshot.stats.mitigation, 31);':
    '  assert.equal(snapshot.stats.technique, 50);\n  assert.equal(snapshot.stats["evasion-subtechnique"], 113);\n  assert.equal(snapshot.stats["detection-strategy"], 36);\n  assert.equal(snapshot.stats["detection-analytic"], 41);\n  assert.equal(snapshot.stats.mitigation, 33);',
    '    ["NJT-0071", 3],\n    ["NJT-0072", 2],':
    '    ["NJT-0071", 3],\n    ["NJT-0072", 2],\n    ["NJT-0073", 2],\n    ["NJT-0074", 3],\n    ["NJT-0075", 2],\n    ["NJT-0076", 2],\n    ["NJT-0077", 2],\n    ["NJT-0078", 2],\n    ["NJT-0079", 2],\n    ["NJT-0080", 2],\n    ["NJT-0081", 2],\n    ["NJT-0082", 2],',
    '  assert.deepEqual(snapshot.objects["DET-000058"].analytic_refs, ["NJA-000032", "NJA-000033"]);\n  assert.equal(snapshot.objects["NJA-000032"].strategy_ref, "DET-000058");\n  assert.equal(snapshot.objects["NJA-000033"].strategy_ref, "DET-000058");':
    '  assert.deepEqual(snapshot.objects["DET-000058"].analytic_refs, ["NJA-000032", "NJA-000033", "NJA-000037"]);\n  assert.equal(snapshot.objects["NJA-000032"].strategy_ref, "DET-000058");\n  assert.equal(snapshot.objects["NJA-000033"].strategy_ref, "DET-000058");\n  for (const [strategyId, analyticIds] of [\n    ["DET-000061", ["NJA-000039"]],\n    ["DET-000062", ["NJA-000040"]],\n    ["DET-000063", ["NJA-000041", "NJA-000042"]],\n  ]) {\n    assert.deepEqual(snapshot.objects[strategyId].analytic_refs, analyticIds);\n    for (const analyticId of analyticIds) {\n      const analytic = snapshot.objects[analyticId];\n      assert.equal(analytic.strategy_ref, strategyId);\n      assert.ok(analytic.data_requirements.length > 0);\n      assert.ok(analytic.observables.length > 0);\n    }\n  }',
    '    ["NJT-0063", "NJT-0064", "NJT-0065", "NJT-0066", "NJT-0067", "NJT-0068", "NJT-0069", "NJT-0070", "NJT-0071", "NJT-0072"],':
    '    ["NJT-0063", "NJT-0064", "NJT-0065", "NJT-0066", "NJT-0067", "NJT-0068", "NJT-0069", "NJT-0070", "NJT-0071", "NJT-0072", "NJT-0073", "NJT-0074", "NJT-0075", "NJT-0076", "NJT-0077", "NJT-0078", "NJT-0079", "NJT-0080", "NJT-0081", "NJT-0082"],',
    '  assert.ok(data.objects["NJA-000036"]);':
    '  assert.ok(data.objects["NJA-000036"]);\n  assert.ok(data.objects["NJA-000042"]);',
}

for old, new in replacements.items():
    if old not in text:
        raise SystemExit(f"expected test fixture block not found: {old[:80]}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
