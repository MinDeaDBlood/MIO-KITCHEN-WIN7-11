# Fix Tkinter Scrollbar Lifecycle Error

## Overview
Fix the `_tkinter.TclError: invalid command name` error that occurs when closing Toplevel windows containing ListBox and ScrollFrame widgets. The error happens because the canvas tries to update a destroyed scrollbar during widget destruction.

## User Stories

### 1. As a user, I want to close windows without errors
**Acceptance Criteria:**
- When I close a Toplevel window containing a ListBox widget, no TclError occurs
- When I close a Toplevel window containing a ScrollFrame widget, no TclError occurs
- The application continues to function normally after closing windows
- No error messages appear in the console or logs

### 2. As a user, I want the application to work on both Windows 7 and Windows 11
**Acceptance Criteria:**
- The fix works on Windows 7 with Python 3.8.10
- The fix works on Windows 11 with Python 3.8.10+
- No platform-specific code is required
- The fix handles different Tcl/Tk timing variations across Windows versions

### 3. As a user, I want to rapidly open and close windows without issues
**Acceptance Criteria:**
- Multiple rapid window open/close operations don't cause errors
- Calling `clear()` method multiple times on the same ListBox instance is safe
- Widget destruction during background thread operations is handled gracefully
- Memory leaks are prevented by properly clearing widget references

### 4. As a developer, I want proper widget lifecycle management
**Acceptance Criteria:**
- Scrollbar is stored as an instance variable, not a local variable
- Canvas-scrollbar binding is disconnected before widget destruction
- `winfo_exists()` checks prevent operations on destroyed widgets
- Custom `destroy()` method properly cleans up resources
- Error handling with try-except catches TclError during destruction

## Technical Context

### Affected Files
- `src/tkui/controls.py` - Contains `ListBox` and `ScrollFrame` classes

### Root Cause
1. Scrollbar created as local variable instead of instance variable
2. Canvas's `yscrollcommand` maintains reference to destroyed scrollbar
3. During destruction, canvas attempts to update scrollbar position
4. Results in `_tkinter.TclError: invalid command name ".!packsuper.!labelframe4.!listbox.!scrollbar"`

### Error Location
```
File "C:\Program Files\Python38\lib\tkinter\__init__.py", line 1892, in __call__
  return self.func(*args)
File "C:\Program Files\Python38\lib\tkinter\__init__.py", line 3530, in set
  self.tk.call(self._w, 'set', first, last)
_tkinter.TclError: invalid command name ".!packsuper.!labelframe4.!listbox.!scrollbar"
```

## Implementation Requirements

### 1. ListBox Class Modifications
- Store scrollbar as instance variable (`self.scrollbar`)
- Add custom `destroy()` method to disconnect canvas-scrollbar binding
- Add `winfo_exists()` checks in `clear()` and `update_ui()` methods
- Wrap canvas operations in try-except blocks

### 2. ScrollFrame Class Modifications
- Store scrollbar as instance variable (`self.scrollbar`)
- Add custom `destroy()` method with same disconnection logic
- Add defensive checks in `update_ui()` method
- Handle destruction scenarios gracefully

### 3. Compatibility Requirements
- Use standard Tkinter methods available in Python 3.8+
- No platform-specific code needed
- Work with both light and dark themes
- Handle different Tcl/Tk versions transparently

## Testing Scenarios

### Manual Testing
1. Open and close DisableAVB window multiple times
2. Open and close DisableEncryption window multiple times
3. Rapidly open and close multiple Toplevel windows
4. Call `clear()` method multiple times on same ListBox
5. Test with both light and dark themes
6. Test on Windows 7 and Windows 11

### Expected Behavior
- No TclError messages in console
- Windows close smoothly without errors
- Application remains stable after multiple operations
- No memory leaks or resource issues

## Success Criteria
- [ ] No `_tkinter.TclError` when closing windows with ListBox widgets
- [ ] No `_tkinter.TclError` when closing windows with ScrollFrame widgets
- [ ] Works on both Windows 7 and Windows 11
- [ ] Handles rapid window operations without errors
- [ ] Proper resource cleanup prevents memory leaks
- [ ] Code follows existing project patterns and style
