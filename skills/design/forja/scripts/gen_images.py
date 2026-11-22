#!/usr/bin/env python3
"""Gera as imagens de um pacote Forja com o Codex CLI do usuário (geração de imagem nativa do Codex).

Uso:
    python3 gen_images.py build/imagens/prompts.json build/imagens [--only hero,onboarding] [--max-width 1600]

prompts.json:
{
  "estilo": "fotografia editorial, luz natural de fim de tarde, ...",   # prefixo comum (direção de arte)
  "evitar": "sem texto, sem logos, sem marcas d'água, ...",            # sufixo comum
  "imagens": [
    {"id": "hero", "prompt": "mulher de 38 anos ...", "formato": "4:5", "alt": {"pt": "...", "en": "...", "de": "..."}}
  ]
}

Para cada imagem:
  1. roda `codex exec` pedindo a geração com a ferramenta de imagem e o arquivo salvo como <id>.png;
  2. se o Codex não salvar no lugar pedido, pega a imagem mais nova em ~/.codex/generated_images;
  3. converte para WebP (largura máxima configurável) e grava <id>.webp;
  4. registra prompt, formato e alt em manifest.json (para regerar ou trocar depois).

Requisitos: `codex` no PATH com login feito (`codex login` ou `codex login --device-auth`), Python 3.11+ e Pillow.
Nunca gere pessoas reais identificáveis, logos ou marcas de terceiros.
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys
import time

FORMATOS = {"1:1": "1024x1024", "4:5": "1024x1280", "3:4": "1024x1365", "9:16": "1024x1792", "16:9": "1792x1024", "3:2": "1536x1024", "2:3": "1024x1536"}


def newest_generated(since: float) -> pathlib.Path | None:
    base = pathlib.Path(os.environ.get("CODEX_HOME", pathlib.Path.home() / ".codex")) / "generated_images"
    if not base.exists():
        return None
    files = [p for p in base.rglob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"} and p.stat().st_mtime >= since]
    return max(files, key=lambda p: p.stat().st_mtime) if files else None


def gerar(item: dict, estilo: str, evitar: str, outdir: pathlib.Path, timeout: int) -> pathlib.Path:
    alvo = outdir / f"{item['id']}.png"
    tamanho = FORMATOS.get(item.get("formato", "1:1"), "1024x1024")
    prompt = (
        "Use your image generation tool to create exactly one image. Do not write code, do not use any other tool.\n"
        f"Size/aspect: {tamanho} ({item.get('formato', '1:1')}).\n"
        f"Image description: {estilo} {item['prompt']} {evitar}\n"
        f"Save the final image as {alvo.name} in the current working directory and reply only with the file name."
    )
    inicio = time.time() - 1
    cmd = ["codex", "exec", "--skip-git-repo-check", "-s", "workspace-write", "-C", str(outdir), prompt]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"codex exec falhou para {item['id']}: {r.stderr[-800:]}")
    if alvo.exists() and alvo.stat().st_mtime >= inicio:
        return alvo
    achado = newest_generated(inicio)
    if achado is None:
        raise RuntimeError(f"nenhuma imagem encontrada para {item['id']}; saída do codex: {r.stdout[-800:]}")
    alvo.write_bytes(achado.read_bytes())
    return alvo


def para_webp(png: pathlib.Path, max_width: int) -> pathlib.Path:
    from PIL import Image

    img = Image.open(png).convert("RGB")
    if img.width > max_width:
        img = img.resize((max_width, round(img.height * max_width / img.width)), Image.LANCZOS)
    out = png.with_suffix(".webp")
    img.save(out, "WEBP", quality=82, method=6)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("prompts")
    ap.add_argument("outdir")
    ap.add_argument("--only", default="")
    ap.add_argument("--max-width", type=int, default=1600)
    ap.add_argument("--timeout", type=int, default=420)
    a = ap.parse_args()

    spec = json.loads(pathlib.Path(a.prompts).read_text())
    outdir = pathlib.Path(a.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    so = {x for x in a.only.split(",") if x}
    manifest_path = outdir / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}

    erros = 0
    for item in spec["imagens"]:
        if so and item["id"] not in so:
            continue
        try:
            png = gerar(item, spec.get("estilo", ""), spec.get("evitar", ""), outdir, a.timeout)
            webp = para_webp(png, a.max_width)
            manifest[item["id"]] = {"arquivo": webp.name, "prompt": item["prompt"], "formato": item.get("formato", "1:1"), "alt": item.get("alt", {}), "gerado_em": time.strftime("%Y-%m-%d %H:%M")}
            print(f"ok  {item['id']} -> {webp}")
        except Exception as e:  # segue com as outras; o pacote usa o placeholder desta
            erros += 1
            print(f"ERRO {item['id']}: {e}", file=sys.stderr)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
