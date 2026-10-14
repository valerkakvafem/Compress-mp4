import argparse
import colorsys
import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path


ART = r"""
       ,|^      )^,    /\^   ,  ^|<,, ^><,^<,, (           <(    (_  `     (_  |\      ,.><^` \,|_   )^\
      //`      ,/\^   <(^   _^   |~`^^^<<>>/>|)/           |>    >  )     ,/   |\,,><^`      ,,/<(_, _>^,
    ,>^        > (>   (/    /   _<,         _/~<``         |~   \( \`    _)    >^`      ,><\`,><^``| _< \_
  ,/^         /` >>   >    \_   ' |          >>|_          |~   /` /    _)`    |\, ,><^`,>^^`     ,^ _>__)
 >^       )  ,/ __|   >    (   /  (_     ^_  )||~          /   ,/ /    ,/`    </\^/\  (`     ,><^^~  < > ^(  (
         \^  >_ __)   >   \`  \`  ^|      \  ^//>          <  _)_/    )/      |_\,\\,  ).><^`,   >   ( >  (_ ^>
         /  )(   , (  (,  /   /   ,>_     ^,  (>>         _| _)\/   ,/^       )  |_,(,   ))  \  _)  ,`~_  <(  \
        \^  |~   ) ^, ^) _` ,)    >^>_     \  ^|)         <|,)>^  ,<^   \_   </  ^\^_|_   (\ _~ /^ ,^ /    /_ ^>
       _<  ,/    |\    )\/ ,\^   /`/,)_     \  ((         (>/^  ,<^     (    (_   \,\^\   ^/, \)/  ` )|    ^(  /__
    ,</\|  (|    |^\,   ^\,^/   )^,`(/>,     \ ^/,       ,>^ ,>/^      \`   _)<<,,,)_,'(   \^_/^    /^|    (>  |(^>,
 ,>^)^ /(  >)    |_^^>,  _\<,  )`\^/^\`^<     \_^(_    ,<^,><^)        /    /^^^^))^\^^^,  _>/`  _)</_|    |\_ ^^_^\^<
 ` /_ \_( _|\    |<) _^<<<__^>>`_^/_    ^|,    ^,^\ ,>()>^\   /       ,`   \><^```  _(^_^,<^`_>(>^` (,|    )|~ < ,  `
/\(   | ` \|>    ||( | `\^/<>,/>(</^^^^^^\^<<_  ^\/\<^`   >  <       _^    \<<^^^^^^<<>)<^,>>\^_^_\ ))|    >|> < )_
)^    ( | <(^,   |\` ^/ ')  ,>^//^`^`````^\ _^>,_ ^(\_   <(  /       /    />^`` ````/~((\^(,  () \^__/|   _^/) | <\_
      > ) <\ \   )/ )~`/,` ,)_//        (,),  (\/<<,^\,  |` ,_      /    /  \,,~       \\\_(, ^,\_/( \(   / /> ( ^_^\,
      \  ,^|  \  ^\_`^)\^ \/\(/         _^ >_,^\\_ ^>>/\_>  ^      /    /               ^\)/(_ ^/,)/_(`  /  |^,_ <   `
     ,(  ^_>\  \, \^/\\^ ,|)><<            ^\^_\/(, ^/,`^( /      /   ,>                <<^(<|, )//()/ _/  /<_^  (,
    ))_(  \\(), ^>,)>^( ,)//`^^    \_     ,<>\^,\,\, ^/((`/     ,/   >^ <._ ,  ,         ) ^\\/, \^//,>^ \/)/)  ,`(,
   //_ )\  \\/(>>,,__^>>(^^<, ^,<~  `^^,/^\,`^\/,\,^>_^>(/_    >^ ,>^`  <^)</^\`        )` _^ ^/<>^`` ,>>)>//` )\  \(
 <\^   >^)<,^</)_ `^^^/(`   ^\_\,    \/_  ^\// ^>\\,_\>//    ,^,>>^      ^>^>_  ^,><,^>)` >^   `^<^^^^` (\>^_><`>   \~
/^<_  <)_((\\>,\>,   , ^_     `\/><,__,^|/>^`    ^>/>//`  ,>\<>/,          `^<>(,,,\,>^/<`      ^ \_  ,</,>>/))_(>  ^<
`     (>|^/(,, (_`   ^, \          `^^``           )>\><>^^<>>/\/>,             ``^^`          / ,^   `|/`<))\`)/)
     _\\| \\/) ^\_    ^,_>                         ````^     `^^>>\<                          \`,^    _)^ (\// (\
     //|,_  \(\,(\     _\\                                                                   ,</`     ()_/)/   ,|
      _|((    ^(<)(       ^><,,,                                                          ,,<`       )(>)^    )||<_,
    /) |>^_    (>\/>,                                                                   \,         ,<|/~)     ^>| ,\
   / | |>_\    ^, >/(, ~(^^<(                         (<>^^^^^^<>/                        ^\>~~<< ,(\>_,`    ) >| | \
 _/_/| |~\^,    '_^^_\>, ^<,_\<,,                                                       ,./`,./`,>/_^^ '    _`<_| |  \
,^>^,' )~| \     \ \\  ^<,  `^^>~`^/>                                             ><(^^`<:^`  _//` // /     / |_/ ),
>^,/`\_^>^_ \    ,\ \     ^>.,, ^<,                                                  ,>^  ,.>^`   /) /\    /  `\` >_\,
<^   |( ( ,  \   ^/( _(._      `^>~~<<                                            ><>~<^^`     _>^)`)\^   /_ ) / )\
     |^_^,^,      \(\ ^,)    /^\^^```)<,                                        ,>/``^^^(><:^^`/`  /)/      ,^,`_^|
     ^ ^,^(^\      ^<\ )/>   ~ |     | _^>.,                                ,.<^`       )  ~  \_  /<^      >^)`_^ <
"""


