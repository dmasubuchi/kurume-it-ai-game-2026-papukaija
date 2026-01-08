"""
OutGameメニュー

トップレベルのメニュー画面を提供する。
InGame直起動を禁止し、必ずOutGameメニューから開始する。
"""

from pathlib import Path
from typing import Callable

from src.outgame.save_manager import SaveManager, SlotName, SLOTS
from src.outgame.readme_viewer import display_readme


class OutGameMenu:
    """OutGameメニュークラス"""

    def __init__(
        self,
        base_path: Path | None = None,
        on_play: Callable[[SlotName, Path], None] | None = None,
    ) -> None:
        """
        Args:
            base_path: 02_tutorial/ のパス
            on_play: Continue時に呼ばれるコールバック (slot, slot_path) -> None
        """
        if base_path is None:
            base_path = Path(__file__).parent.parent.parent
        self.base_path = Path(base_path)
        self.save_manager = SaveManager(base_path)
        self.on_play = on_play
        self.running = True

    def clear_screen(self) -> None:
        """画面クリア（シンプル版）"""
        print("\n" * 3)

    def show_header(self) -> None:
        """ヘッダー表示"""
        print("=" * 50)
        print("  AI × Game Development Tutorial")
        print("  久留米工業大学 2026")
        print("=" * 50)
        print()

    def show_slot_status(self) -> None:
        """スロット状態を表示"""
        print("--- SAVE Slots ---")
        for status in self.save_manager.status():
            if not status.exists or not status.ready:
                state = "[Empty]"
            else:
                state = f"[Ready] Turn {status.turn}"
            print(f"  {status.name}: {state}")
        print()

    def show_main_menu(self) -> str:
        """メインメニューを表示して選択を取得"""
        self.clear_screen()
        self.show_header()
        self.show_slot_status()

        print("--- Menu ---")
        print("  1) Continue A")
        print("  2) Continue B")
        print("  3) Continue C")
        print("  4) Manage Saves")
        print("  5) Readme")
        print("  6) Quit")
        print()

        return input("Select (1-6): ").strip()

    def handle_continue(self, slot: SlotName) -> None:
        """Continue処理"""
        if not self.save_manager.is_ready(slot):
            print(f"\nSAVE_{slot} is not ready.")
            print("Use 'Manage Saves' -> 'setup' to initialize it first.")
            input("Press Enter to continue...")
            return

        slot_path = self.save_manager.get_slot_path(slot)
        print(f"\nLoading SAVE_{slot}...")

        if self.on_play:
            self.on_play(slot, slot_path)
        else:
            print("(No game handler registered)")
            input("Press Enter to continue...")

    def show_manage_menu(self) -> None:
        """Manage Savesメニュー"""
        while True:
            self.clear_screen()
            self.show_header()
            self.show_slot_status()

            print("--- Manage Saves ---")
            print("Commands:")
            print("  status      : Show slot status")
            print("  setup A|B|C : Initialize slot from template")
            print("  reset A|B|C : Reset slot to template state")
            print("  delete A|B|C: Delete slot data")
            print("  copy A B    : Copy slot A to B")
            print("  back        : Return to main menu")
            print()

            cmd = input("Command: ").strip().lower()

            if cmd == "back" or cmd == "":
                break
            elif cmd == "status":
                self._cmd_status()
            elif cmd.startswith("setup "):
                self._cmd_setup(cmd[6:].strip().upper())
            elif cmd.startswith("reset "):
                self._cmd_reset(cmd[6:].strip().upper())
            elif cmd.startswith("delete "):
                self._cmd_delete(cmd[7:].strip().upper())
            elif cmd.startswith("copy "):
                self._cmd_copy(cmd[5:].strip().upper())
            else:
                print(f"Unknown command: {cmd}")
                input("Press Enter to continue...")

    def _cmd_status(self) -> None:
        """status コマンド"""
        print()
        print("=== Detailed Status ===")
        for status in self.save_manager.status():
            print(f"\nSAVE_{status.name}:")
            print(f"  Exists: {status.exists}")
            print(f"  Ready: {status.ready}")
            if status.created_at:
                print(f"  Created: {status.created_at}")
            if status.last_played:
                print(f"  Last Played: {status.last_played}")
            print(f"  Turn: {status.turn}")
        print()
        input("Press Enter to continue...")

    def _cmd_setup(self, slot: str) -> None:
        """setup コマンド"""
        if slot not in SLOTS:
            print(f"Invalid slot: {slot}. Use A, B, or C.")
            input("Press Enter to continue...")
            return

        if self.save_manager.setup(slot):  # type: ignore
            print(f"SAVE_{slot} initialized successfully.")
        else:
            print(f"Failed to setup SAVE_{slot}. It may already exist.")
        input("Press Enter to continue...")

    def _cmd_reset(self, slot: str) -> None:
        """reset コマンド"""
        if slot not in SLOTS:
            print(f"Invalid slot: {slot}. Use A, B, or C.")
            input("Press Enter to continue...")
            return

        confirm = input(f"Reset SAVE_{slot}? All data will be lost. (y/N): ")
        if confirm.lower() == "y":
            if self.save_manager.reset(slot):  # type: ignore
                print(f"SAVE_{slot} reset successfully.")
            else:
                print(f"Failed to reset SAVE_{slot}.")
        else:
            print("Cancelled.")
        input("Press Enter to continue...")

    def _cmd_delete(self, slot: str) -> None:
        """delete コマンド"""
        if slot not in SLOTS:
            print(f"Invalid slot: {slot}. Use A, B, or C.")
            input("Press Enter to continue...")
            return

        confirm = input(f"Delete SAVE_{slot}? All data will be lost. (y/N): ")
        if confirm.lower() == "y":
            if self.save_manager.delete(slot):  # type: ignore
                print(f"SAVE_{slot} deleted.")
            else:
                print(f"Failed to delete SAVE_{slot}.")
        else:
            print("Cancelled.")
        input("Press Enter to continue...")

    def _cmd_copy(self, args: str) -> None:
        """copy コマンド"""
        parts = args.split()
        if len(parts) != 2:
            print("Usage: copy A B")
            input("Press Enter to continue...")
            return

        src, dest = parts
        if src not in SLOTS or dest not in SLOTS:
            print(f"Invalid slots. Use A, B, or C.")
            input("Press Enter to continue...")
            return

        if src == dest:
            print("Source and destination cannot be the same.")
            input("Press Enter to continue...")
            return

        confirm = input(f"Copy SAVE_{src} to SAVE_{dest}? (y/N): ")
        if confirm.lower() == "y":
            if self.save_manager.copy(src, dest):  # type: ignore
                print(f"Copied SAVE_{src} to SAVE_{dest}.")
            else:
                print(f"Failed to copy. SAVE_{src} may not exist.")
        else:
            print("Cancelled.")
        input("Press Enter to continue...")

    def run(self) -> None:
        """メニューループを実行"""
        self.running = True

        while self.running:
            choice = self.show_main_menu()

            if choice == "1":
                self.handle_continue("A")
            elif choice == "2":
                self.handle_continue("B")
            elif choice == "3":
                self.handle_continue("C")
            elif choice == "4":
                self.show_manage_menu()
            elif choice == "5":
                display_readme(self.base_path)
            elif choice == "6":
                self.running = False
                print("\nGoodbye!")
            else:
                print(f"Invalid selection: {choice}")
                input("Press Enter to continue...")
