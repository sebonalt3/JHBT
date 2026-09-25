"""지후배틀 릴레이 작업용 배포 빌드: 전체 ZIP과 단일 HTML을 생성한다."""

import base64
import mimetypes
import re
import sys
import zipfile
from pathlib import Path


SOURCE = Path(__file__).resolve().parent
SCRIPTS = ("character-balance.js", "firebase-config.js", "firebase-online.js")


def build(output: Path) -> None:
    if output == SOURCE:
        raise ValueError("산출물 폴더는 게임 소스 폴더와 달라야 합니다")
    output.mkdir(parents=True, exist_ok=True)
    html = (SOURCE / "index.html").read_text(encoding="utf-8")

    for name in SCRIPTS:
        tag = f'<script src="{name}"></script>'
        if html.count(tag) != 1:
            raise ValueError(f"스크립트 태그를 정확히 한 번 찾아야 합니다: {name}")
        code = (SOURCE / name).read_text(encoding="utf-8")
        code = re.sub(r"</script", r"<\\/script", code, flags=re.IGNORECASE)
        html = html.replace(tag, f"<script>\n{code}\n</script>")

    paths = set(re.findall(r"portraits/[A-Za-z0-9_.-]+\.(?:png|svg|jpg|jpeg|webp)", html))
    for path in sorted(paths):
        data = (SOURCE / path).read_bytes()
        media_type = mimetypes.guess_type(path)[0]
        if media_type is None:
            raise ValueError(f"이미지 형식을 알 수 없습니다: {path}")
        html = html.replace(path, f"data:{media_type};base64,{base64.b64encode(data).decode('ascii')}")

    if re.search(r"portraits/[A-Za-z0-9_.-]+\.(?:png|svg|jpg|jpeg|webp)", html):
        raise ValueError("단일 HTML에 외부 초상화 경로가 남아 있습니다")
    (output / "index.html").write_text(html, encoding="utf-8")

    with zipfile.ZipFile(output / "jihoo-battle-3.2.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(SOURCE.rglob("*")):
            if file.is_file() and output not in file.parents and "__pycache__" not in file.parts and file.name != ".DS_Store":
                archive.write(file, file.relative_to(SOURCE))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("사용법: python3 build-release.py <산출물 폴더>")
    build(Path(sys.argv[1]).resolve())
