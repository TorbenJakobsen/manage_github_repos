from typing import Self

from colorama import Fore, Style


class ColorDecorator:

    def __init__(
        self: Self,
        use_colors: bool = True,
    ):
        self._use_colors = use_colors

    # YELLOW

    def bright_yellow_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.YELLOW}{Style.BRIGHT}{text}{Fore.RESET}"

    # RED

    def bright_red_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.RED}{Style.BRIGHT}{text}{Fore.RESET}"

    # BLUE

    def bright_blue_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.BLUE}{Style.BRIGHT}{text}{Fore.RESET}"

    # GREEN

    def bright_green_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.GREEN}{Style.BRIGHT}{text}{Fore.RESET}"

    # WHITE

    def bright_white_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.WHITE}{Style.BRIGHT}{text}{Fore.RESET}"

    def dim_white_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.WHITE}{Style.DIM}{text}{Fore.RESET}"

    # CYAN

    def dim_cyan_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.CYAN}{Style.DIM}{text}{Fore.RESET}"

    def bright_cyan_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.CYAN}{Style.BRIGHT}{text}{Fore.RESET}"

    # MAGENTA

    def bright_magenta_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.MAGENTA}{Style.BRIGHT}{text}{Fore.RESET}"

    # ===

    def error(
        self: Self,
        text: str,
    ) -> str:
        return self.bright_magenta_text(text)

    def neutral(
        self: Self,
        text: str,
    ) -> str:
        return self.dim_white_text(text)

    def not_a_repository(
        self: Self,
        text: str,
    ) -> str:
        return self.bright_red_text(text)

    def local_and_remote_identical(
        self: Self,
        text: str,
    ) -> str:
        return self.dim_white_text(text)

    def local_and_remote_different(
        self: Self,
        text: str,
    ) -> str:
        return self.bright_red_text(text)

    def active_head(
        self: Self,
        text: str,
    ) -> str:
        return self.bright_green_text(text)

    def inactive_head(
        self: Self,
        text: str,
    ) -> str:
        return self.dim_white_text(text)

    def managed_repo(
        self: Self,
        text: str,
    ) -> str:
        return self.bright_green_text(text)

    def unmanaged_repo(
        self: Self,
        text: str,
    ) -> str:
        return self.dim_white_text(text)
