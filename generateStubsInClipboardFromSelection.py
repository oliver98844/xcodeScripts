#!/usr/bin/python

def sendToClipBoard(string):
    from AppKit import NSPasteboard, NSObject, NSStringPboardType
    pasteboard = NSPasteboard.generalPasteboard()
    emptyOwner = NSObject.alloc().init()
    pasteboard.declareTypes_owner_([NSStringPboardType], emptyOwner)
    pasteboard.setString_forType_(string, NSStringPboardType)

def generateSelectedMethodStubs():
    from Foundation import NSAppleScript, objc
    getSelectedTextAppleScript = '''
        tell application \"Xcode\"
        set current_document to text document 1 whose name ends with (word -1 of (get name of window 1))
        tell current_document
            set documentContent to (get text of contents)
            set {startIdx, endIdx} to selected character range
            set len to endIdx - startIdx
            if (len > -1) then
                set selectedText to (text startIdx thru endIdx of documentContent)
            else
                set selectedText to \"\"
            end if
            return selectedText
            end tell
        end tell'''
    appleScript = NSAppleScript.alloc().initWithSource_(getSelectedTextAppleScript)
    result = appleScript.executeAndReturnError_(objc.nil)
    selected_text = result[0].stringValue()
    selected_stubs = selected_text.replace(";", "\n{\n}\n")
    while selected_stubs.endswith('\n'): selected_stubs = selected_stubs[:-1]
    return selected_stubs

if __name__ == "__main__":
    text = generateSelectedMethodStubs()
    sendToClipBoard(text)
