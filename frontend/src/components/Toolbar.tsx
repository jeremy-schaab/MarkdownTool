import {
  Bold,
  Italic,
  Code,
  List,
  ListOrdered,
  Quote,
  Link,
  Image,
  Table,
  CheckSquare,
  Minus,
  Heading1,
  Heading2,
  Heading3,
  FileCode,
} from 'lucide-react';

interface ToolbarProps {
  onInsert: (type: string) => void;
}

export function Toolbar({ onInsert }: ToolbarProps) {
  const buttons = [
    { icon: Bold, label: 'Bold', type: 'bold', shortcut: 'Ctrl+B' },
    { icon: Italic, label: 'Italic', type: 'italic', shortcut: 'Ctrl+I' },
    { icon: Heading1, label: 'Header 1', type: 'h1' },
    { icon: Heading2, label: 'Header 2', type: 'h2' },
    { icon: Heading3, label: 'Header 3', type: 'h3' },
    { icon: Link, label: 'Link', type: 'link' },
    { icon: Code, label: 'Inline Code', type: 'code' },
    { icon: FileCode, label: 'Code Block', type: 'codeBlock' },
    { icon: List, label: 'Bullet List', type: 'list' },
    { icon: ListOrdered, label: 'Numbered List', type: 'numberedList' },
    { icon: CheckSquare, label: 'Task List', type: 'checkbox' },
    { icon: Quote, label: 'Quote', type: 'quote' },
    { icon: Image, label: 'Image', type: 'image' },
    { icon: Table, label: 'Table', type: 'table' },
    { icon: Minus, label: 'Horizontal Rule', type: 'hr' },
  ];

  return (
    <div className="flex items-center gap-1 p-2 bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex-wrap">
      {buttons.map(({ icon: Icon, label, type, shortcut }) => (
        <button
          key={type}
          onClick={() => onInsert(type)}
          className="p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors group relative"
          title={`${label}${shortcut ? ` (${shortcut})` : ''}`}
          aria-label={label}
        >
          <Icon className="w-4 h-4 text-gray-700 dark:text-gray-300" />
        </button>
      ))}
    </div>
  );
}
