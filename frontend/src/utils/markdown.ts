// Markdown snippet templates
export const markdownSnippets = {
  bold: '**bold text**',
  italic: '*italic text*',
  h1: '\n# Header 1\n',
  h2: '\n## Header 2\n',
  h3: '\n### Header 3\n',
  h4: '\n#### Header 4\n',
  link: '[link text](url)',
  image: '![alt text](image-url)',
  code: '`inline code`',
  codeBlock: '\n```language\n// code block\n```\n',
  quote: '\n> Quote\n',
  list: '\n- List item\n',
  numberedList: '\n1. First item\n',
  table: '\n| Header 1 | Header 2 |\n|----------|----------|\n| Cell 1   | Cell 2   |\n',
  hr: '\n---\n',
  checkbox: '\n- [ ] Task item\n',
  strikethrough: '~~strikethrough~~',
};

// Insert markdown snippet at cursor position
export const insertSnippet = (
  content: string,
  cursorPosition: number,
  snippet: string
): { newContent: string; newCursorPosition: number } => {
  const before = content.substring(0, cursorPosition);
  const after = content.substring(cursorPosition);
  const newContent = before + snippet + after;
  const newCursorPosition = cursorPosition + snippet.length;

  return { newContent, newCursorPosition };
};

// Wrap selected text with markdown syntax
export const wrapSelection = (
  content: string,
  selectionStart: number,
  selectionEnd: number,
  prefix: string,
  suffix?: string
): { newContent: string; newSelectionStart: number; newSelectionEnd: number } => {
  const before = content.substring(0, selectionStart);
  const selected = content.substring(selectionStart, selectionEnd);
  const after = content.substring(selectionEnd);

  const actualSuffix = suffix || prefix;
  const newContent = before + prefix + selected + actualSuffix + after;

  return {
    newContent,
    newSelectionStart: selectionStart + prefix.length,
    newSelectionEnd: selectionEnd + prefix.length,
  };
};

// Download file helper
export const downloadFile = (content: string, filename: string) => {
  const blob = new Blob([content], { type: 'text/markdown' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};

// Copy to clipboard helper
export const copyToClipboard = async (text: string): Promise<boolean> => {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (err) {
    console.error('Failed to copy:', err);
    return false;
  }
};

// Debounce utility for preview updates
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout> | null = null;

  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      timeout = null;
      func(...args);
    };

    if (timeout) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(later, wait);
  };
}
