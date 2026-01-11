import os
import socket
import psutil

from pyrogram import Client, types
from .. import loader, utils


@loader.module("NetEnvInfo", "Kuruuse-P", 1.2)
class NetEnvInfo(loader.Module):
    """Automatic host, environment and network detection (single command)."""

    # ===================== STRINGS ===================== #

    strings = {
        "header": "🇺🇸 <b>Runtime Environment Detection</b>\n\n",
        "hostname": "🏠 <b>Hostname:</b> {hostname}\n",
        "termux": "📱 <b>Termux:</b> {value}\n",
        "goorm": "☁️ <b>goorm.io:</b> {value}\n",
        "vps": "🖥️ <b>VPS/VDS:</b> {value} ({details})\n\n",
        "netio": "🌐 <b>Network I/O</b>\n"
                 "- Sent: {sent} MB\n"
                 "- Received: {recv} MB\n"
                 "- Packets Sent: {ps}\n"
                 "- Packets Received: {pr}\n\n",
        "interfaces": "🔌 <b>Network Interfaces</b>\n{data}\n",
        "connections": "🔗 <b>Active Connections</b>\n{data}",
        "denied": "🔒 <b>{name}:</b> Access denied\n\n",
        "error": "❌ Error: {e}"
    }

    strings_ru = {
        "header": "🇷🇺 <b>Определение среды выполнения</b>\n\n",
        "hostname": "🏠 <b>Имя хоста:</b> {hostname}\n",
        "termux": "📱 <b>Termux:</b> {value}\n",
        "goorm": "☁️ <b>goorm.io:</b> {value}\n",
        "vps": "🖥️ <b>VPS/VDS:</b> {value} ({details})\n\n",
        "netio": "🌐 <b>Сетевой I/O</b>\n"
                 "- Отправлено: {sent} МБ\n"
                 "- Получено: {recv} МБ\n"
                 "- Пакетов отправлено: {ps}\n"
                 "- Пакетов получено: {pr}\n\n",
        "interfaces": "🔌 <b>Сетевые интерфейсы</b>\n{data}\n",
        "connections": "🔗 <b>Активные соединения</b>\n{data}",
        "denied": "🔒 <b>{name}:</b> Доступ запрещён\n\n",
        "error": "❌ Ошибка: {e}"
    }

    strings_kz = {
        "header": "🇰🇿 <b>Орындалу ортасын анықтау</b>\n\n",
        "hostname": "🏠 <b>Хост атауы:</b> {hostname}\n",
        "termux": "📱 <b>Termux:</b> {value}\n",
        "goorm": "☁️ <b>goorm.io:</b> {value}\n",
        "vps": "🖥️ <b>VPS/VDS:</b> {value} ({details})\n\n",
        "netio": "🌐 <b>Желі I/O</b>\n"
                 "- Жіберілді: {sent} МБ\n"
                 "- Алынды: {recv} МБ\n"
                 "- Пакеттер жіберілді: {ps}\n"
                 "- Пакеттер алынды: {pr}\n\n",
        "interfaces": "🔌 <b>Желі интерфейстері</b>\n{data}\n",
        "connections": "🔗 <b>Белсенді қосылымдар</b>\n{data}",
        "denied": "🔒 <b>{name}:</b> Қол жеткізуге тыйым салынған\n\n",
        "error": "❌ Қате: {e}"
    }

    strings_ua = {
        "header": "🇺🇦 <b>Визначення середовища виконання</b>\n\n",
        "hostname": "🏠 <b>Ім'я хоста:</b> {hostname}\n",
        "termux": "📱 <b>Termux:</b> {value}\n",
        "goorm": "☁️ <b>goorm.io:</b> {value}\n",
        "vps": "🖥️ <b>VPS/VDS:</b> {value} ({details})\n\n",
        "netio": "🌐 <b>Мережевий I/O</b>\n"
                 "- Надіслано: {sent} МБ\n"
                 "- Отримано: {recv} МБ\n"
                 "- Пакетів надіслано: {ps}\n"
                 "- Пакетів отримано: {pr}\n\n",
        "interfaces": "🔌 <b>Мережеві інтерфейси</b>\n{data}\n",
        "connections": "🔗 <b>Активні з'єднання</b>\n{data}",
        "denied": "🔒 <b>{name}:</b> Доступ заборонено\n\n",
        "error": "❌ Помилка: {e}"
    }

    strings_uz = {
        "header": "🇺🇿 <b>Ish muhiti aniqlash</b>\n\n",
        "hostname": "🏠 <b>Xost nomi:</b> {hostname}\n",
        "termux": "📱 <b>Termux:</b> {value}\n",
        "goorm": "☁️ <b>goorm.io:</b> {value}\n",
        "vps": "🖥️ <b>VPS/VDS:</b> {value} ({details})\n\n",
        "netio": "🌐 <b>Tarmoq I/O</b>\n"
                 "- Yuborildi: {sent} MB\n"
                 "- Qabul qilindi: {recv} MB\n"
                 "- Paketlar yuborildi: {ps}\n"
                 "- Paketlar qabul qilindi: {pr}\n\n",
        "interfaces": "🔌 <b>Tarmoq interfeyslari</b>\n{data}\n",
        "connections": "🔗 <b>Faol ulanishlar</b>\n{data}",
        "denied": "🔒 <b>{name}:</b> Ruxsat yo‘q\n\n",
        "error": "❌ Xatolik: {e}"
    }

    strings_jp = {
        "header": "🇯🇵 <b>実行環境の検出</b>\n\n",
        "hostname": "🏠 <b>ホスト名:</b> {hostname}\n",
        "termux": "📱 <b>Termux:</b> {value}\n",
        "goorm": "☁️ <b>goorm.io:</b> {value}\n",
        "vps": "🖥️ <b>VPS/VDS:</b> {value} ({details})\n\n",
        "netio": "🌐 <b>ネットワーク I/O</b>\n"
                 "- 送信: {sent} MB\n"
                 "- 受信: {recv} MB\n"
                 "- 送信パケット: {ps}\n"
                 "- 受信パケット: {pr}\n\n",
        "interfaces": "🔌 <b>ネットワークインターフェース</b>\n{data}\n",
        "connections": "🔗 <b>アクティブな接続</b>\n{data}",
        "denied": "🔒 <b>{name}:</b> アクセス拒否\n\n",
        "error": "❌ エラー: {e}"
    }

    strings_kr = {
        "header": "🇰🇷 <b>실행 환경 감지</b>\n\n",
        "hostname": "🏠 <b>호스트 이름:</b> {hostname}\n",
        "termux": "📱 <b>Termux:</b> {value}\n",
        "goorm": "☁️ <b>goorm.io:</b> {value}\n",
        "vps": "🖥️ <b>VPS/VDS:</b> {value} ({details})\n\n",
        "netio": "🌐 <b>네트워크 I/O</b>\n"
                 "- 송신: {sent} MB\n"
                 "- 수신: {recv} MB\n"
                 "- 송신 패킷: {ps}\n"
                 "- 수신 패킷: {pr}\n\n",
        "interfaces": "🔌 <b>네트워크 인터페이스</b>\n{data}\n",
        "connections": "🔗 <b>활성 연결</b>\n{data}",
        "denied": "🔒 <b>{name}:</b> 접근 거부됨\n\n",
        "error": "❌ 오류: {e}"
    }

    # ===================== UTILS ===================== #

    def mb(self, b: int) -> float:
        return round(b / 1024 / 1024, 1)

    def is_termux(self):
        return "TERMUX_VERSION" in os.environ

    def is_goorm(self):
        h = socket.gethostname().lower()
        return h == "goorm" or "goorm" in h

    def is_vps(self):
        indicators = [
            "kvm", "vmware", "virtualbox", "xen", "qemu",
            "amazon", "google", "oracle", "digitalocean",
            "linode", "vultr", "microsoft"
        ]
        try:
            with open("/sys/class/dmi/id/sys_vendor") as f:
                v = f.read().lower()
                if any(i in v for i in indicators):
                    return True, v.capitalize()
        except:
            pass

        try:
            with open("/proc/cpuinfo") as f:
                if "hypervisor" in f.read().lower():
                    return True, "Hypervisor"
        except:
            pass

        if os.path.exists("/.dockerenv"):
            return True, "Docker"

        return False, "Physical / Unknown"

    # ===================== COMMAND ===================== #

    @loader.command()
    async def netenv(self, app: Client, message: types.Message):
        """Automatic environment and network detection"""

        reply = self.strings["header"]

        try:
            reply += self.strings["hostname"].format(
                hostname=socket.gethostname()
            )
            reply += self.strings["termux"].format(
                value="Yes" if self.is_termux() else "No"
            )
            reply += self.strings["goorm"].format(
                value="Yes" if self.is_goorm() else "No"
            )

            is_vps, details = self.is_vps()
            reply += self.strings["vps"].format(
                value="Yes" if is_vps else "No",
                details=details
            )

            try:
                io = psutil.net_io_counters()
                reply += self.strings["netio"].format(
                    sent=self.mb(io.bytes_sent),
                    recv=self.mb(io.bytes_recv),
                    ps=io.packets_sent,
                    pr=io.packets_recv
                )
            except PermissionError:
                reply += self.strings["denied"].format(name="Network I/O")

            try:
                iface_txt = ""
                for iface, addrs in psutil.net_if_addrs().items():
                    iface_txt += f"- {iface}\n"
                    for a in addrs:
                        iface_txt += f"  • {a.family.name}: {a.address}\n"
                reply += self.strings["interfaces"].format(data=iface_txt)
            except PermissionError:
                reply += self.strings["denied"].format(name="Interfaces")

            try:
                conns_txt = ""
                for c in psutil.net_connections()[:10]:
                    la = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else "N/A"
                    ra = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else "N/A"
                    conns_txt += f"- {la} → {ra} [{c.status}]\n"
                reply += self.strings["connections"].format(
                    data=conns_txt or "No active connections"
                )
            except PermissionError:
                reply += self.strings["denied"].format(name="Connections")

            await utils.answer(message, reply)

        except Exception as e:
            await utils.answer(
                message,
                self.strings["error"].format(e=e)
            )
