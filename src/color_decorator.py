from typing import Self

from colorama import Fore, Style


class ColorDecorator:

    def __init__(
        self: Self,
        use_colors: bool = False,
    ):
        self._use_colors = bool(use_colors)

    def decorate_text(
        self: Self,
        text: str | None,
        fore,
        style,
    ) -> str | None:
        if text is None:
            return None
        text_str = str(text)
        if len(text_str.strip()) == 0:
            return text_str
        if not self._use_colors:
            return text_str
        if style is None:
            return f"{fore}{text_str}{Fore.RESET}"

        return f"{fore}{style}{text_str}{Fore.RESET}"

    # YELLOW

    def bright_yellow_text(
        self: Self,
        text: str,
    ) -> str:
        return self.decorate_text(text, Fore.YELLOW, Style.BRIGHT)

    # RED

    def bright_red_text(
        self: Self,
        text: str,
    ) -> str:
        return self.decorate_text(text, Fore.RED, Style.BRIGHT)

    # BLUE

    def bright_blue_text(
        self: Self,
        text: str,
    ) -> str:
        return self.decorate_text(text, Fore.BLUE, Style.BRIGHT)

    # GREEN

    def bright_green_text(
        self: Self,
        text: str,
    ) -> str:
        return self.decorate_text(text, Fore.GREEN, Style.BRIGHT)

    # WHITE

    def bright_white_text(
        self: Self,
        text: str,
    ) -> str:
        return self.decorate_text(text, Fore.WHITE, Style.BRIGHT)

    def dim_white_text(
        self: Self,
        text: str,
    ) -> str:
        return self.decorate_text(text, Fore.WHITE, Style.DIM)

    # CYAN

    def dim_cyan_text(
        self: Self,
        text: str,
    ) -> str:
        return self.decorate_text(text, Fore.CYAN, Style.DIM)

    def bright_cyan_text(
        self: Self,
        text: str,
    ) -> str:
        return self.decorate_text(text, Fore.CYAN, Style.BRIGHT)

    # MAGENTA

    def bright_magenta_text(
        self: Self,
        text: str,
    ) -> str:
        return self.decorate_text(text, Fore.MAGENTA, Style.BRIGHT)

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
