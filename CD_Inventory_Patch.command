#!/bin/bash

# Crimson Desert Mac Inventory Patcher
# Created for Cherry's Naver Cafe

clear
echo "==============================================="
echo "   붉은사막 인벤토리 확장 패치 (Mac 네이티브용)"
echo "   대상: 기본 200칸 / 최대 240칸 확장"
echo "==============================================="
echo ""

# 게임 경로 설정
TARGET_PATH="$HOME/Library/Application Support/Steam/steamapps/common/Crimson Desert/CrimsonDesert_Steam.app/Contents/Resources/packages/0008/0.paz"
APP_PATH="$HOME/Library/Application Support/Steam/steamapps/common/Crimson Desert/CrimsonDesert_Steam.app"

if [ ! -f "$TARGET_PATH" ]; then
    echo "❌ 오류: 게임 파일을 찾을 수 없습니다."
    echo "스팀 기본 경로에 게임이 설치되어 있는지 확인해주세요."
    exit 1
fi

echo "1. 원본 파일 백업 중..."
cp "$TARGET_PATH" "$TARGET_PATH.bak"
echo "✅ 백업 완료: 0.paz.bak"

echo "2. 인벤토리 데이터 패치 중..."
python3 -c "
import os
path = '$TARGET_PATH'
sig = b'\x02\x00\x09\x00\x00\x00Character\x00\x01'
with open(path, 'r+b') as f:
    data = f.read()
    off = data.find(sig)
    if off != -1:
        f.seek(off + 17)
        f.write(b'\xc8\x00\xf0\x00')
        print('✅ 데이터 수정 성공!')
    else:
        print('❌ 오류: 데이터를 찾을 수 없습니다.')
"

echo "3. macOS 보안 격리 해제 중 (비밀번호 입력 필요)..."
sudo xattr -cr "$APP_PATH"

echo ""
echo "==============================================="
echo "   🎉 패치가 완료되었습니다! 게임을 실행하세요."
echo "==============================================="
read -p "아무 키나 누르면 종료됩니다..."