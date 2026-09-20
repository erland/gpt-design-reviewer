from __future__ import annotations

import ast
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

DEFAULT_IGNORED_DIRS = {
    '.git', '.hg', '.svn', '.idea', '.vscode', '__pycache__', '.pytest_cache',
    '.mypy_cache', '.ruff_cache', 'node_modules', 'dist', 'build', 'target',
    'coverage', '.next', '.nuxt', '.gradle', '.venv', 'venv', 'vendor',
}

TEXT_EXTENSIONS = {
    '.py', '.pyi', '.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs', '.java', '.kt', '.kts',
    '.go', '.rs', '.cs', '.c', '.h', '.cc', '.cpp', '.hpp', '.rb', '.php', '.swift',
    '.scala', '.sh', '.bash', '.zsh', '.sql', '.graphql', '.gql', '.html', '.css', '.scss',
    '.less', '.vue', '.svelte', '.md', '.rst', '.txt', '.yaml', '.yml', '.json', '.toml',
    '.xml', '.properties', '.gradle', '.conf', '.ini', '.env', '.dockerfile',
}

SOURCE_EXTENSIONS = {
    '.py', '.pyi', '.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs', '.java', '.kt', '.kts',
    '.go', '.rs', '.cs', '.c', '.h', '.cc', '.cpp', '.hpp', '.rb', '.php', '.swift',
    '.scala', '.vue', '.svelte', '.sql',
}

IMPORT_PATTERNS = {
    'javascript': re.compile(r"(?:import\s+(?:[^'\"]+?\s+from\s+)?|require\s*\()\s*['\"]([^'\"]+)['\"]"),
    'java': re.compile(r'^\s*import\s+(?:static\s+)?([\w.*]+)\s*;', re.MULTILINE),
    'kotlin': re.compile(r'^\s*import\s+([\w.*]+)', re.MULTILINE),
    'go': re.compile(r'^\s*import\s+(?:\w+\s+)?["`]([^"`]+)["`]', re.MULTILINE),
    'csharp': re.compile(r'^\s*using\s+([\w.]+)\s*;', re.MULTILINE),
}

FUNC_PATTERNS = {
    'javascript': re.compile(r'(?m)^\s*(?:export\s+)?(?:async\s+)?(?:function\s+([A-Za-z_$][\w$]*)\s*\([^)]*\)|(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)'),
    'java_like': re.compile(r'(?m)^\s*(?:public|protected|private|static|final|synchronized|abstract|native|default|open|internal|override|suspend|inline|external|operator|infix|tailrec|\s)+\s*[\w<>,.?\[\]]+\s+([A-Za-z_$][\w$]*)\s*\([^;{}]*\)\s*(?:throws\s+[^{]+)?\{'),
    'go': re.compile(r'(?m)^\s*func\s+(?:\([^)]*\)\s*)?([A-Za-z_]\w*)\s*\([^)]*\)'),
    'rust': re.compile(r'(?m)^\s*(?:pub(?:\([^)]*\))?\s+)?(?:async\s+)?fn\s+([A-Za-z_]\w*)\s*\('),
}

@dataclass
class FileRecord:
    path: str
    extension: str
    bytes: int
    lines: int | None
    nonblank_lines: int | None
    sha256: str | None
    source: bool
    parse_error: str | None = None


def is_probably_text(path: Path) -> bool:
    if path.name.lower() == 'dockerfile':
        return True
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    try:
        chunk = path.read_bytes()[:4096]
    except OSError:
        return False
    if b'\x00' in chunk:
        return False
    if not chunk:
        return True
    printable = sum((32 <= b < 127) or b in (9, 10, 13) for b in chunk)
    return printable / len(chunk) > 0.92


def walk_files(root: Path, ignored_dirs: set[str] | None = None) -> Iterable[Path]:
    ignored = DEFAULT_IGNORED_DIRS | (ignored_dirs or set())
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(root).parts
        if any(part in ignored for part in rel_parts[:-1]):
            continue
        yield path


def read_text(path: Path, max_bytes: int = 5_000_000) -> tuple[str | None, str | None]:
    try:
        if path.stat().st_size > max_bytes:
            return None, f'skipped: file exceeds {max_bytes} bytes'
        data = path.read_bytes()
        if b'\x00' in data[:4096]:
            return None, 'skipped: binary content detected'
        return data.decode('utf-8', errors='replace'), None
    except OSError as exc:
        return None, f'read error: {exc}'


