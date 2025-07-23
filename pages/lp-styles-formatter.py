import re

# Set of class names treated equal to .lp-template (no space)
equal_classes = {
    'lp-nav', 'lp-hero', 'lp-courses', 'lp-features',
    'lp-trust', 'lp-media', 'lp-testimonials', 'lp-partners',
    'lp-news', 'lp-ambassador', 'lp-footer'
}

def should_skip(sel):
    return sel.startswith('.lp-body') or sel.count(' ') >= 2

def process_selector(sel):
    sel = sel.strip()

    if sel.startswith('section.lp-template'):
        return sel

    if sel.startswith('.lp-template'):
        return sel.replace('.lp-template', 'section.lp-template', 1)

    if should_skip(sel):
        return sel

    if sel.startswith('.'):
        parts = sel.split()
        first = parts[0]
        if first.startswith('.'):
            class_name = first[1:]
            if class_name in equal_classes:
                return f'.lp-template{sel}'

    return f'.lp-template {sel}'

def process_block(css_block):
    def replace_selector_block(match):
        selector_part = match.group(1).strip()
        declarations = match.group(2).strip()

        selectors = [s.strip() for s in selector_part.split(',')]
        new_selectors = [process_selector(s) for s in selectors]
        return ', '.join(new_selectors) + ' ' + declarations

    # Add two newlines after each block
    return re.sub(r'([^{@}][^{]*?)\s*({[^{}]*})', lambda m: replace_selector_block(m) + '\n\n', css_block)

def process_css(css):
    result = ''
    pos = 0

    for match in re.finditer(r'(@[^{]+\{)', css):
        start, end = match.span()
        at_rule_header = match.group(1)

        before = css[pos:start]
        if before.strip():
            result += process_block(before).strip() + '\n\n'

        # Find matching closing brace
        depth = 1
        i = end
        while i < len(css):
            if css[i] == '{':
                depth += 1
            elif css[i] == '}':
                depth -= 1
                if depth == 0:
                    break
            i += 1

        inner_content = css[end:i].strip()
        processed_inner = process_block(inner_content).strip()
        result += f'{at_rule_header}\n{processed_inner}\n}}\n\n'
        pos = i + 1

    remaining = css[pos:].strip()
    if remaining:
        result += process_block(remaining).strip() + '\n\n'

    return result.rstrip() + '\n'

def prefix_selectors(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        css = f.read()

    updated_css = process_css(css)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_css)

# 📄 Replace with your actual file
file_path = 'lp-styles.css'
prefix_selectors(file_path)
