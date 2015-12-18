vusion.conf can be found at _/etc/vusion/vusion.conf_ or at a location of your choice if you specify it on the command line.

# Structure #
The file is split into sections. Each section is defined by a name in square-brackets. eg:
```
[SECTION NAME]
variable = value
```

## Window Section ##
  * single\_mode - Single mode is a boolean value telling vusion to start with two windows for [Dual Mode](Dual_Mode.md) or one.

## MIDI Section ##
  * device - The MIDI device. You can use the command _vusion-list-midi_ to list the midi device numbers.

## Keyboard Section ##
The keyboard section is only used when in [Dual Mode](Dual_Mode.md). If its not in Dual Mode you will have to control Vusion by a MIDI controller only.

  * viewer\_live - The key that selects the live video feeds
  * viewer\_video - The key that selects videos
  * viewer\_image - The key that selects images
  * viewer\_surface - The key that selects a surface in the preview window
  * viewer\_capture - Captures video if the selected surface contains a live video feed.
  * viewer\_play\_pause - Play/Pause a selected surface if it contains a video
  * viewer\_stop - Stop a selected surface if it contains a video
  * viewer\_savecapture - Select where to save the next live video capture to
  * display\_quit - Quit Vusion
  * display\_fullscreen = Activate/Deactivate fullscreen mode for the main window

## Live Section ##
The live section contains the settings for live video feeds.

  * driver - Currently only 'video4linux' is supported.
  * device - A list of video devices seperated by a semi-colon
  * input - A list of input sources seperated by a semi-colon (These relate to above. Ie if device is /dev/video0;/dev/video1 and input is 0,1 then /dev/video0 will have the input 0 and /dev/video1 will have the input 1)
  * freq - A list of frequencies seperated by a semi-colon (For use if the input source is TV. If the input source is Composite, etc. specify the frequency as 0)

## Video Section ##
The video section contains the settings for videos.

  * driver - What library to do video processing. Currenently only 'pygame' is supported.  The pygame driver only supports MPEG1
  * seek\_seconds - The amount of time to skip if you seek left or right.
  * play\_audio - Play audio in the movie
  * infinite\_loop - Keep looping the video forever
  * auto\_start - Automatically start the video once loaded into a surface

## Messages ##
The messages section lets you configure the VusionError module.

  * notices - A notice is normally a debug message. These don't need to be read really.
  * warnings - Warnings occur when something like a non-existant driver is sepcified. Non-fatal errors
  * logfile -  file to log warnings and errors to (Logs warnings regardless of the above setting. Does not log notices.)