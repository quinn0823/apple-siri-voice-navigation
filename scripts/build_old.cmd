@REM Apple Siri Voice Navigation
@REM The MIT License (MIT)
@REM Copyright (c) 2025 Jonathan Chiu

@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

for %%i in ("..") do set mod_name=%%~nxi

set packer_rel=..\..\..\Tools\scs_packer\scs_packer.exe
set source_rel=source
set build_rel=build

for %%i in ("%packer_rel%") do set packer_abs=%%~fi
for %%i in ("%source_rel%") do set source_abs=%%~fi
for %%i in ("%build_rel%") do set build_abs=%%~fi

echo [INFO] 检查 scs_packer
if exist "%packer_rel%" (
    echo [INFO] scs_packer: "%packer_rel%"
) else (
    echo [ERRO] 未找到 scs_packer
    pause
    exit /b 1
)

echo.

echo [INFO] 检查 source 文件夹
if exist "%source_rel%" (
    echo [INFO] source 文件夹: "%source_rel%"
) else (
    echo [ERRO] 未找到 source 文件夹
    pause
    exit /b 1
)

echo.

echo [INFO] 检查 build 文件夹
if exist "%build_rel%" (
    echo [INFO] build 文件夹: "%build_rel%" & echo [INFO] 清理 build 文件夹
    rmdir /s /q "%build_rel%"
    if errorlevel 1 (
        echo [ERRO] 无法清理 build 文件夹
        pause
        exit /b 1
    )
) else (
    echo [INFO] 未找到 build 文件夹
)

echo [INFO] 创建 build 文件夹
mkdir "%build_rel%"
if errorlevel 1 (
    echo [ERRO] 无法创建 build 文件夹
    pause
    exit /b 1
) else (
    echo [INFO] build 文件夹: "%build_rel%"
)

echo [INFO] 创建 workshop 文件夹
mkdir "%build_rel%\workshop"
if errorlevel 1 (
    echo [ERRO] 无法创建 workshop 文件夹
    pause
    exit /b 1
) else (
    echo [INFO] workshop 文件夹: "%build_rel%\workshop"
)

echo [INFO] 创建 standard 文件夹
mkdir "%build_rel%\standard"
if errorlevel 1 (
    echo [ERRO] 无法创建 standard 文件夹
    pause
    exit /b 1
) else (
    echo [INFO] standard 文件夹: "%build_rel%\standard"
)

echo.

echo [INFO] 创建 versions.sii
(
    echo SiiNunit {
) > "%build_rel%\workshop\versions.sii"
if errorlevel 1 (
    echo [ERRO] 无法创建 versions.sii
    pause
    exit /b 1
) else (
    echo [INFO] versions.sii: "%build_rel%\workshop\versions.sii"
)

for /d %%i in ("%source_rel%\*") do (
    echo.

    set current_pack_name=%%~nxi
    set current_pack_path=%%i

    echo [INFO] 打开 !current_pack_name! 文件夹: "!current_pack_path!" & echo [INFO] 创建 Workshop 版本 & echo [INFO] 创建 !current_pack_name! 文件夹
    mkdir "%build_rel%\workshop\!current_pack_name!"
    if errorlevel 1 (
        echo [ERRO] 无法创建 !current_pack_name! 文件夹
        pause
        exit /b 1
    ) else (
        echo [INFO] !current_pack_name! 文件夹: "%build_rel%\workshop\!current_pack_name!"
    )

    echo [INFO] 追加 versions.sii
    (
        echo     package_version_info : .!current_pack_name! {
        echo         package_name: "!current_pack_name!"
        echo     }
    ) >> "%build_rel%\workshop\versions.sii"
    if errorlevel 1 (
        echo [ERRO] 无法追加 versions.sii
        pause
        exit /b 1
    ) else (
        echo [INFO] versions.sii: "%build_rel%\workshop\versions.sii"
    )

    for %%j in ("!current_pack_path!\*") do (
        set current_file_name=%%~nxj
        set current_file_path=%%j

        echo [INFO] 复制 !current_file_name!
        copy "!current_file_path!" "%build_rel%\workshop\!current_pack_name!\!current_file_name!" > nul
        if errorlevel 1 (
            echo [ERRO] 无法复制 !current_file_name!
        ) else (
            echo [INFO] !current_file_name!: "%build_rel%\workshop\!current_pack_name!\!current_file_name!"
        )
    )

    for /d %%j in ("!current_pack_path!\*") do (
        set current_data_name=%%~nxj
        set current_data_path=%%j
        set workshop_build_path=%build_rel%\workshop\!current_pack_name!

        echo [INFO] 创建 !current_data_name!.scs & echo [INFO] 运行 scs_packer
        "%packer_rel%" create "!workshop_build_path!\!current_data_name!.scs" -root "!current_data_path!"
        if errorlevel 1 (
            echo [WARN] 无法创建 !current_data_name!.scs
            set errorlevel=0
        ) else (
            echo [INFO] !current_data_name!.scs: "!workshop_build_path!\!current_data_name!.scs"
        )
    )

    echo [INFO] 创建 Standard 版本 & echo [INFO] 创建 %mod_name%-!current_pack_name!.zip & echo [INFO] 运行 7-zip
    cd !current_pack_path!
    "C:\Program Files\7-Zip\7z.exe" a "..\..\%build_rel%\standard\%mod_name%-!current_pack_name!.zip" *
    if errorlevel 1 (
        echo [ERRO] 无法创建 %mod_name%-!current_pack_name!.zip
        pause
        exit /b 1
    ) else (
        echo [INFO] %mod_name%-!current_pack_name!.zip: "%build_rel%\standard\!current_pack_name!.zip"
    )
    cd ..\..
)

echo.

echo [INFO] 追加 versions.sii
>> "%build_rel%\workshop\versions.sii" (
    @REM echo     /* ^(C^) 2025 Quinn Qiu All rights reserved. */
    echo }
)
if errorlevel 1 (
    echo [ERRO] 无法追加 versions.sii
    pause
    exit /b 1
) else (
    echo [INFO] versions.sii: "%build_rel%\workshop\versions.sii"
)

echo.

echo [INFO] 检查 versions.sii
if exist "%build_rel%\workshop\versions.sii" (
    echo [INFO] 找到 versions.sii: "%build_rel%\workshop\versions.sii"
) else (
    echo [ERRO] 未找到 versions.sii
    pause
    exit /b 1
)

echo.

echo [INFO] 检查 build 文件夹
if exist "%build_rel%" (
    echo [INFO] build 文件夹: "%build_rel%"
    tree "%build_rel%" /f
) else (
    echo [ERRO] 未找到 build 文件夹
    pause
    exit /b 1
)

echo.

echo [INFO] 运行完成

pause