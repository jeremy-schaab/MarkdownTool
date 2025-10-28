import { useRef, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import type { editor } from 'monaco-editor';

interface MarkdownEditorProps {
  value: string;
  onChange: (value: string | undefined) => void;
  onCursorChange?: (position: number) => void;
  readOnly?: boolean;
}

export function MarkdownEditor({
  value,
  onChange,
  onCursorChange,
  readOnly = false,
}: MarkdownEditorProps) {
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null);

  const handleEditorDidMount = (editor: editor.IStandaloneCodeEditor) => {
    editorRef.current = editor;

    // Track cursor position changes
    editor.onDidChangeCursorPosition((e) => {
      const position = editor.getModel()?.getOffsetAt(e.position) || 0;
      onCursorChange?.(position);
    });

    // Focus the editor
    editor.focus();
  };

  // Public method to insert text at cursor
  const insertAtCursor = (text: string) => {
    const editor = editorRef.current;
    if (!editor) return;

    const selection = editor.getSelection();
    if (!selection) return;

    editor.executeEdits('', [
      {
        range: selection,
        text,
        forceMoveMarkers: true,
      },
    ]);

    editor.focus();
  };

  // Public method to wrap selected text
  const wrapSelection = (prefix: string, suffix?: string) => {
    const editor = editorRef.current;
    if (!editor) return;

    const selection = editor.getSelection();
    if (!selection) return;

    const actualSuffix = suffix || prefix;
    const selectedText = editor.getModel()?.getValueInRange(selection) || '';

    editor.executeEdits('', [
      {
        range: selection,
        text: prefix + selectedText + actualSuffix,
        forceMoveMarkers: true,
      },
    ]);

    editor.focus();
  };

  // Expose methods to parent component
  useEffect(() => {
    if (editorRef.current) {
      (window as any).markdownEditor = {
        insertAtCursor,
        wrapSelection,
      };
    }
  }, []);

  return (
    <Editor
      height="100%"
      defaultLanguage="markdown"
      value={value}
      onChange={onChange}
      onMount={handleEditorDidMount}
      theme="vs-dark"
      options={{
        minimap: { enabled: false },
        fontSize: 14,
        lineNumbers: 'on',
        wordWrap: 'on',
        scrollBeyondLastLine: false,
        automaticLayout: true,
        tabSize: 2,
        insertSpaces: true,
        readOnly,
        scrollbar: {
          verticalScrollbarSize: 10,
          horizontalScrollbarSize: 10,
        },
        padding: { top: 16, bottom: 16 },
      }}
    />
  );
}
