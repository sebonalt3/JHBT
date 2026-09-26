# 지후배틀

웹에서 플레이: https://wwwsebon-cloud.github.io/JHBT/

`index.html` 하나로 실행됩니다. 화면·게임 흐름·전투·캐릭터 수치(`CHARACTER_BALANCE`)·초상화(`PORTRAITS`, base64)·Firebase 설정·패치노트(`PATCH_NOTES`)가 모두 이 파일 안에 있습니다. 빌드 과정은 없습니다.

## 파일

- `index.html` — 게임 전체
- `firestore.rules` — Firestore 보안 규칙. Firebase 콘솔 → Firestore Database → 규칙에 전체를 붙여넣어 게시합니다.

## 릴리스

버전을 올릴 때는 `index.html`의 네 곳을 함께 바꿉니다: `<title>`, 로비 배지(`lobby-badge`), 로비 패치 버튼(`btnLobbyPatch`), `PATCH_NOTES`의 최신 항목.

## 온라인 기능

Firebase 프로젝트 `jihoobattle`의 이메일/비밀번호 인증과 Firestore를 사용합니다. 닉네임과 비밀번호(6~32자)로 계정을 만들면 8자리 UID가 배정되고, 다른 기기에서는 UID와 비밀번호로 로그인해 백업을 복원합니다. 3.0 시절 4자리 UID 계정은 32자 복구 키를 비밀번호로 써서 로그인할 수 있습니다. 비밀번호 재설정 수단은 없습니다.

웹 API 키는 공개 클라이언트 설정입니다. 리더보드 수치는 클라이언트가 올리므로 조작을 막지는 못합니다.