def file_record(root: Path, path: Path) -> FileRecord:
    rel = path.relative_to(root).as_posix()
    size = path.stat().st_size
    ext = path.suffix.lower() or ('dockerfile' if path.name.lower() == 'dockerfile' else '')
    source = ext in SOURCE_EXTENSIONS
    if not is_probably_text(path):
        return FileRecord(rel, ext, size, None, None, None, source)
    text, err = read_text(path)
    if text is None:
        return FileRecord(rel, ext, size, None, None, None, source, err)
    lines = text.splitlines()
    digest = hashlib.sha256(text.encode('utf-8', errors='replace')).hexdigest()
    return FileRecord(rel, ext, size, len(lines), sum(bool(x.strip()) for x in lines), digest, source, err)


def python_functions(text: str) -> tuple[list[dict], str | None]:
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return [], f'python syntax error: {exc.msg} at line {exc.lineno}'
    result = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            end = getattr(node, 'end_lineno', node.lineno)
            result.append({'name': node.name, 'start_line': node.lineno, 'end_line': end, 'lines': max(1, end - node.lineno + 1), 'confidence': 'high'})
    return result, None


def brace_function_extents(text: str, pattern: re.Pattern, names_by_group: bool = False) -> list[dict]:
    lines = text.splitlines()
    starts = []
    for match in pattern.finditer(text):
        name = next((g for g in match.groups() if g), '<anonymous>') if names_by_group else (match.group(1) or '<anonymous>')
        line = text.count('\n', 0, match.start()) + 1
        starts.append((line, name))
    result = []
    for line, name in starts:
        depth = 0
        seen_open = False
        end_line = line
        for idx in range(line - 1, min(len(lines), line - 1 + 2000)):
            stripped = re.sub(r'//.*$', '', lines[idx])
            for ch in stripped:
                if ch == '{':
                    depth += 1; seen_open = True
                elif ch == '}' and seen_open:
                    depth -= 1
            end_line = idx + 1
            if seen_open and depth <= 0:
                break
        result.append({'name': name, 'start_line': line, 'end_line': end_line, 'lines': max(1, end_line - line + 1), 'confidence': 'heuristic'})
    return result


def functions_for_file(path: Path, text: str) -> tuple[list[dict], str | None]:
    ext = path.suffix.lower()
    if ext in {'.py', '.pyi'}:
        return python_functions(text)
    if ext in {'.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs'}:
        return brace_function_extents(text, FUNC_PATTERNS['javascript'], names_by_group=True), None
    if ext in {'.java', '.kt', '.kts', '.cs'}:
        return brace_function_extents(text, FUNC_PATTERNS['java_like']), None
    if ext == '.go':
        return brace_function_extents(text, FUNC_PATTERNS['go']), None
    if ext == '.rs':
        return brace_function_extents(text, FUNC_PATTERNS['rust']), None
    return [], None


def imports_for_file(path: Path, text: str) -> list[str]:
    ext = path.suffix.lower()
    if ext in {'.py', '.pyi'}:
        try:
            tree = ast.parse(text)
        except SyntaxError:
            return []
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
        return sorted(set(imports))
    if ext in {'.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs'}:
        return sorted(set(IMPORT_PATTERNS['javascript'].findall(text)))
    if ext == '.java':
        return sorted(set(IMPORT_PATTERNS['java'].findall(text)))
    if ext in {'.kt', '.kts'}:
        return sorted(set(IMPORT_PATTERNS['kotlin'].findall(text)))
    if ext == '.go':
        return sorted(set(IMPORT_PATTERNS['go'].findall(text)))
    if ext == '.cs':
        return sorted(set(IMPORT_PATTERNS['csharp'].findall(text)))
    return []