PINK = 213
PINK_FADE = [213, 176, 139, 97, 60, 238]


ART_M = r"""
    /^   \\  )`  ) ^>.,^>^>\|      |  <>\_  |_ >_ ,><^``\   \(
  ,/`   _//  /  \` )>   ``\//`     (  | /  ,^  /^` ,.>|^><^_|/>
_/`   , / >  |  / \`|   ~ ^||      ) _>)  ,/  <)\(^>^` ,,</ |>)_ _
     \^,^ >, | \` / ^~   , <|      / /)` )^|  |^//,_>\^, |~ ~> \ \
     / /  \^_\_( )  /\_  ^_)^ <   _\// ,/` /  ) \)\_ \,^ / /,  (_</
   ><`~/  (\  \,/` )\))_  )_(> >  ,/`)//  <  <\,,\(\ _>_/` ,|  (> \(,
\<)`/_\|  |\>,_^(,)^\` ^(  )/\ (,/><^~<_  /  /\/>`/^\_)^_,/^|  (\ //\>
//_<__|(  (|\\^></>()<||<>, ^<\<^`( ) /^ )  )~><<><<>\>((\()\  |^ (| )
^  / ~|^_ |^(\\`,/(^    /( \>,^\\ ) ^,/ ,` ,^|>  _`_|/,_///_(  /> >|\,
   < \|_)_<<//^,((^     ^^>//,^><<\)\)_,^ ,^ _^     _(/,^)\\) / )) | `
  ,/,_>,,^<\//,>/\(^^, ,_,<\)/,^,|,\)`,^ >^,_,      _^\((^\>,^\\\^,^,
_,/ /\/<<:<../<`^,\^_/\<`^)>>\/\)>\/\/`>^  \^(^<,_,</,/ /\..><(/^)| ^,
`^ _|)/\<)( ( ,   ^<>>\>>^^ _^<<^>\/<>,     `><><^<><`  _`) </^>\))> )
   )//>/,\_( \^_              ^^^``^:<\>/               /)`  /_`/`)`
   `|| ^<<( \,^\,                                     ,/^  \,\^  ,/,,
  //|/_  /(>_ `^^^`              _,,,_              )(`    /><~  /\^\
 /`>||\  ^/)\,^<^\,_            ^`` _`^             ,>^,/,//^/  ,\|__\
/_/^))_,  \^\`^< `^(<`                           ^~|^^`.<^,//_ _^)|<\_
<` /^/,^( \\^<,,,`^|~(<,                        ~<|<^`_,,//)/_,' \^^ `
   ~\^/, \ \,^<  (<   ^><<,                  ,,<^   |`` (` /`_`,(/  ~
"""


