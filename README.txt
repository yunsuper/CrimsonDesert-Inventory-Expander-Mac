====================================================================
 Crimson Desert - Mac Inventory Patcher v2.2.0
====================================================================
 Author: yunsuper1
 Based on original Windows script by kindiboy (v2.2.0)
 Target OS: macOS (including the latest Tahoe 26.3.1)
====================================================================

[🇰🇷 한국어 설명]
- 이 패치는 2026년 4월 4일 업데이트된 붉은사막의 최신 데이터 구조(LZ4 동적 오프셋)에 대응하는 맥(Mac) 네이티브 전용 패치입니다. (기본 180칸 / 최대 999칸)

✨ 맥 전용 특별 기능
- 경로 자동 탐색: 게임이 어디에 설치되어 있든 meta/0.papgt 파일을 스크립트가 스스로 찾아냅니다.
- 안전한 자동 백업: 패치 실행 시 원본 파일(.inventory_backup)을 자동 생성하여 문제 발생 시 언제든 복구가 가능합니다.

💡 필수 주의사항 (처음 1회만 진행)
다운로드 받은 .command 파일은 맥의 보안 정책상 바로 더블클릭하면 실행되지 않습니다. 반드시 아래 과정을 먼저 진행해 주세요.

1. patch_inventory_mac.py 와 CD_Inventory_Patch.command 파일을 같은 폴더에 다운로드 받습니다.
2. 맥에서 [터미널(Terminal)]을 실행합니다.
3. 터미널 창에 아래 명령어를 입력합니다. (맨 끝에 띄어쓰기 한 칸 필수!)
   chmod +x 
4. 다운받은 CD_Inventory_Patch.command 파일을 마우스로 클릭해서 터미널 창 안으로 드래그 앤 드롭한 뒤, 엔터(Return)를 칩니다.
5. 이제 터미널을 끄고, CD_Inventory_Patch.command 파일을 더블클릭하면 패치가 정상적으로 실행됩니다!
* 진행 중 맥 로그인 비밀번호를 요구할 수 있습니다. (Gatekeeper 보안 격리 해제용)


--------------------------------------------------------------------


[🇬🇧 English Instructions]
- This is a Mac-native patcher updated for the latest Crimson Desert (v2.2.0) data structure with LZ4 dynamic offset scanning. (180 Default / 999 Max slots) 

✨ Mac-Exclusive Features
- Auto Path Finder: Automatically locates the meta/0.papgt file regardless of your installation directory.
- Safe Auto-Backup: Automatically creates original backups (.inventory_backup) before patching for easy restoration.

💡 IMPORTANT: First-time setup (Execution Permission)
Due to macOS security policies, you cannot run the .command file immediately. You must grant execution permission first.

1. Download both 'patch_inventory_mac.py' and 'CD_Inventory_Patch.command' into the same folder.
2. Open the [Terminal] on your Mac.
3. Type the following command (make sure to include the space at the end!):
   chmod +x 
4. Drag and drop the 'CD_Inventory_Patch.command' file into the Terminal window, then press Enter (Return).
5. Close the Terminal. You can now double-click the 'CD_Inventory_Patch.command' file to run the patcher!
* It may ask for your Mac login password during the process. (This is to bypass Gatekeeper quarantine via xattr).

====================================================================