# github-profile

README de perfil de GitHub: una sola imagen pixel-art **animada** (`assets/readme.gif`),
generada por código con Python + Pillow a partir de sprites del personaje.

## Estructura
```
README.md            el perfil (va en el repo gabrielurs/gabrielurs)
assets/
  readme.gif         LA imagen (título + retrato bebiendo + ARSENAL + DUNGEONS + bosque top-down)
  readme.png         primer frame, estático (fallback)
scripts/
  build_readme.py    genera readme.gif + readme.png   <- el único script vivo
sprites/             pixel-art del personaje (fuente, generado con IA)
  run-east.gif       ciclo de carrera (6 frames) -> el que corre por el bosque
  drink-south.gif    animación bebiendo -> el retrato grande (chill)
  east/west/north... stills direccionales (no usados ahora, se guardan por si acaso)
_archive/            direcciones anteriores descartadas (póster HLD, banner, panel…) — borrables
```

## Regenerar
```bash
python3 scripts/build_readme.py
```
Requiere Python 3 + Pillow (`pip install pillow`) y fuentes DejaVu del sistema.
Todo (fondo, marco, paneles, texto, bosque animado) se dibuja por código; el
personaje sale de los GIFs de `sprites/`. Cambiar el sprite = cambiar el GIF y re-generar.

## Qué anima
- Retrato central: el personaje **bebiendo** (loop lento, chill).
- Banda inferior: bosque **top-down** con el personaje **corriendo** por un camino,
  árboles con parallax (scroll seamless) y luciérnagas.
- El resto del card es estático (para que el GIF pese poco).

## Publicar
Sale en tu perfil si el repo se llama igual que tu usuario: **`gabrielurs/gabrielurs`**.
```bash
cd /home/it/personal/github-profile
git init && git add -A && git commit -m "pixel-art profile"
# gh repo create gabrielurs --public --source=. --push
```

## Pendiente / notas
- Email: en `README.md` está `gabrielurscoste@gmail.com` — cámbialo si prefieres el profesional.
- `_archive/` se puede borrar entero cuando quieras.
