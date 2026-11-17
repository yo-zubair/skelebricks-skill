#!/usr/bin/env python3
"""Validate Bricks JSON (clipboard or template export).

Usage: python3 validate.py [--upstream] file.json [file2.json ...]

Checks tree integrity, global class references and the value-shape mistakes
that silently produce no CSS, plus the SkeleBricks framework rules (token names
from framework/tokens.md, no raw colours/sizes, BEM class names, section labels,
styles on classes not elements, %root% in custom CSS).
--upstream skips the SkeleBricks checks (for the raw upstream patterns/).
Exit code 1 if any ERROR is found; WARNs don't fail.
"""
import json
import os
import re
import sys

TOKENS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "framework", "tokens.md")
try:
    with open(TOKENS_FILE) as _f:
        TOKENS = set(re.findall(r"^\s*(--[a-z0-9-]+)\s*:", _f.read(), re.M))
except OSError:
    TOKENS = set()
BEM_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*(__[a-z0-9]+(-[a-z0-9]+)*)?(--[a-z0-9]+(-[a-z0-9]+)*)?$")
VAR_RE = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)")
RAW_LEN_RE = re.compile(r"(?<![\w.-])-?\d*\.?\d+(px|rem|em)\b")
RAW_COLOR_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(rgba?|hsla?)\(")
ELEMENT_OK_UNDERSCORE = {"_cssGlobalClasses", "_cssId", "_attributes", "_conditions", "_interactions", "_hidden"}
TOKEN_LEN_KEYS = {"_padding", "_margin", "_rowGap", "_columnGap", "_gap", "_gridGap"}

ID_RE = re.compile(r"^[a-z0-9]{6}$", re.I)
DEFAULT_BREAKPOINTS = {"tablet_portrait", "mobile_landscape", "mobile_portrait", "desktop"}
DEFAULT_PSEUDOS = {"hover", "active", "focus"}
LAYOUT = {"section", "container", "block", "div"}

WRONG_KEYS = {
    "_textAlign": "use _typography: {\"text-align\": ...}",
    "_maxWidth": "use _widthMax",
    "_minWidth": "use _widthMin",
    "_maxHeight": "use _heightMax",
    "_minHeight": "use _heightMin",
    "_borderRadius": "use _border.radius",
    "_animation": "deprecated; use _interactions",
    "_animationDuration": "deprecated; use _interactions",
    "_animationDelay": "deprecated; use _interactions",
}
CAMEL_TYPO = re.compile(r"^[a-z]+[A-Z]")


def element_lists(d):
    for key in ("content", "header", "footer"):
        if isinstance(d.get(key), list):
            yield key, d[key]


def split_key(key):
    """'_padding:tablet_portrait:hover' -> ('_padding', ['tablet_portrait', 'hover'])"""
    parts = key.split(":")
    return parts[0], parts[1:]


def check_settings(where, settings, errors, warns, is_layout, custom_bps):
    if not isinstance(settings, dict):
        errors.append(f"{where}: settings must be an object, got {type(settings).__name__}")
        return
    for key, val in settings.items():
        base, suffixes = split_key(key)
        for s in suffixes:
            if s in DEFAULT_BREAKPOINTS or s in custom_bps or s in DEFAULT_PSEUDOS:
                continue
            if s in ("tablet", "mobile", "desktop_only", "laptop"):
                errors.append(f"{where}: '{key}' uses unknown breakpoint '{s}'")
            elif not s.startswith("variant-"):
                warns.append(f"{where}: '{key}' uses suffix '{s}' (must be a registered breakpoint or pseudo-class)")
        if base in WRONG_KEYS:
            errors.append(f"{where}: '{key}' -> {WRONG_KEYS[base]}")
        if base == "_gap" and is_layout:
            errors.append(f"{where}: '_gap' on a layout element -> use _columnGap/_rowGap")
        if base == "_cssClasses" and not isinstance(val, str):
            errors.append(f"{where}: _cssClasses must be a space-separated string")
        if base == "_cssGlobalClasses" and not isinstance(val, list):
            errors.append(f"{where}: _cssGlobalClasses must be an array of class ids")
        if base == "_typography" and isinstance(val, dict):
            for k in val:
                if CAMEL_TYPO.match(k):
                    errors.append(f"{where}: _typography key '{k}' must be a CSS property name (kebab-case)")
            if "color" in val and not isinstance(val["color"], dict):
                errors.append(f"{where}: _typography.color must be an object ({{hex|rgb|raw}})")
        if base == "_boxShadow" and isinstance(val, (dict, list)):
            items = val if isinstance(val, list) else [val]
            for it in items:
                if isinstance(it, dict) and any(k in it for k in ("offsetX", "offsetY", "blur")):
                    errors.append(f"{where}: _boxShadow offsets must nest under 'values'")
            if isinstance(val, list):
                warns.append(f"{where}: _boxShadow is an array; expected a single object")
        if base == "_gradient" and isinstance(val, dict) and "stops" in val:
            errors.append(f"{where}: _gradient uses 'colors': [{{color, stop}}], not 'stops'")
        if base == "_background":
            if isinstance(val, str):
                errors.append(f"{where}: _background must be an object")
            elif isinstance(val, dict):
                if "gradient" in val:
                    errors.append(f"{where}: _background.gradient is not a Bricks key -> use _gradient")
                if "color" in val and not isinstance(val["color"], dict):
                    errors.append(f"{where}: _background.color must be an object")
        if base in ("_padding", "_margin") and isinstance(val, str):
            errors.append(f"{where}: {base} must be a per-side object, not a string")
        if base == "_border" and isinstance(val, dict) and "color" in val and not isinstance(val["color"], dict):
            errors.append(f"{where}: _border.color must be an object")
        if base == "_cssCustom" and isinstance(val, str) and re.search(r"#brxe-[a-z0-9]{6}", val):
            warns.append(f"{where}: _cssCustom hard-codes #brxe-id; ids change on paste/import -> use %root%")
        if base == "_interactions" and isinstance(val, list):
            for it in val:
                if not isinstance(it, dict) or not it.get("id"):
                    errors.append(f"{where}: every interaction needs an 'id'")


def walk_strings(val):
    if isinstance(val, str):
        yield val
    elif isinstance(val, dict):
        for v in val.values():
            yield from walk_strings(v)
    elif isinstance(val, list):
        for v in val:
            yield from walk_strings(v)


def walk_colors(val):
    """yield color objects (dicts with hex/rgb/raw) anywhere in a value"""
    if isinstance(val, dict):
        if any(k in val for k in ("hex", "rgb")) and "raw" not in val:
            yield val
        for v in val.values():
            yield from walk_colors(v)
    elif isinstance(val, list):
        for v in val:
            yield from walk_colors(v)


def check_framework(where, settings, errors, warns, is_class):
    if not isinstance(settings, dict):
        return
    for key, val in settings.items():
        base, _ = split_key(key)
        for sv in walk_strings(val):
            for name in VAR_RE.findall(sv):
                if TOKENS and name not in TOKENS:
                    errors.append(f"{where}: var({name}) is not a SkeleBricks token (closed set, see framework/tokens.md)")
        for c in walk_colors(val):
            errors.append(f"{where}: '{key}' has a raw colour {c.get('hex') or c.get('rgb')} -> use {{\"raw\": \"var(--token)\"}}")
        if base == "_cssCustom" and isinstance(val, str):
            if "%root%" not in val:
                warns.append(f"{where}: _cssCustom should target %root%")
            if RAW_COLOR_RE.search(val):
                warns.append(f"{where}: _cssCustom contains a raw colour -> use a colour token")
        if base in TOKEN_LEN_KEYS:
            for sv in walk_strings(val):
                if "var(" not in sv and RAW_LEN_RE.search(sv):
                    warns.append(f"{where}: '{key}' raw length '{sv}' -> snap to a --space-* token")
        if base == "_typography" and isinstance(val, dict):
            fs = val.get("font-size")
            if isinstance(fs, str) and "var(" not in fs and RAW_LEN_RE.search(fs):
                warns.append(f"{where}: font-size '{fs}' -> snap to a --text-* token")
        if base == "_border" and isinstance(val, dict) and isinstance(val.get("radius"), dict):
            for sv in val["radius"].values():
                if isinstance(sv, str) and "var(" not in sv and RAW_LEN_RE.search(sv) and sv not in ("0", "0px"):
                    warns.append(f"{where}: border radius '{sv}' -> use a --radius-* token")
        if base == "_boxShadow":
            warns.append(f"{where}: _boxShadow control -> use %root% {{ box-shadow: var(--shadow-*); }} in _cssCustom")
        if not is_class:
            if base == "_cssClasses":
                warns.append(f"{where}: _cssClasses used; SkeleBricks styles only through BEM global classes")
            elif base.startswith("_") and base not in ELEMENT_OK_UNDERSCORE:
                warns.append(f"{where}: style setting '{key}' on the element -> move it to the element's BEM class")


def validate(path, framework=True):
    errors, warns = [], []
    try:
        with open(path) as f:
            d = json.load(f)
    except Exception as e:  # noqa: BLE001
        return [f"JSON does not parse: {e}"], []

    is_clipboard = d.get("source") == "bricksCopiedElements"
    is_template = "type" in d and not is_clipboard
    if not is_clipboard and not is_template:
        errors.append("neither clipboard (source: bricksCopiedElements) nor template (type) format")
    if is_clipboard and "version" not in d:
        warns.append("clipboard JSON has no 'version'")

    classes = d.get("globalClasses", d.get("global_classes", [])) or []
    class_ids = set()
    class_names = {c.get("id"): str(c.get("name", "")) for c in classes if isinstance(c, dict)}
    for c in classes:
        if not isinstance(c, dict) or "id" not in c or "name" not in c:
            errors.append(f"global class missing id/name: {c!r}"[:160])
            continue
        if c["id"] in class_ids:
            errors.append(f"duplicate global class id {c['id']}")
        class_ids.add(c["id"])
        check_settings(f"class .{c['name']}", c.get("settings", {}), errors, warns, False, set())
        if framework:
            if not BEM_RE.match(str(c["name"])):
                errors.append(f"class '{c['name']}' is not a BEM name (block__element--modifier, lowercase)")
            check_framework(f"class .{c['name']}", c.get("settings", {}), errors, warns, True)

    all_ids = set()
    found_any = False
    for listname, els in element_lists(d):
        found_any = True
        byid = {}
        for e in els:
            eid = e.get("id")
            for req in ("id", "name", "parent", "children", "settings"):
                if req not in e:
                    errors.append(f"[{listname}] element {eid}: missing '{req}'")
            if eid in all_ids:
                errors.append(f"duplicate element id {eid}")
            all_ids.add(eid)
            byid[eid] = e
            if eid and not ID_RE.match(str(eid)):
                warns.append(f"element id '{eid}' is not 6-char alphanumeric")
        for e in els:
            eid, parent = e.get("id"), e.get("parent")
            if parent not in (0, "0"):
                if parent not in byid:
                    errors.append(f"{eid}: parent '{parent}' not found")
                elif eid not in byid[parent].get("children", []):
                    errors.append(f"{eid}: parent '{parent}' doesn't list it as a child")
            elif e.get("name") != "section" and listname == "content" and is_clipboard:
                warns.append(f"{eid}: root element is '{e.get('name')}', usually a section")
            for c in e.get("children", []):
                if c not in byid:
                    errors.append(f"{eid}: child '{c}' not found")
                elif byid[c].get("parent") != eid:
                    errors.append(f"{eid}: child '{c}' points to parent '{byid[c].get('parent')}'")
            if e.get("name") == "section" and parent not in (0, "0"):
                errors.append(f"{eid}: section nested inside '{parent}'")
            s = e.get("settings", {})
            check_settings(f"{e.get('name')}#{eid}", s, errors, warns, e.get("name") in LAYOUT, set())
            if framework:
                check_framework(f"{e.get('name')}#{eid}", s, errors, warns, False)
                if e.get("name") == "container" and isinstance(s, dict):
                    names = [class_names.get(c, "") for c in s.get("_cssGlobalClasses", []) or []]
                    if names and not any(n.endswith("__container") for n in names):
                        errors.append(f"{eid}: Container's BEM class must be '{{block}}__container' (got {', '.join(names)})")
                if e.get("name") == "section":
                    lbl = str(e.get("label", "")).strip()
                    if not lbl or lbl.lower() == "section":
                        errors.append(f"{eid}: section needs a purpose label (Hero, Features, CTA, Pricing...)")
            if isinstance(s, dict):
                for cid in s.get("_cssGlobalClasses", []) or []:
                    if cid not in class_ids:
                        errors.append(f"{eid}: global class id '{cid}' not in globalClasses")
                if s.get("hasLoop") and not (isinstance(s.get("query"), dict) and s["query"].get("objectType")):
                    warns.append(f"{eid}: hasLoop without query.objectType")
        h1s = [e for e in els if e.get("name") == "heading" and e.get("settings", {}).get("tag") == "h1"]
        if len(h1s) > 1:
            warns.append(f"[{listname}] {len(h1s)} h1 headings")
    if not found_any:
        errors.append("no element array found (content/header/footer)")
    return errors, warns


def main():
    args = sys.argv[1:]
    framework = "--upstream" not in args
    paths = [a for a in args if a != "--upstream"]
    if not paths:
        print(__doc__)
        sys.exit(2)
    if framework and not TOKENS:
        print(f"WARN  could not read tokens from {TOKENS_FILE}; token-name check disabled")
    failed = False
    for path in paths:
        errors, warns = validate(path, framework)
        status = "FAIL" if errors else "OK"
        print(f"{status}  {path}  ({len(errors)} errors, {len(warns)} warnings)")
        for m in errors:
            print(f"  ERROR {m}")
        for m in warns:
            print(f"  WARN  {m}")
        failed = failed or bool(errors)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
