@echo off
REM KRİTİK KOMUT: BAT DOSYASININ BULUNDUĞU DİZİNE GEÇ
cd /d "%~dp0"
color 0F
CHCP 65001 > NUL
title Türk Lirası Bankot Tanıma Sistemi

python turk_lirasi_bankot.py
pause


