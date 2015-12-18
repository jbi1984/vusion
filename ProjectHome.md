Vusion is basically a video mixer that supports input from either an image, MPEG-1 encoded video or from a Video4Linux device. Vusion was written in python and uses the pygame library for mixing.

It's designed to be controlled via a MIDI controller rather than a standard mouse or keyboard. I chose to design it this way because MIDI is an invaluable system for theatrical productions and the specific timing of effects is vital. Using MIDI allows Vusion to be easily controlled via a MIDI Show Control application.

Additionally Vusion will eventually support the rm-rf SIPC (Show Inter-Process Communication) Standard which uses dbus to control applications similarly to a MIDI Show Control program.

## Project Status ##

As of November 2007, Vusion is being rewritten to have a better modular and more defined code-structure. The next release of Vusion will probably be 2.0 which will have many new features:

  * Pluggable 2D Effects
  * Pluggable 3D Effects (With OpenGL)
  * Setting transparency for individual surfaces
  * Transitioning between a pre-defined combination of surfaces
  * Improved and powerful XML configuration allowing robust and extensive MIDI control
  * Support for more than 2 surfaces
  * Configuration now in one file that conforms to the rm-rf XML Configuration Document standard
  * Some simple built-in 2D effects: Translate, Rotate, Zoom, Per channel gamma changing
  * Some simple built-in 3D effects: Surface 'flip', Box transition