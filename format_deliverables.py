"""Reformat deliverables to have proper line wrapping (80 char max)."""

import textwrap
from pathlib import Path


def wrap_text(text, width=78):
    """Wrap text to specified width while preserving structure."""
    lines = text.split('\n')
    wrapped_lines = []

    for line in lines:
        # Preserve empty lines
        if not line.strip():
            wrapped_lines.append('')
            continue

        # Preserve lines that are headers or separators
        if line.startswith('=') or line.startswith('-') or line.startswith('│'):
            wrapped_lines.append(line)
            continue

        # Preserve bullet points and numbered lists
        if line.strip().startswith(('•', '*', '-', '1.', '2.', '3.', '4.', '5.', '6.')):
            # Get indent
            indent = len(line) - len(line.lstrip())
            prefix = line[:indent]

            # Wrap with hanging indent
            wrapped = textwrap.fill(
                line,
                width=width,
                initial_indent='',
                subsequent_indent=prefix + '  ',
                break_long_words=False,
                break_on_hyphens=False
            )
            wrapped_lines.append(wrapped)
            continue

        # Regular paragraph wrapping
        if len(line) > width:
            # Preserve indent
            indent = len(line) - len(line.lstrip())
            prefix = ' ' * indent

            wrapped = textwrap.fill(
                line.strip(),
                width=width,
                initial_indent=prefix,
                subsequent_indent=prefix,
                break_long_words=False,
                break_on_hyphens=False
            )
            wrapped_lines.append(wrapped)
        else:
            wrapped_lines.append(line)

    return '\n'.join(wrapped_lines)


def format_file(filepath):
    """Format a single file."""
    with open(filepath, 'r') as f:
        content = f.read()

    formatted = wrap_text(content)

    with open(filepath, 'w') as f:
        f.write(formatted)

    print(f"✓ Formatted: {filepath.name}")


def main():
    """Format all text files in deliverables."""
    deliverables_dir = Path('deliverables')

    txt_files = list(deliverables_dir.glob('*.txt'))

    if not txt_files:
        print("No .txt files found in deliverables/")
        return

    print(f"\nFormatting {len(txt_files)} files...\n")

    for filepath in txt_files:
        format_file(filepath)

    print(f"\n✓ All files formatted with 78-character line width!\n")


if __name__ == "__main__":
    main()