def normalized_duplicate_blocks(text: str, min_lines: int = 8, max_blocks: int = 25000) -> list[tuple[str, int, str]]:
    raw = text.splitlines()
    normalized = []
    original_lines = []
    for i, line in enumerate(raw, 1):
        s = line.strip()
        if not s or s.startswith(('//', '#', '*', '/*', '--')):
            continue
        s = re.sub(r'\s+', ' ', s)
        normalized.append(s)
        original_lines.append(i)
    if len(normalized) < min_lines:
        return []
    out = []
    for idx in range(0, len(normalized) - min_lines + 1, min_lines):
        block = '\n'.join(normalized[idx:idx + min_lines])
        if len(block) < 120:
            continue
        digest = hashlib.sha256(block.encode()).hexdigest()
        out.append((digest, original_lines[idx], block[:240]))
        if len(out) >= max_blocks:
            break
    return out


def analyze_tree(root: Path, large_file_lines: int = 500, large_function_lines: int = 80, duplicate_block_lines: int = 8) -> dict:
    root = root.resolve()
    records: list[FileRecord] = []
    extension_counts = Counter()
    dir_counts = Counter()
    functions: list[dict] = []
    imports: list[dict] = []
    errors: list[dict] = []
    duplicate_map: dict[str, list[dict]] = defaultdict(list)

    for path in walk_files(root):
        try:
            rec = file_record(root, path)
            records.append(rec)
            extension_counts[rec.extension or '<none>'] += 1
            rel = path.relative_to(root)
            dir_counts[rel.parts[0] if len(rel.parts) > 1 else '.'] += 1
            if rec.parse_error:
                errors.append({'path': rec.path, 'stage': 'read', 'message': rec.parse_error})
            if rec.lines is None or not rec.source:
                continue
            text, read_err = read_text(path)
            if text is None:
                if read_err:
                    errors.append({'path': rec.path, 'stage': 'read', 'message': read_err})
                continue
            funcs, parse_err = functions_for_file(path, text)
            if parse_err:
                errors.append({'path': rec.path, 'stage': 'function_scan', 'message': parse_err})
            for f in funcs:
                f['path'] = rec.path
                functions.append(f)
            imps = imports_for_file(path, text)
            if imps:
                imports.append({'path': rec.path, 'imports': imps})
            for digest, line, preview in normalized_duplicate_blocks(text, duplicate_block_lines):
                duplicate_map[digest].append({'path': rec.path, 'line': line, 'preview': preview})
        except Exception as exc:  # best-effort evidence collection; one file must not abort the run
            errors.append({'path': str(path), 'stage': 'file_analysis', 'message': f'{type(exc).__name__}: {exc}'})

    duplicates = []
    for digest, occurrences in duplicate_map.items():
        unique_paths = {o['path'] for o in occurrences}
        if len(occurrences) >= 2 and len(unique_paths) >= 2:
            duplicates.append({'fingerprint': digest[:16], 'occurrences': occurrences[:20]})
    duplicates.sort(key=lambda d: (-len(d['occurrences']), d['fingerprint']))

    large_files = [asdict(r) for r in records if r.lines is not None and r.source and r.lines >= large_file_lines]
    large_files.sort(key=lambda r: (-int(r['lines'] or 0), r['path']))
    large_functions = [f for f in functions if f['lines'] >= large_function_lines]
    large_functions.sort(key=lambda f: (-f['lines'], f['path'], f['start_line']))

    total_lines = sum(r.lines or 0 for r in records)
    source_lines = sum(r.lines or 0 for r in records if r.source)
    return {
        'schema_version': 1,
        'tool': 'design-reviewer-source-inventory',
        'root': str(root),
        'semantics': {
            'purpose': 'deterministic evidence only',
            'warning': 'Indicators are hotspots, not design conclusions. Semantic review is required before creating DR observations.',
        },
        'summary': {
            'files': len(records),
            'source_files': sum(r.source for r in records),
            'total_text_lines': total_lines,
            'source_lines': source_lines,
            'extensions': dict(sorted(extension_counts.items())),
            'top_level_entries': dict(sorted(dir_counts.items())),
        },
        'indicators': {
            'large_files_threshold_lines': large_file_lines,
            'large_files': large_files,
            'large_functions_threshold_lines': large_function_lines,
            'large_functions': large_functions,
            'imports': imports,
            'duplicate_block_lines': duplicate_block_lines,
            'possible_duplicate_blocks': duplicates[:100],
        },
        'files': [asdict(r) for r in records],
        'errors': errors,
    }


def dumps_json(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False, sort_keys=False) + '\n'
