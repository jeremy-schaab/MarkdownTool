# Markdown Manager - React Frontend

Modern, high-performance React frontend for the Markdown Manager application.

## Features

- 🚀 **Fast & Responsive** - Built with React 19 + Vite for instant page loads
- ✏️ **Monaco Editor** - VS Code-powered markdown editing experience
- 👁️ **Live Preview** - Real-time markdown rendering with debouncing
- 📁 **File Browser** - Tree view with search and filtering
- 🎨 **Rich Toolbar** - 15+ formatting buttons for markdown
- 🌓 **Dark Mode** - Automatic theme switching
- 💾 **Auto-save Indication** - Clear visual feedback for unsaved changes
- ⚡ **Resizable Panels** - Customize your layout

## Technology Stack

- **React 19** - Latest React with improved performance
- **TypeScript** - Type-safe development
- **Vite** - Lightning-fast build tool
- **Monaco Editor** - VS Code's editor component
- **Tailwind CSS** - Utility-first styling
- **React Markdown** - GitHub-flavored markdown rendering
- **Lucide Icons** - Beautiful, consistent icons

## Installation

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configuration

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` to set your API URL:

```env
VITE_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

The app will be available at **http://localhost:5173**

## Usage

### Opening a Folder

1. Click "Open Folder" in the header
2. Enter the path to your markdown files folder
3. The file browser will display all `.md` and `.markdown` files

### Editing Files

1. Click on any file in the file browser
2. The Monaco editor will open on the left
3. Live preview appears on the right
4. Use the toolbar for quick formatting

### Saving Changes

- Click the "Save" button (turns blue when changes detected)
- Keyboard shortcut: `Ctrl+S` (coming soon)
- Original file is backed up automatically

### Toolbar Shortcuts

| Button | Function | Output |
|--------|----------|--------|
| **B** | Bold | `**text**` |
| *I* | Italic | `*text*` |
| H1 | Header 1 | `# Header` |
| H2 | Header 2 | `## Header` |
| 🔗 | Link | `[text](url)` |
| `<>` | Code | `` `code` `` |
| ``` | Code Block | ` ```code``` ` |
| • | Bullet List | `- item` |
| 1. | Numbered List | `1. item` |
| ☐ | Task List | `- [ ] task` |
| " | Quote | `> quote` |
| 🖼️ | Image | `![alt](url)` |
| 📊 | Table | Markdown table template |
| — | HR | `---` |

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── FileBrowser.tsx  # File tree navigation
│   │   ├── MarkdownEditor.tsx   # Monaco editor wrapper
│   │   ├── MarkdownPreview.tsx  # Preview renderer
│   │   └── Toolbar.tsx      # Formatting toolbar
│   ├── services/
│   │   └── api.ts           # API client for backend
│   ├── types/
│   │   └── index.ts         # TypeScript type definitions
│   ├── utils/
│   │   └── markdown.ts      # Markdown utilities
│   ├── App.tsx              # Main application component
│   ├── main.tsx             # Entry point
│   └── index.css            # Global styles
├── package.json
├── vite.config.ts
└── tailwind.config.js
```

## Development

### Scripts

```bash
# Development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Code Quality

The project uses:
- **ESLint** - Code linting
- **TypeScript** - Type checking
- **Prettier** - Code formatting (recommended)

## Building for Production

```bash
npm run build
```

The production build will be in the `dist/` folder.

### Serve Production Build

```bash
npm run preview
```

Or use any static file server:

```bash
npx serve dist
```

## Integration with Backend

The frontend communicates with the FastAPI backend at `http://localhost:8000` (configurable via `VITE_API_URL`).

### API Endpoints Used

- `GET /api/files/list` - List markdown files
- `GET /api/files/content` - Read file content
- `POST /api/files/save` - Save file
- `POST /api/files/create` - Create new file
- `DELETE /api/files/delete` - Delete file

See [backend/README.md](../backend/README.md) for full API documentation.

## Performance

| Metric | Value |
|--------|-------|
| **Initial Load** | <1s |
| **File Selection** | <50ms |
| **Typing Latency** | <16ms (60fps) |
| **Preview Update** | Debounced 300ms |
| **Bundle Size** | ~500KB (gzipped) |

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Troubleshooting

### CORS Errors

If you see CORS errors:

1. Ensure backend is running on port 8000
2. Check `VITE_API_URL` in `.env` matches backend URL
3. Verify backend CORS settings in `backend/main.py`

### Monaco Editor Not Loading

Clear browser cache and reload:

```bash
# Clear Vite cache
rm -rf node_modules/.vite
npm run dev
```

### Build Errors

```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

## Keyboard Shortcuts (Planned)

- `Ctrl+S` - Save file
- `Ctrl+B` - Bold selection
- `Ctrl+I` - Italic selection
- `Ctrl+K` - Insert link
- `Ctrl+Shift+C` - Code block
- `Ctrl+/` - Toggle comment

## Future Enhancements

- [ ] AI summarization UI
- [ ] Cloud sync configuration
- [ ] Keyboard shortcuts
- [ ] File upload/drag-drop
- [ ] Search across files
- [ ] Recent files history
- [ ] Git integration
- [ ] Collaborative editing

## License

Same as parent project.

## Contributing

See main [README.md](../README.md) for contribution guidelines.
