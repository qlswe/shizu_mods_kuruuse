#     /$$   /$$ /$$   /$$ /$$$$$$$  /$$   /$$ /$$   /$$  /$$$$$$  /$$$$$$$$      /$$$$$$$
#    | $$  /$$/| $$  | $$| $$__  $$| $$  | $$| $$  | $$ /$$__  $$| $$_____/     | $$__  $$
#    | $$ /$$/ | $$  | $$| $$  \ $$| $$  | $$| $$  | $$| $$  \__/| $$           | $$  \ $$
#    | $$$$$/  | $$  | $$| $$$$$$$/| $$  | $$| $$  | $$|  $$$$$$ | $$$$$ /$$$$$$| $$$$$$$/
#    | $$  $$  | $$  | $$| $$__  $$| $$  | $$| $$  | $$ \____  $$| $$__/|______/| $$____/
#    | $$\  $$ | $$  | $$| $$  \ $$| $$  | $$| $$  | $$ /$$  \ $$| $$           | $$
#    | $$ \  $$|  $$$$$$/| $$  | $$|  $$$$$$/|  $$$$$$/|  $$$$$$/| $$$$$$$$     | $$
#    |__/  \__/ \______/ |__/  |__/ \______/  \______/  \______/ |________/     |__/


# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/shizu_mods_kuruuse

import platform
import psutil

from pyrogram import Client, types
from .. import loader, utils

