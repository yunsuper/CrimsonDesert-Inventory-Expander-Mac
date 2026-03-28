# Crimson Desert Inventory Expander for macOS (Native/Steam)
이 스크립트는 macOS 환경에서 **붉은사막(Crimson Desert)**의 인벤토리 슬롯을 확장해주는 네이티브 패치 도구입니다.

## 🚀 주요 기능
* 즉시 확장: 기본 인벤토리 50칸 → 200칸으로 즉시 변경
* 최대 확장: 게임 내 시스템 안정성을 고려한 최적 수치인 240칸 적용
* 안전한 패치: 원본 파일(0.paz) 자동 백업 생성 (0.paz.bak)
* 보안 해제: macOS 특유의 '손상된 파일' 또는 '보안 격리' 오류 자동 해결 (xattr -cr)

## 🛠 설치 및 사용 방법
1. 파일 다운로드: 저장소에서 CD_Inventory_Patch.command 파일을 다운로드하고 압축을 풉니다.

2. 실행 권한 부여: 터미널에 아래 명령어를 입력합니다. (맨 끝에 한 칸 띄워주세요)
```bash
chmod +x
```

3. 드래그 앤 드롭: 위 명령어를 입력한 상태에서 다운로드한 CD_Inventory_Patch.command 파일을 터미널 창으로 드래그한 뒤 **엔터(Enter)**를 누릅니다.
 
4. 패치 실행: 이제 해당 파일을 더블 클릭하여 실행합니다.

5. 비밀번호 입력: 중간에 Password: 문구가 뜨면 맥 로그인 비밀번호를 입력하고 엔터를 누르세요. (입력 시 글자가 보이지 않는 것이 정상이니 끝까지 치고 엔터를 누르시면 됩니다.)

## ⚠️ 주의사항
* 게임 종료: 반드시 게임이 완전히 종료된 상태에서 실행해야 합니다.

* 설치 경로: 스팀 기본 설치 경로(~/Library/Application Support/Steam/...)를 기준으로 작동합니다. 경로가 다를 경우 스크립트 내 TARGET_PATH를 직접 수정해야 합니다.

* 업데이트 대응: 게임 업데이트 후 인벤토리가 초기화되면 패치를 다시 한 번 실행해 주세요.

## ⚖️ 라이선스 (License)
이 프로젝트는 MIT License에 따라 배포됩니다.

제작: yunsuper (GitHub) / yunsuper1 (NexusMods)

Nexus Mods Page: [Mod#56](https://www.nexusmods.com/crimsondesert/mods/56)

---

This script is a native patching tool designed to expand inventory slots for Crimson Desert on macOS.

## 🚀 Key Features
* Instant Expansion: Increases base inventory from 50 to 200 slots immediately.
* Maximum Capacity: Optimized to 240 slots for maximum game stability.
* Safe Patching: Automatically creates a backup of the original file (0.paz.bak).
* Security Bypass: Automatically resolves macOS-specific "App is damaged" or "Quarantine" errors (xattr -cr).

## 🛠 Installation and How to Use
1. Download: Download the CD_Inventory_Patch.command file from the repository and unzip it.

2. Grant Execution Permission: Open the Terminal and type the following command (make sure to include a space at the end):
 ```bash
chmod +x
```

3. Drag & Drop: Drag the downloaded CD_Inventory_Patch.command file into the Terminal window and press Enter.

4. Run the Patch: Now, double-click the file to execute it.

5. Enter Password: When prompted for a Password:, type your macOS login password and press Enter. (Note: Characters will not be displayed while typing; this is normal—just type it out and hit Enter.)


## ⚠️ Important Notes
* Close the Game: Ensure the game is completely closed before running the patch.

* Installation Path: This script is configured for the default Steam installation path (~/Library/Application Support/Steam/...). If you have installed the game in a custom location, you must manually edit the TARGET_PATH inside the script.

* Post-Update: If an official game update resets your inventory, simply run this patch again.

## Gemini의 응답
작성하신 한글 README 내용의 톤과 구성을 그대로 살려, 외국 유저들도 쉽게 이해할 수 있도록 정리한 영어 버전입니다.

Crimson Desert Inventory Expander for macOS (Native/Steam)
This script is a native patching tool designed to expand inventory slots for Crimson Desert on macOS.

🚀 Key Features
* **Instant Expansion**: Increases base inventory from 50 to 200 slots immediately.
* **Maximum Capacity**: Optimized to 240 slots for maximum game stability.
* **Safe Patching**: Automatically creates a backup of the original file (0.paz.bak).
* **Security Bypass**: Automatically resolves macOS-specific "App is damaged" or "Quarantine" errors (xattr -cr).

🛠 Installation & How to Use
1. **Download**: Download the CD_Inventory_Patch.command file from the repository and unzip it.

2. **Grant Execution Permission**: Open the Terminal and type the following command (make sure to include a space at the end):

   ```bash
   chmod +x 
   ```

3. **Drag & Drop**: Drag the downloaded CD_Inventory_Patch.command file into the Terminal window and press Enter.

4. **Run the Patch**: Now, double-click the file to execute it.

5. **Enter Password**: When prompted for a Password:, type your macOS login password and press Enter. (Note: Characters will not be displayed while typing; this is normal—just type it out and hit Enter.)

## ⚠️ Important Notes
* <b>Close the Game</b>: Ensure the game is completely closed before running the patch.

* <b>Installation Path</b>: This script is configured for the default Steam installation path (~/Library/Application Support/Steam/...). If you have installed the game in a custom location, you must manually edit the <b>TARGET_PATH</b> inside the script.

* <b>Post-Update</b>: If an official game update resets your inventory, simply run this patch again.

⚖️ License
This project is distributed under the MIT License.

Created by: yunsuper (GitHub) / yunsuper1 (NexusMods)

Nexus Mods Page: [Mod#56](https://www.nexusmods.com/crimsondesert/mods/56)

