# Tasks: Fix Tkinter Scrollbar Lifecycle Error

## Task List

- [x] 1. Fix ListBox class in src/tkui/controls.py
  - [x] 1.1 Modify gui() method to use instance variable for scrollbar
  - [x] 1.2 Add custom destroy() method
  - [x] 1.3 Update clear() method with winfo_exists() checks
  - [x] 1.4 Update update_ui() method with defensive checks

- [x] 2. Fix ScrollFrame class in src/tkui/controls.py
  - [x] 2.1 Modify gui() method to use instance variable for scrollbar
  - [x] 2.2 Add custom destroy() method
  - [x] 2.3 Update update_ui() method with defensive checks

- [ ] 3. Test the fixes
  - [ ] 3.1 Test closing DisableAVB window multiple times
  - [ ] 3.2 Test closing DisableEncryption window multiple times
  - [ ] 3.3 Test rapid window open/close operations
  - [ ] 3.4 Test clear() method multiple times
  - [ ] 3.5 Verify no TclError in console logs

- [ ] 4. Verify compatibility
  - [ ] 4.1 Test on Windows 7 (if available)
  - [ ] 4.2 Test on Windows 11
  - [ ] 4.3 Test with light theme
  - [ ] 4.4 Test with dark theme

## Task Details

### Task 1.1: Modify ListBox.gui() method
**File**: `src/tkui/controls.py`
**Lines**: 62-82

Change scrollbar from local variable to instance variable:
- Line 67: `scrollbar = Scrollbar(...)` → `self.scrollbar = Scrollbar(...)`
- Line 71: `yscrollcommand=scrollbar.set` → `yscrollcommand=self.scrollbar.set`
- Line 72: `scrollbar.config(...)` → `self.scrollbar.config(...)`
- Line 79: `scrollbar.pack(...)` → `self.scrollbar.pack(...)`

### Task 1.2: Add ListBox.destroy() method
**File**: `src/tkui/controls.py`
**Location**: After line 60 (after clear() method)

Add new method:
```python
def destroy(self):
    """Safely destroy the ListBox widget by disconnecting canvas-scrollbar binding."""
    try:
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.config(yscrollcommand='')
    except tk.TclError:
        pass
    super().destroy()
```

### Task 1.3: Update ListBox.clear() method
**File**: `src/tkui/controls.py`
**Lines**: 53-60

Add winfo_exists() check and clear list:
```python
def clear(self):
    for widget in self.loaded_value:
        if widget.winfo_exists():
            widget.destroy()
    self.loaded_value.clear()
```

### Task 1.4: Update ListBox.update_ui() method
**File**: `src/tkui/controls.py`
**Lines**: 84-86

Add defensive checks:
```python
def update_ui(self):
    try:
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            if hasattr(self, 'label_frame') and self.label_frame.winfo_exists():
                self.canvas.config(scrollregion=self.canvas.bbox('all'))
    except tk.TclError:
        pass
```

### Task 2.1: Modify ScrollFrame.gui() method
**File**: `src/tkui/controls.py`
**Lines**: 130-141

Same changes as Task 1.1 but for ScrollFrame class.

### Task 2.2: Add ScrollFrame.destroy() method
**File**: `src/tkui/controls.py`
**Location**: After line 128 (after clear() method)

Same implementation as Task 1.2 but for ScrollFrame class.

### Task 2.3: Update ScrollFrame.update_ui() method
**File**: `src/tkui/controls.py`
**Lines**: 143-145

Same implementation as Task 1.4 but for ScrollFrame class.

### Task 3: Testing Tasks
**Manual testing steps**:
1. Run the application
2. Open DisableAVB window and close it 10 times
3. Open DisableEncryption window and close it 10 times
4. Rapidly open and close multiple windows
5. Check console for any TclError messages
6. Verify normal functionality is preserved

### Task 4: Compatibility Testing
**Testing checklist**:
- [ ] Windows 7 with Python 3.8.10
- [ ] Windows 11 with Python 3.8.10+
- [ ] Light theme enabled
- [ ] Dark theme enabled
- [ ] No errors in console
- [ ] Smooth window closing behavior

## Estimated Time
- Task 1: 30 minutes
- Task 2: 20 minutes
- Task 3: 30 minutes
- Task 4: 20 minutes
- **Total**: ~2 hours

## Dependencies
- None - all changes are self-contained in `src/tkui/controls.py`

## Risks
- **Low risk**: Changes are isolated to widget lifecycle management
- **Mitigation**: Extensive testing before deployment
- **Rollback**: Simple git revert if issues arise
