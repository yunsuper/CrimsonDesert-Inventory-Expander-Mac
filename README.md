# Crimson Desert Inventory Expander for macOS (Native/Steam) (v2.2.0)
이 도구는 **붉은사막(Crimson Desert)**의 최신 업데이트(LZ4 압축 구조 변경)에 대응하는 macOS 전용 인벤토리 확장 패치입니다.

## 🚀 업데이트 주요 사항 (v2.2.0)
* **최신 패치 대응**: 2026년 4월 4일 업데이트된 붉은사막의 최신 데이터 구조(LZ4 동적 오프셋)에 대응하는 맥(Mac) 네이티브 전용 패치입니다.
* **안정성 최적화**: 기본 확장 칸수를 180칸으로 조정하여 게임 내 상호작용 버그를 방지했습니다. (최대 999칸 지원)
* **상호작용 버그 수정 & 퀘스트 보상 보호**: 인벤토리 확장으로 인해 발생할 수 있는 상호작용 버그를 해결하고, 인벤토리가 너무 높으면 시스템이 가방 확장 퀘스트 보상을 누락시키는 문제를 해결했습니다.
* **안전한 패치**: 원본 파일(0.paz) 자동 백업 생성 (0.paz.inventory_backup)
* **경로 자동 탐색 & 보안 해제**: 스크립트가 스스로 `0.papgt`의 위치를 찾아내며, macOS 특유의 '손상된 파일' 오류(Gatekeeper 격리)를 자동으로 해제(`xattr -cr`)합니다.

## 🛠 설치 및 사용 방법
1. **파일 준비**:` patch_inventory_mac.py`와 `CD_Inventory_Patch.command` 파일을 같은 폴더에 다운로드합니다.
   
2. **권한 부여**: [터미널(Terminal)]을 열고 아래 명령어를 입력합니다. (끝에 한 칸 띄워주세요)
```bash
chmod +x
```

3. **드래그 앤 드롭**: 위 명령어를 입력한 상태에서 CD_Inventory_Patch.command 파일을 터미널 창으로 드래그한 뒤 **엔터(Enter)**를 누릅니다.
   
4. **패치 실행**: 이제 터미널을 닫고, 해당 파일을 더블 클릭하여 실행합니다.
   
5. **완료**: 패치 프로세스가 진행되며 [프로세스 완료됨] 문구가 뜨면 창을 닫고 게임을 실행하세요.<br>
*참고: 실행 중 맥 비밀번호를 요구할 수 있습니다. 입력 시 글자가 보이지 않는 것은 정상입니다.*

## ⚠️ 주의사항
* **게임 종료**: 반드시 게임이 완전히 종료된 상태에서 실행해야 합니다.

* **설치 경로**: 스팀 기본 설치 경로(~/Library/Application Support/Steam/...)를 기준으로 작동합니다. 경로가 다를 경우 스크립트 내 TARGET_PATH를 직접 수정해야 합니다.

* **업데이트 대응**: 게임 업데이트 후 인벤토리가 초기화되면 패치를 다시 한 번 실행해 주세요.

## ⚖️ 라이선스 (License)
이 프로젝트는 MIT License에 따라 배포됩니다.

제작: yunsuper (GitHub) / yunsuper1 (NexusMods)

Nexus Mods Page: [Mod#56](https://www.nexusmods.com/crimsondesert/mods/56)

---

This script is a native patching tool designed to expand inventory slots for Crimson Desert on macOS.

## 🚀 Key Features & Updates (v2.2.0)
* **Latest Patch Support**: Fully compatible with the new LZ4 compression structure and dynamic offsets from the April 4, 2026 update.
* **Stability Optimization**: Default inventory set to 180 slots to prevent in-game interaction bugs. (Supports up to 999 slots)
* **Bug Fixes & Reward Protection**: Fixed interaction issues with objects (candles/braziers) and prevented quest reward (inventory expansion) skips caused by excessive slot counts.
* **Safe Patching**: Automatically creates a backup of the original file (0.paz.inventory_backup).
* **Auto Path-Finder & Security Bypass**: The script dynamically locates 0.papgt and automatically resolves macOS-specific "App is damaged" or Quarantine errors (xattr -cr).

## 🛠 Installation and How to Use
1. **Prepare Files**: Download both `patch_inventory_mac.py` and `CD_Inventory_Patch.command` filesinto the same folder.

2. **Grant Permission**: Open Terminal and type the following command (ensure there is a space at the end):
 ```bash
chmod +x
```

3. **Drag & Drop**: Drag the CD_Inventory_Patch.command file into the Terminal window and press Enter.

4. **Execute**: Close the Terminal and double-click the .command file to run the patcher.

5. **Finish**: Once you see [Process Completed], close the window and launch the game.<br>
*Note: You may be prompted for your macOS password. It is normal for characters not to appear while typing.*

## ⚠️ Important Notes
* **Close the Game**: Ensure the game is completely closed before running the patch.

* **Installation Path**: Configured for the default Steam path. If using a custom path, manually edit TARGET_PATH in the script.

* **Post-Update**: If an official game update resets your inventory, simply run this patch again.


## ⚖️ License
This project is distributed under the MIT License.

Created by: yunsuper (GitHub) / yunsuper1 (NexusMods)

Nexus Mods Page: [Mod#56](https://www.nexusmods.com/crimsondesert/mods/56)