@loader.module("SysInfo", "Kuruuse-P", 1.0)
class SysInfo(loader.Module):
    """Module to retrieve and display system information and characteristics. Supports premium stickers via config."""

    def __init__(self):
        self.config = loader.ModuleConfig(
            "sticker_id", None, lambda: "Sticker file_id to send with each response (premium or regular)"
        )

    strings = {
        "sys_info": "🖥️ System Information:\n- OS: {os}\n- Architecture: {arch}\n- Processor: {proc}\n- Python Version: {py_ver}",
        "cpu_info": "🧠 CPU Usage:\n- Current Usage: {usage}%\n- Cores: {cores} (Physical: {phys_cores})",
        "mem_info": "🧮 Memory Usage:\n- Total: {total} MB\n- Used: {used} MB\n- Free: {free} MB\n- Usage: {percent}%",
        "swap_info": "🔄 Swap Usage:\n- Total: {total} MB\n- Used: {used} MB\n- Free: {free} MB\n- Usage: {percent}%",
        "disk_info": "💽 Disk Usage:\n- Total: {total} GB\n- Used: {used} GB\n- Free: {free} GB\n- Usage: {percent}%",
        "permission_error": "❌ Permission denied. This command requires access to system files (/proc/*), which might not be available in your environment (e.g., Termux on Android without proper permissions or root).",
        "general_error": "❌ An error occurred: {error}",
        "invalid_path": "❌ Invalid path: {path}",
    }

    strings_ru = {
        "sys_info": "🖥️ Информация о системе:\n- ОС: {os}\n- Архитектура: {arch}\n- Процессор: {proc}\n- Версия Python: {py_ver}",
        "cpu_info": "🧠 Использование CPU:\n- Текущее использование: {usage}%\n- Ядра: {cores} (Физические: {phys_cores})",
        "mem_info": "🧮 Использование памяти:\n- Всего: {total} МБ\n- Использовано: {used} МБ\n- Свободно: {free} МБ\n- Использование: {percent}%",
        "swap_info": "🔄 Использование swap:\n- Всего: {total} МБ\n- Использовано: {used} МБ\n- Свободно: {free} МБ\n- Использование: {percent}%",
        "disk_info": "💽 Использование диска:\n- Всего: {total} ГБ\n- Использовано: {used} ГБ\n- Свободно: {free} ГБ\n- Использование: {percent}%",
        "permission_error": "❌ Отказано в доступе. Эта команда требует доступа к системным файлам (/proc/*), который может быть недоступен в вашей среде (например, Termux на Android без соответствующих разрешений или root).",
        "general_error": "❌ Произошла ошибка: {error}",
        "invalid_path": "❌ Неверный путь: {path}",
    }

    strings_kz = {
        "sys_info": "🖥️ Жүйе туралы ақпарат:\n- ОС: {os}\n- Архитектура: {arch}\n- Процессор: {proc}\n- Python нұсқасы: {py_ver}",
        "cpu_info": "🧠 CPU пайдалану:\n- Қазіргі пайдалану: {usage}%\n- Ядролар: {cores} (Физикалық: {phys_cores})",
        "mem_info": "🧮 Жады пайдалану:\n- Барлығы: {total} МБ\n- Пайдаланылған: {used} МБ\n- Бос: {free} МБ\n- Пайдалану: {percent}%",
        "swap_info": "🔄 Swap пайдалану:\n- Барлығы: {total} МБ\n- Пайдаланылған: {used} МБ\n- Бос: {free} МБ\n- Пайдалану: {percent}%",
        "disk_info": "💽 Диск пайдалану:\n- Барлығы: {total} ГБ\n- Пайдаланылған: {used} ГБ\n- Бос: {free} ГБ\n- Пайдалану: {percent}%",
        "permission_error": "❌ Рұқсат жоқ. Бұл команда жүйе файлдарына (/proc/*) қол жеткізуді талап етеді, ол сіздің ортаңызда қолжетімді болмауы мүмкін (мысалы, Android-тегі Termux рұқсатсыз немесе root-сыз).",
        "general_error": "❌ Қате орын алды: {error}",
        "invalid_path": "❌ Жарамсыз жол: {path}",
    }

    strings_ua = {
        "sys_info": "🖥️ Інформація про систему:\n- ОС: {os}\n- Архітектура: {arch}\n- Процесор: {proc}\n- Версія Python: {py_ver}",
        "cpu_info": "🧠 Використання CPU:\n- Поточне використання: {usage}%\n- Ядра: {cores} (Фізичні: {phys_cores})",
        "mem_info": "🧮 Використання пам'яті:\n- Всього: {total} МБ\n- Використано: {used} МБ\n- Вільно: {free} МБ\n- Використання: {percent}%",
        "swap_info": "🔄 Використання swap:\n- Всього: {total} МБ\n- Використано: {used} МБ\n- Вільно: {free} МБ\n- Використання: {percent}%",
        "disk_info": "💽 Використання диска:\n- Всього: {total} ГБ\n- Використано: {used} ГБ\n- Вільно: {free} ГБ\n- Використання: {percent}%",
        "permission_error": "❌ Доступ заборонено. Це командування вимагає доступу до системних файлів (/proc/*), який може бути недоступним у вашому середовищі (наприклад, Termux на Android без належних дозволів або root).",
        "general_error": "❌ Виникла помилка: {error}",
        "invalid_path": "❌ Недійсний шлях: {path}",
    }

    strings_uz = {
        "sys_info": "🖥️ Tizim ma'lumotlari:\n- OS: {os}\n- Arxitektura: {arch}\n- Protsessor: {proc}\n- Python versiyasi: {py_ver}",
        "cpu_info": "🧠 CPU ishlatilishi:\n- Joriy ishlatilishi: {usage}%\n- Yadrolar: {cores} (Fizik: {phys_cores})",
        "mem_info": "🧮 Xotira ishlatilishi:\n- Jami: {total} MB\n- Ishlatilgan: {used} MB\n- Bo'sh: {free} MB\n- Ishlatilishi: {percent}%",
        "swap_info": "🔄 Swap ishlatilishi:\n- Jami: {total} MB\n- Ishlatilgan: {used} MB\n- Bo'sh: {free} MB\n- Ishlatilishi: {percent}%",
        "disk_info": "💽 Disk ishlatilishi:\n- Jami: {total} GB\n- Ishlatilgan: {used} GB\n- Bo'sh: {free} GB\n- Ishlatilishi: {percent}%",
        "permission_error": "❌ Ruxsat berilmadi. Ushbu buyruq tizim fayllariga (/proc/*) kirishga ruxsat talab qiladi, bu sizning muhitingizda mavjud bo'lmasligi mumkin (masalan, Android'dagi Termux'da to'g'ri ruxsatlar yoki rootsiz).",
        "general_error": "❌ Xatolik yuz berdi: {error}",
        "invalid_path": "❌ Noto'g'ri yo'l: {path}",
    }

    strings_jp = {
        "sys_info": "🖥️ システム情報:\n- OS: {os}\n- アーキテクチャ: {arch}\n- プロセッサ: {proc}\n- Python バージョン: {py_ver}",
        "cpu_info": "🧠 CPU 使用率:\n- 現在の使用率: {usage}%\n- コア: {cores} (物理: {phys_cores})",
        "mem_info": "🧮 メモリ使用量:\n- 合計: {total} MB\n- 使用中: {used} MB\n- 空き: {free} MB\n- 使用率: {percent}%",
        "swap_info": "🔄 スワップ使用量:\n- 合計: {total} MB\n- 使用中: {used} MB\n- 空き: {free} MB\n- 使用率: {percent}%",
        "disk_info": "💽 ディスク使用量:\n- 合計: {total} GB\n- 使用中: {used} GB\n- 空き: {free} GB\n- 使用率: {percent}%",
        "permission_error": "❌ 許可が拒否されました。このコマンドはシステムファイル (/proc/*) へのアクセスを必要とし、あなたの環境（例: Android の Termux で適切な許可や root なし）では利用できない可能性があります。",
        "general_error": "❌ エラーが発生しました: {error}",
        "invalid_path": "❌ 無効なパス: {path}",
    }

    strings_kr = {
        "sys_info": "🖥️ 시스템 정보:\n- OS: {os}\n- 아키텍처: {arch}\n- 프로세서: {proc}\n- 파이썬 버전: {py_ver}",
        "cpu_info": "🧠 CPU 사용량:\n- 현재 사용량: {usage}%\n- 코어: {cores} (물리적: {phys_cores})",
        "mem_info": "🧮 메모리 사용량:\n- 총계: {total} MB\n- 사용됨: {used} MB\n- 남음: {free} MB\n- 사용률: {percent}%",
        "swap_info": "🔄 스왑 사용량:\n- 총계: {total} MB\n- 사용됨: {used} MB\n- 남음: {free} MB\n- 사용률: {percent}%",
        "disk_info": "💽 디스크 사용량:\n- 총계: {total} GB\n- 사용됨: {used} GB\n- 남음: {free} GB\n- 사용률: {percent}%",
        "permission_error": "❌ 권한 거부됨. 이 명령은 시스템 파일 (/proc/*)에 대한 액세스를 필요로 하며, 귀하의 환경(예: 루트 권한 없이 Termux on Android)에서 사용할 수 없을 수 있습니다.",
        "general_error": "❌ 오류 발생: {error}",
        "invalid_path": "❌ 잘못된 경로: {path}",
    }

    def bytes_to_mb(self, bytes_size: int) -> float:
        """Convert bytes to megabytes"""
        return round(bytes_size / (1024 * 1024), 1)

    def bytes_to_gb(self, bytes_size: int) -> float:
        """Convert bytes to gigabytes"""
        return round(bytes_size / (1024 * 1024 * 1024), 1)

    async def send_sticker_if_configured(self, app: Client, message: types.Message):
        if self.config["sticker_id"]:
            try:
                await app.send_sticker(message.chat.id, self.config["sticker_id"], reply_to_message_id=message.id)
            except Exception:
                pass

    @loader.command()
    async def sysinfo(self, app: Client, message: types.Message):
        """Get general system information: .sysinfo"""
        try:
            sys_info = platform.uname()
            proc = sys_info.processor or "Unknown"
            if proc == "Unknown":
                try:
                    with open("/proc/cpuinfo", "r") as f:
                        for line in f:
                            if "model name" in line.lower():
                                proc = line.split(":", 1)[1].strip()
                                break
                except Exception:
                    pass
            await self.send_sticker_if_configured(app, message)
            await utils.answer(
                message,
                self.strings["sys_info"].format(
                    os=f"{sys_info.system} {sys_info.release}",
                    arch=sys_info.machine,
                    proc=proc,
                    py_ver=platform.python_version()
                )
            )
        except Exception as e:
            await utils.answer(
                message,
                self.strings["general_error"].format(error=str(e))
            )

    @loader.command()
    async def cpu(self, app: Client, message: types.Message):
        """Get CPU usage information: .cpu"""
        try:
            usage = psutil.cpu_percent(interval=0.1)
            cores = psutil.cpu_count(logical=True)
            phys_cores = psutil.cpu_count(logical=False)
            await self.send_sticker_if_configured(app, message)
            await utils.answer(
                message,
                self.strings["cpu_info"].format(
                    usage=usage,
                    cores=cores,
                    phys_cores=phys_cores
                )
            )
        except PermissionError:
            await utils.answer(message, self.strings["permission_error"])
        except Exception as e:
            await utils.answer(
                message,
                self.strings["general_error"].format(error=str(e))
            )

    @loader.command()
    async def mem(self, app: Client, message: types.Message):
        """Get memory usage information: .mem"""
        try:
            mem = psutil.virtual_memory()
            await self.send_sticker_if_configured(app, message)
            await utils.answer(
                message,
                self.strings["mem_info"].format(
                    total=self.bytes_to_mb(mem.total),
                    used=self.bytes_to_mb(mem.used),
                    free=self.bytes_to_mb(mem.free),
                    percent=mem.percent
                )
            )
        except PermissionError:
            await utils.answer(message, self.strings["permission_error"])
        except Exception as e:
            await utils.answer(
                message,
                self.strings["general_error"].format(error=str(e))
            )

    @loader.command()
    async def swap(self, app: Client, message: types.Message):
        """Get swap usage information: .swap"""
        try:
            swap = psutil.swap_memory()
            await self.send_sticker_if_configured(app, message)
            await utils.answer(
                message,
                self.strings["swap_info"].format(
                    total=self.bytes_to_mb(swap.total),
                    used=self.bytes_to_mb(swap.used),
                    free=self.bytes_to_mb(swap.free),
                    percent=swap.percent
                )
            )
        except PermissionError:
            await utils.answer(message, self.strings["permission_error"])
        except Exception as e:
            await utils.answer(
                message,
                self.strings["general_error"].format(error=str(e))
            )

    @loader.command()
    async def disk(self, app: Client, message: types.Message):
        """Get disk usage information: .disk [path]"""
        args = utils.get_args_raw(message)
        path = args or "/"
        try:
            disk = psutil.disk_usage(path)
            await self.send_sticker_if_configured(app, message)
            await utils.answer(
                message,
                self.strings["disk_info"].format(
                    total=self.bytes_to_gb(disk.total),
                    used=self.bytes_to_gb(disk.used),
                    free=self.bytes_to_gb(disk.free),
                    percent=disk.percent
                )
            )
        except FileNotFoundError:
            await utils.answer(
                message,
                self.strings["invalid_path"].format(path=path)
            )
        except PermissionError:
            await utils.answer(message, self.strings["permission_error"])
        except Exception as e:
            await utils.answer(
                message,
                self.strings["general_error"].format(error=str(e))
            )

    @loader.command(aliases=["sysall"])
    async def allinfo(self, app: Client, message: types.Message):
        """Get all system information in one go: .allinfo [disk_path]"""
        reply = ""
        args = utils.get_args_raw(message)
        path = args or "/"

        await self.send_sticker_if_configured(app, message)

        try:
            sys_info = platform.uname()
            proc = sys_info.processor or "Unknown"
            if proc == "Unknown":
                try:
                    with open("/proc/cpuinfo", "r") as f:
                        for line in f:
                            if "model name" in line.lower():
                                proc = line.split(":", 1)[1].strip()
                                break
                except Exception:
                    pass
            reply += self.strings["sys_info"].format(
                os=f"{sys_info.system} {sys_info.release}",
                arch=sys_info.machine,
                proc=proc,
                py_ver=platform.python_version()
            ) + "\n\n"
        except Exception as e:
            reply += self.strings["general_error"].format(error=str(e)) + "\n\n"

        # CPU Info
        try:
            usage = psutil.cpu_percent(interval=0.1)
            cores = psutil.cpu_count(logical=True)
            phys_cores = psutil.cpu_count(logical=False)
            reply += self.strings["cpu_info"].format(
                usage=usage,
                cores=cores,
                phys_cores=phys_cores
            ) + "\n\n"
        except Exception:
            pass

        # Memory Info
        try:
            mem = psutil.virtual_memory()
            reply += self.strings["mem_info"].format(
                total=self.bytes_to_mb(mem.total),
                used=self.bytes_to_mb(mem.used),
                free=self.bytes_to_mb(mem.free),
                percent=mem.percent
            ) + "\n\n"
        except Exception:
            pass

        # Swap Info
        try:
            swap = psutil.swap_memory()
            reply += self.strings["swap_info"].format(
                total=self.bytes_to_mb(swap.total),
                used=self.bytes_to_mb(swap.used),
                free=self.bytes_to_mb(swap.free),
                percent=swap.percent
            ) + "\n\n"
        except Exception:
            pass

        # Disk Info
        try:
            disk = psutil.disk_usage(path)
            reply += self.strings["disk_info"].format(
                total=self.bytes_to_gb(disk.total),
                used=self.bytes_to_gb(disk.used),
                free=self.bytes_to_gb(disk.free),
                percent=disk.percent
            ) + "\n\n"
        except FileNotFoundError:
            reply += self.strings["invalid_path"].format(path=path) + "\n\n"
        except Exception:
            pass

        await utils.answer(message, reply)