def show_banner(cycles=2, animate=True):
    os.system("")
    cols = shutil.get_terminal_size((120, 30)).columns

    lines = ART.rstrip("\n").split("\n")
    art_pad = " " * max(0, (cols - max(len(l) for l in lines)) // 2)
    print("\033[36m" + "\n".join(art_pad + l for l in lines) + "\033[0m\n")

    caption = "Hello kitties!  by ValerkaKVA"
    cap_pad = " " * max(0, (cols - len(caption)) // 2)

    if not animate or not sys.stdout.isatty():
        print(cap_pad + caption + "\n")
        return

    def draw(color):
        text = " " * len(caption) if color is None else f"\033[38;5;{color}m{caption}\033[0m"
        sys.stdout.write("\r" + cap_pad + text)
        sys.stdout.flush()

    try:
        draw(PINK)
        time.sleep(1.0)
        for _ in range(cycles):
            for c in PINK_FADE + [None]:
                draw(c)
                time.sleep(0.08)
            time.sleep(0.4)
            for c in reversed(PINK_FADE):
                draw(c)
                time.sleep(0.08)
            draw(PINK)
            time.sleep(0.9)
    except KeyboardInterrupt:
        pass
    finally:
        draw(PINK)
        print("\n")


LIVE = None
LOG = []
STATE = {}


def say(msg):
    if LIVE:
        LOG.append(msg)
    else:
        print(msg)


FLAG_COLORS = [
    (255, 120, 190),
    (255, 190, 220),
    (255, 255, 255),
    (150, 210, 255),
    (80, 160, 255),
]


def _palette(steps=5):
    keys = FLAG_COLORS + FLAG_COLORS[-2:0:-1] + [FLAG_COLORS[0]]
    pal = []
    for a, b in zip(keys, keys[1:]):
        for k in range(steps):
            t = k / steps
            r, g, bl = (round(a[i] + (b[i] - a[i]) * t) for i in range(3))
            pal.append(f"\033[38;2;{r};{g};{bl}m")
    return pal


PALETTE = _palette()
PINK_ESC = "\033[38;5;213m"

CAT_FRAMES = [
    [" /\\_/\\ ", "( o.o )", " > ^ < "],
    ["  /\\_/\\", " ( o.o)", "  > ^< "],
    ["   /\\_ ", "  ( o> ", "   /\\) "],
    [" /\\_/\\ ", "(     )", " \\___/~"],
    [" _|\\   ", " <o )  ", " (/\\   "],
    ["/\\_/\\  ", "(o.o ) ", " >^ <  "],
]


def _rainbow(line, y, phase):
    out, last = [], -1
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(" ")
            continue
        idx = ((x + 2 * y) // 4 - phase) % len(PALETTE)
        if idx != last:
            out.append(PALETTE[idx])
            last = idx
        out.append(ch)
    return "".join(out) + "\033[0m"


class Live:

    def __init__(self):
        self.t0 = time.time()
        self.size = None
        self.active = False
        self.arts = []
        for a in (ART, ART_M):
            lines = a.rstrip("\n").split("\n")
            self.arts.append((lines, max(len(l) for l in lines)))

    def start(self):
        os.system("")
        sys.stdout.write("\033[?1049h\033[?25l\033[2J")
        sys.stdout.flush()
        self.active = True

    def stop(self):
        if self.active:
            sys.stdout.write("\033[0m\033[?25h\033[?1049l")
            sys.stdout.flush()
            self.active = False

    def _pick(self, cols, rows):
        for lines, w in self.arts:
            if w <= cols and len(lines) + 8 <= rows:
                return lines, w
        return [], 0

    def draw(self, st):
        cols, rows = shutil.get_terminal_size((120, 30))
        out = []
        if (cols, rows) != self.size:
            out.append("\033[2J")
            self.size = (cols, rows)
        phase = int((time.time() - self.t0) * 8)

        art, art_w = self._pick(cols, rows)
        block_h = len(art) + 4
        top = max(0, (rows - 4 - block_h) // 2) + 1

        for i, line in enumerate(art):
            col = (cols - art_w) // 2 + 1
            out.append(f"\033[{top + i};{col}H" + _rainbow(line, i, phase))

        def centered(row, text, color=""):
            col = max(1, (cols - len(text)) // 2 + 1)
            out.append(f"\033[{row};1H\033[2K\033[{row};{col}H{color}{text}\033[0m")

        r = top + len(art) + 1
        centered(r, "Hello kitties!  by ValerkaKVA", PINK_ESC)

        pct = st.get("pct")
        width = max(10, min(40, cols - 14))
        if pct is None:
            pos = int((time.time() - self.t0) * 12) % width
            bar = "".join("#" if abs(k - pos) < 3 else "-" for k in range(width))
            centered(r + 1, f"[{bar}]", PINK_ESC)
        else:
            done = int(width * pct)
            centered(r + 1, f"[{'#' * done}{'-' * (width - done)}] {pct * 100:5.1f}%", PINK_ESC)

        info = f"{st.get('name', '')} ({st.get('idx', 1)}/{st.get('n', 1)})"
        if st.get("speed"):
            info += f"   {st['speed']}"
        if st.get("fps"):
            info += f"   {st['fps']} fps"
        centered(r + 2, info[: cols - 1])

        if cols >= 10:
            frame = CAT_FRAMES[int((time.time() - self.t0) * 5) % len(CAT_FRAMES)]
            col = cols - 8
            for k, row_txt in enumerate(frame):
                out.append(f"\033[{rows - 2 + k};{col}H" + _rainbow(row_txt, k, phase * 2))
        sys.stdout.write("".join(out))
        sys.stdout.flush()


def probe_duration(src: Path):
    try:
        res = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(src)],
            capture_output=True, text=True, timeout=20)
        return float(res.stdout.strip())
    except Exception:
        return None


def run_cmd(cmd, args):
    if not LIVE:
        return subprocess.run(cmd).returncode == 0

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, encoding="utf-8", errors="replace")
    errors = []
    STATE.update(pct=0.0 if STATE.get("dur") else None, fps="", speed="")

    def pump_out():
        for line in proc.stdout:
            key, _, val = line.strip().partition("=")
            if key in ("out_time_us", "out_time_ms"):
                try:
                    sec = int(val) / 1e6
                except ValueError:
                    continue
                if STATE.get("dur"):
                    STATE["pct"] = min(1.0, max(0.0, sec / STATE["dur"]))
            elif key == "fps":
                STATE["fps"] = val
            elif key == "speed":
                STATE["speed"] = val.strip()

    def pump_err():
        for line in proc.stderr:
            errors.append(line.rstrip())

    threads = [threading.Thread(target=f, daemon=True) for f in (pump_out, pump_err)]
    for t in threads:
        t.start()
    try:
        while proc.poll() is None:
            LIVE.draw(STATE)
            time.sleep(0.1)
    except KeyboardInterrupt:
        proc.kill()
        raise
    for t in threads:
        t.join(timeout=2)

    if proc.returncode == 0:
        STATE["pct"] = 1.0
        LIVE.draw(STATE)
        return True
    for line in errors[-5:]:
        say("[ffmpeg] " + line)
    return False


WIN_PX = (800, 600)

INSTRUCTIONS = [
    ("", "ENGLISH", "УКРАЇНСЬКА"),
    ("video.mp4/folder", "compress a file or a whole folder", "стиснути файл або всю папку"),
    ("--crf 18..23", "quality, lower = better", "якість, менше = краще"),
    ("--codec h265", "smaller file (default h264)", "менший файл (за замовч. h264)"),
    ("--turbo", "fastest, bigger file", "найшвидше, файл більший"),
    ("--cpu", "no GPU, smaller file", "без відеокарти, менший файл"),
    ("--jobs 3", "several files at once", "кілька файлів одночасно"),
    ("--plain", "no live screen", "без живого екрана"),
    ("--no-intro", "skip this intro", "без вступу"),
    ("no path?", "the script will ask for it", "скрипт сам запитає шлях"),
]


def set_window_size(px_w=800, px_h=600):
    cols, rows = px_w // 8, px_h // 16
    try:
        if os.name == "nt":
            if os.environ.get("WT_SESSION") or os.environ.get("TERM_PROGRAM") == "vscode":
                return
            os.system(f"mode con: cols={cols} lines={rows}")
        elif sys.stdout.isatty():
            sys.stdout.write(f"\033[8;{rows};{cols}t")
            sys.stdout.flush()
    except Exception:
        pass


def center_window(size_px=None):
    if os.name != "nt" or os.environ.get("TERM_PROGRAM") == "vscode":
        return
    try:
        import ctypes
        from ctypes import wintypes

        k32, u32 = ctypes.windll.kernel32, ctypes.windll.user32
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            pass
        k32.GetConsoleWindow.restype = wintypes.HWND
        u32.GetAncestor.restype = wintypes.HWND
        u32.GetAncestor.argtypes = [wintypes.HWND, wintypes.UINT]
        u32.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
        u32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int,
                                     ctypes.c_int, ctypes.c_int, wintypes.UINT]

        hwnd = k32.GetConsoleWindow()
        if not hwnd:
            return
        root = u32.GetAncestor(hwnd, 3)
        if root:
            hwnd = root

        rect = wintypes.RECT()
        if not u32.GetWindowRect(hwnd, ctypes.byref(rect)):
            return
        w, h = rect.right - rect.left, rect.bottom - rect.top
        flags = 0x0004 | 0x0010
        if size_px and os.environ.get("WT_SESSION"):
            w, h = size_px
        else:
            flags |= 0x0001

        work = wintypes.RECT()
        u32.SystemParametersInfoW(0x0030, 0, ctypes.byref(work), 0)
        x = work.left + (work.right - work.left - w) // 2
        y = work.top + (work.bottom - work.top - h) // 2
        u32.SetWindowPos(hwnd, None, x, y, w, h, flags)
    except Exception:
        pass


def pick_art(cols, rows, reserve, prefer_small=False):
    arts = [ART, ART_M]
    if prefer_small:
        arts.reverse()
    for a in arts:
        lines = a.rstrip("\n").split("\n")
        w = max(len(l) for l in lines)
        if w <= cols - 2 and len(lines) + reserve <= rows:
            return lines, w
    return [], 0


def show_intro():
    os.system("")
    cols, rows = shutil.get_terminal_size((100, 37))
    out = sys.stdout

    greeting = "Hello, user!"
    out.write(" " * max(0, (cols - len(greeting)) // 2) + PINK_ESC)
    for ch in greeting:
        out.write(ch)
        out.flush()
        time.sleep(0.07)
    out.write("\033[0m\n\n")
    out.flush()
    time.sleep(0.4)

    art, art_w = pick_art(cols, rows, 16)
    if not art:
        art, art_w = pick_art(cols, rows, 0, prefer_small=True)
    pad = " " * max(0, (cols - art_w) // 2)
    for i, line in enumerate(art):
        out.write(pad + _rainbow(line, i, 0) + "\n")
        out.flush()
        time.sleep(0.045)

    caption = "Hello kitties!  by ValerkaKVA"
    out.write("\n" + " " * max(0, (cols - len(caption)) // 2) + PINK_ESC + caption + "\033[0m\n\n")

    c1 = max(len(r[0]) for r in INSTRUCTIONS) + 2
    c2 = max(len(r[1]) for r in INSTRUCTIONS) + 2
    width = c1 + c2 + max(len(r[2]) for r in INSTRUCTIONS)
    pad = " " * max(0, (cols - width) // 2)
    for k, (opt, en, uk) in enumerate(INSTRUCTIONS):
        if k == 0:
            head = "\033[1;38;5;213m"
            out.write(pad + head + opt.ljust(c1) + en.ljust(c2) + uk + "\033[0m\n")
        else:
            out.write(pad + "\033[38;5;117m" + opt.ljust(c1) + "\033[38;5;250m"
                      + en.ljust(c2) + uk + "\033[0m\n")
    out.flush()


def check_ffmpeg():
    if shutil.which("ffmpeg") is None:
        sys.exit("ffmpeg не знайдено в PATH.\n"
                 "Встанови: winget install ffmpeg  (потім ПЕРЕЗАПУСТИ термінал)")


HW_ENCODERS = {
    "h264": [("nvenc", "h264_nvenc"), ("qsv", "h264_qsv"), ("amf", "h264_amf")],
    "h265": [("nvenc", "hevc_nvenc"), ("qsv", "hevc_qsv"), ("amf", "hevc_amf")],
}
_hw_cache = {}


def detect_hw(codec: str):
    if codec in _hw_cache:
        return _hw_cache[codec]
    found = None
    for kind, enc in HW_ENCODERS.get(codec, []):
        test = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                "-i", "color=black:s=320x240:d=0.2", "-frames:v", "1",
                "-c:v", enc, "-f", "null", "-"]
        if subprocess.run(test, capture_output=True).returncode == 0:
            found = (kind, enc)
            break
    _hw_cache[codec] = found
    return found


def build_command(src: Path, dst: Path, args, audio_copy: bool, hw=None, hwdec=False) -> list:
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error"]
    if args.live:
        cmd += ["-nostats", "-progress", "pipe:1"]
    else:
        cmd += ["-nostats" if args.jobs > 1 else "-stats"]
    cmd += ["-y"]
    if hwdec:
        cmd += ["-hwaccel", "auto"]
    cmd += ["-i", str(src), "-map", "0:v:0", "-map", "0:a?", "-map_metadata", "0",
            "-threads", "0"]
    crf = str(args.crf)

    if hw:
        kind, enc = hw
        cmd += ["-c:v", enc]
        if kind == "nvenc":
            cmd += ["-preset", "p1" if args.turbo else "p2", "-rc", "vbr", "-cq", crf, "-b:v", "0"]
        elif kind == "qsv":
            cmd += ["-preset", "veryfast", "-global_quality", crf]
        elif kind == "amf":
            cmd += ["-quality", "speed", "-rc", "cqp",
                    "-qp_i", crf, "-qp_p", crf, "-qp_b", crf]
        if args.codec == "h265":
            cmd += ["-tag:v", "hvc1"]
    elif args.codec == "h264":
        cmd += ["-c:v", "libx264", "-preset", args.preset,
                "-crf", "0" if args.lossless else crf]
    elif args.codec == "h265":
        cmd += ["-c:v", "libx265", "-preset", args.preset, "-crf", crf, "-tag:v", "hvc1"]
        if args.lossless:
            cmd += ["-x265-params", "lossless=1"]
    elif args.codec == "av1":
        cmd += ["-c:v", "libsvtav1", "-preset", "8", "-crf", crf]

    ten_bit = args.tenbit and args.codec != "h264"
    cmd += ["-pix_fmt", "yuv420p10le" if ten_bit else "yuv420p"]
    cmd += ["-c:a", "copy"] if audio_copy else ["-c:a", "aac", "-b:a", "192k"]
    cmd += ["-movflags", "+faststart", str(dst)]
    return cmd


def run_ffmpeg(src: Path, dst: Path, args) -> bool:
    hw = None
    if not args.cpu and not args.lossless and args.codec in HW_ENCODERS:
        hw = detect_hw(args.codec)
    say(f"[кодувальник] {hw[1] + ' (відеокарта)' if hw else 'процесор (CPU), preset ' + args.preset}")

    attempts = []
    if hw:
        attempts += [(hw, True, True), (hw, True, False), (hw, False, False)]
    attempts += [(None, True, True), (None, True, False), (None, False, False)]
    for mode, audio_copy, hwdec in attempts:
        if run_cmd(build_command(src, dst, args, audio_copy, mode, hwdec), args):
            return True
        dst.unlink(missing_ok=True)
        say("[інфо] не вийшло, пробую інший варіант...")
    return False


def compress(src: Path, args, idx=1, n=1) -> None:
    dst = src.with_name(f"{src.stem}_compressed.mp4")
    if dst.exists() and not args.overwrite:
        say(f"[пропуск] {dst.name} вже існує (--overwrite щоб перезаписати)")
        return

    STATE.clear()
    STATE.update(name=src.name, idx=idx, n=n, pct=None, fps="", speed="",
                 dur=probe_duration(src) if LIVE else None)
    say(f"[старт] {src.name}")
    if not run_ffmpeg(src, dst, args):
        say(f"[помилка] не вдалося обробити {src.name}")
        return

    old, new = src.stat().st_size, dst.stat().st_size
    if new >= old:
        say(f"[увага] результат не менший за оригінал "
              f"({new / 1e6:.1f} МБ >= {old / 1e6:.1f} МБ), видаляю")
        dst.unlink()
        return

    say(f"[готово] {old / 1e6:.1f} МБ -> {new / 1e6:.1f} МБ "
          f"(економія {(1 - new / old) * 100:.1f}%)")


def main():
    p = argparse.ArgumentParser(description="Стиснення MP4 майже без втрати якості")
    p.add_argument("path", nargs="?", help="MP4-файл або папка з ними (якщо не вказано - запитає)")
    p.add_argument("--codec", choices=["h264", "h265", "av1"], default="h264",
                   help="h264 - працює скрізь (за замовчуванням), h265/av1 - менший файл")
    p.add_argument("--crf", type=int, default=20,
                   help="менше = краща якість (h264/h265: 18-23; av1: 25-32)")
    p.add_argument("--preset", default="veryfast",
                   help="для процесора: ultrafast...superfast...veryfast...medium...slow...veryslow")
    p.add_argument("--turbo", action="store_true",
                   help="найшвидше з можливого (файл буде більшим)")
    p.add_argument("--jobs", type=int, default=1,
                   help="скільки файлів обробляти одночасно (корисно для відеокарти й папок)")
    p.add_argument("--no-anim", action="store_true", help="без анімації напису на старті")
    p.add_argument("--plain", action="store_true",
                   help="без живого екрана (звичайний вивід ffmpeg)")
    p.add_argument("--no-intro", action="store_true", help="без привітання й вступної анімації")
    p.add_argument("--no-resize", action="store_true", help="не міняти розмір і положення вікна консолі")
    p.add_argument("--tenbit", action="store_true", help="10-бітний колір (h265/av1)")
    p.add_argument("--lossless", action="store_true",
                   help="справжній lossless (файл буде величезним)")
    p.add_argument("--cpu", action="store_true",
                   help="не використовувати відеокарту (повільніше, але менший файл)")
    p.add_argument("--overwrite", action="store_true")
    args = p.parse_args()
    if args.turbo:
        args.preset = "ultrafast"
    args.jobs = max(1, args.jobs)

    tty = sys.stdout.isatty()
    if tty and not args.no_resize:
        set_window_size(*WIN_PX)
        center_window(WIN_PX)
    args.live = (not args.plain and args.jobs == 1 and tty
                 and shutil.get_terminal_size((120, 30)).lines >= 8)
    if tty and not (args.no_intro or args.no_anim):
        show_intro()
    elif not (args.live and args.path):
        show_banner(animate=False)
    check_ffmpeg()

    raw = args.path or input("Шлях до MP4 або папки: ")
    target = Path(raw.strip().strip('"'))
    if target.is_dir():
        files = [f for f in sorted(target.iterdir())
                 if f.suffix.lower() == ".mp4" and "_compressed" not in f.stem]
    elif target.is_file():
        files = [target]
    else:
        sys.exit(f"Шлях не знайдено: {target}")

    if not files:
        sys.exit("MP4-файлів не знайдено")

    if not args.cpu and not args.lossless and args.codec in HW_ENCODERS:
        detect_hw(args.codec)

    global LIVE
    if args.live:
        LIVE = Live()
        LIVE.start()
    try:
        if args.jobs > 1 and len(files) > 1:
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=args.jobs) as pool:
                list(pool.map(lambda f: compress(f, args), files))
        else:
            for i, f in enumerate(files, 1):
                compress(f, args, i, len(files))
    finally:
        if LIVE:
            LIVE.stop()
            LIVE = None
        for msg in LOG:
            print(msg)


if __name__ == "__main__":
    main()