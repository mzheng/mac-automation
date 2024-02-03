on run argv
	set device_code to item 1 of argv
	tell application "Safari"
        activate
        tell front window
            set currentTab to make new tab with properties {URL:"https://microsoft.com/devicelogin"}
            set current tab to currentTab
        end tell
    end tell
	delay 2 -- Wait for the page to load, may need to adjust this delay
	tell application "System Events"
		tell process "Safari"
			set frontmost to true
			keystroke device_code
			delay 1
			keystroke return using command down
			delay 5
			keystroke return using command down
			delay 3
			keystroke return using command down
		end tell
	end tell

	delay 5 -- Wait for any post-action processing, adjust as needed
    tell application "Safari"
        tell front window
            close currentTab
        end tell
    end tell
end run
