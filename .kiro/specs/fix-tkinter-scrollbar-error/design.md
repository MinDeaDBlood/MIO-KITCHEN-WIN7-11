# Design: Fix Tkinter Scrollbar Lifecycle Error

## Solution Overview

The fix modifies the `ListBox` and `ScrollFrame` classes in `src/tkui/controls.py` to properly manage scrollbar lifecycle by:
1. Storing scrollbar as instance variable
2. Disconnecting canvas-scrollbar binding before destruction
3. Adding defensive checks with `winfo_exists()`
4. Implementing custom `destroy()` methods

## Architecture

### Current Implementation (Problematic)
```python
class ListBox(Frame):
    def gui(self):
        scrollbar = Scrollbar(self, orient='vertical')  # Local variable
        self.canvas.config(yscrollcommand=scrollbar.set)
        # When widget is destroyed, canvas still references scrollbar
```

### New Implementation (Fixed)
```python
class ListBox(Frame):
    def gui(self):
        self.scrollbar = Scrollbar(self, orient='vertical')  # Instance variable
        self.canvas.config(yscrollcommand=self.scrollbar.set)
    
    def destroy(self):
        # Disconnect binding before destruction
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            try:
                self.canvas.config(yscrollcommand='')
            except tk.TclError:
                pass
        super().destroy()
```

## Component Changes

### 1. ListBox Class (`src/tkui/controls.py`)

#### Modified Methods

**`gui()` method (lines 62-82):**
```python
def gui(self):
    self.canvas = Canvas(self, bg=self.bg, highlightthickness=0)
    self.scrollbar = Scrollbar(self, orient='vertical')  # Changed from local to instance
    self.label_frame = Frame(self.canvas, bg=self.bg)
    
    self.canvas.config(yscrollcommand=self.scrollbar.set)  # Use self.scrollbar
    self.scrollbar.config(command=self.canvas.yview)  # Use self.scrollbar
    
    # ... rest of the method
    
    self.scrollbar.pack(side='right', fill='y')  # Use self.scrollbar
```

**New `destroy()` method (after line 60):**
```python
def destroy(self):
    """Safely destroy the ListBox widget by disconnecting canvas-scrollbar binding."""
    try:
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.config(yscrollcommand='')
    except tk.TclError:
        # Widget already destroyed or in process of destruction
        pass
    super().destroy()
```

**Updated `clear()` method (lines 53-60):**
```python
def clear(self):
    """Clear all items from the ListBox."""
    for widget in self.loaded_value:
        if widget.winfo_exists():  # Check before destroying
            widget.destroy()
    self.loaded_value.clear()  # Clear the list to prevent memory leaks
```

**Updated `update_ui()` method (lines 84-86):**
```python
def update_ui(self):
    """Update the canvas scroll region."""
    try:
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            if hasattr(self, 'label_frame') and self.label_frame.winfo_exists():
                self.canvas.config(scrollregion=self.canvas.bbox('all'))
    except tk.TclError:
        pass
```

### 2. ScrollFrame Class (`src/tkui/controls.py`)

#### Modified Methods

**`gui()` method (lines 130-141):**
```python
def gui(self):
    self.canvas = Canvas(self, bg=self.bg, highlightthickness=0)
    self.scrollbar = Scrollbar(self, orient='vertical')  # Changed from local to instance
    self.label_frame = Frame(self.canvas, bg=self.bg)
    
    self.canvas.config(yscrollcommand=self.scrollbar.set)  # Use self.scrollbar
    self.scrollbar.config(command=self.canvas.yview)  # Use self.scrollbar
    
    # ... rest of the method
    
    self.scrollbar.pack(side='right', fill='y')  # Use self.scrollbar
```

**New `destroy()` method (after line 128):**
```python
def destroy(self):
    """Safely destroy the ScrollFrame widget by disconnecting canvas-scrollbar binding."""
    try:
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.config(yscrollcommand='')
    except tk.TclError:
        # Widget already destroyed or in process of destruction
        pass
    super().destroy()
```

**Updated `update_ui()` method (lines 143-145):**
```python
def update_ui(self):
    """Update the canvas scroll region."""
    try:
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            if hasattr(self, 'label_frame') and self.label_frame.winfo_exists():
                self.canvas.config(scrollregion=self.canvas.bbox('all'))
    except tk.TclError:
        pass
```

## Error Handling Strategy

### Three-Layer Defense

1. **Instance Variable Storage**: Prevents premature garbage collection
2. **Existence Checks**: `winfo_exists()` verifies widget is still valid
3. **Exception Handling**: `try-except` catches TclError during destruction

### Destruction Sequence
```
User closes window
    ↓
Toplevel.destroy() called
    ↓
ListBox.destroy() called
    ↓
Check if canvas exists (winfo_exists)
    ↓
Disconnect yscrollcommand
    ↓
Call super().destroy()
    ↓
Scrollbar destroyed safely
```

## Compatibility Considerations

### Python Version
- Requires Python 3.8+ (already required by project)
- Uses standard Tkinter methods available in all versions

### Platform Compatibility
- **Windows 7**: Tcl/Tk 8.6.x - handles slower destruction timing
- **Windows 11**: Tcl/Tk 8.6.x+ - handles faster destruction timing
- No platform-specific code needed

### Theme Compatibility
- Works with both light and dark themes
- No visual changes to widgets
- Maintains existing styling

## Testing Strategy

### Unit Testing Approach
- Test `destroy()` method with existing canvas
- Test `destroy()` method with already-destroyed canvas
- Test `clear()` method multiple times
- Test `update_ui()` during destruction

### Integration Testing
- Open/close DisableAVB window 10 times
- Open/close DisableEncryption window 10 times
- Rapid open/close of multiple windows
- Background thread operations during window close

### Regression Testing
- Verify all existing ListBox functionality works
- Verify all existing ScrollFrame functionality works
- Check theme switching still works
- Verify scrolling behavior unchanged

## Performance Impact

- **Minimal**: Only adds lightweight checks
- **No overhead** during normal operation
- **Faster cleanup**: Prevents error handling overhead
- **Memory**: Prevents potential memory leaks from orphaned references

## Rollback Plan

If issues arise:
1. Revert changes to `src/tkui/controls.py`
2. Original code is preserved in git history
3. No database or configuration changes needed
4. No user data affected

## Success Metrics

- Zero `_tkinter.TclError` occurrences in logs
- No user reports of window closing errors
- Stable memory usage over time
- No performance degradation
