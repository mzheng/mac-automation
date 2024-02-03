on run argv
	set prompt to item 1 of argv
	tell application "Safari"
        activate
        tell front window
            set currentTab to make new tab with properties {URL:"http://chat.openai.com/"}
            set current tab to currentTab
        end tell
    end tell
	delay 2 -- Wait for the page to load, may need to adjust this delay
	tell application "System Events"
		tell process "Safari"
			set frontmost to true
			keystroke prompt
			delay 1
			keystroke return using command down
		end tell
	end tell
end run
