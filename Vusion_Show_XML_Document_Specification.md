# Introduction #
The Show XML Document Specification 1.0 is currently in development and subject to change. This wiki exists to document how to write a file and what elements are required etc.

## Example File ##
```
<vusionshow version="1.0">
   <metadata>
      <author>Chris Stranex</author>
      <title>Example File</title>
      <description>This description isn't ever used by the Vusion application itself but should help editors, etc.</description>
   </metadata>

   <dimensions fullscreen="true">320x240</dimensions>
    
   <default>
      <gamma all="1" />
      <transition value="100" />
      <surface n="a" type="image" file="logo.png?50x20" />
      <surface n="b" type="video" file="amerika.mpg" />
   </default>
   <midi>
         <note n="38" c="1" action="quit()" />
         <note n="39" c="1" action="live.capture_video()" />
         <note n="40" c="1" action="trigger.select_surface_a()" />
         <note n="41" c="1" action="trigger.select_surface_b()" />
         <note n="42" c="1" action="video.control_playpause(?)" />
         <note n="43" c="1" action="video.control_stop(?)" />
         <note n="44" c="1" action="video.control_seek_forward(?)" />
         <note n="45" c="1" action="video.control_seek_backward(?)" />
         <note n="46" c="1" action="trigger.live(1)" />
         <note n="47" c="1" action="trigger.live(2)" />
         <note n="48" c="1" action="trigger.video(welcome.mpg)" />
         <note n="49" c="1" action="trigger.image(sunset.png)"/>
         <note n="50" c="1" action="trigger.video(sponsors.mpg)" />
         <note n="51" c="1" action="trigger.video(end.mpg)" />
         <cc n="11" c="1" change="transition" />         
         <cc n="7" c="1" change="gamma_all" />
   </midi>
</vusionshow>
```

## Elements ##
### vusionshow ###
```
<vusionshow version="VERSION">
...
</vusionshow>
```

This tag is **required**. It is the main tag of the show file. The version is currently 1.0.

Attributes:
  * version - Version number
Children:
  * metadata
  * default
  * midi
  * dimensions

### Metadata ###
```
<metadata>
...
</metadata>
```

This tag is **optional**. It provides information to editors or other applications.

Attributes:
  * none
Children:
  * author
  * title
  * description
  * dateCreated
  * dateModified
  * link

### author ###
` <author>CDATA</author> `

This tag is **optional**. It provides the author's name.

Attributes:
  * email - Email address of the author
Children:
  * none

### title ###
` <title>CDATA</title> `

This tag is **optional**. It provides the name of the show. If Vusion detects this tag it will change the name of the window to "Vusion 0.2 - TITLE" where TITLE is the contents of the tag.

Attributes:
  * none
Children:
  * none

### description ###
` <description>CDATA</description> `

This tag is **optional**. It provides a description of the show.

Attributes:
  * none
Children:
  * none

### dateCreated ###
` <dateCreated>CDATA</dateCreated> `

This tag is **optional**. It provides an [RFC2822](http://www.faqs.org/rfcs/rfc2822) formatted date of creation.

Attributes:
  * none
Children:
  * none

### dateModified ###
` <dateModified>CDATA</dateModified> `

This tag is **optional**. It provides an [RFC2822](http://www.faqs.org/rfcs/rfc2822) formatted date of modification.

Attributes:
  * none
Children:
  * none

### link ###
` <link>CDATA</link> `

This tag is **optional**. It provides a URL from where the show file came.

Attributes:
  * none
Children:
  * none

### dimensions ###
` <dimensions fullscreen="FULLSCREEN">XxY</dimensions> `

This tag is **required**. It tells Vusion the dimensions of the window (in the format WIDTHxHEIGHT) it must draw and if it should be in fullscreen or not.

Attributes:
  * fullscreen - either true or false. Start Vusion in fullscreen mode
Children:
  * none

### default ###
```
<default>
...
</default>
```

This tag is **required**. The default tag contains what visual settings Vusion needs to start up with. For example its gamma, what's loaded on each surface.

Attributes:
  * none
Children:
  * gamma
  * transition
  * surface

### gamma ###
` <gamma all="VALUE" /> `

This tag is optional. By default the gamma is set to 1. r,g,b attributes are optional. Gamma values range from 0 to 255

Attributes:
  * all - Gamma value for RGB.
  * r - Gamma value for Red
  * g - Gamma value for Green
  * b - Gamma value for Blue
Children:
  * none

### transition ###
` <transition value="VALUE" /> `

This tag is optional. By default the transition value is set to 64. This sets the position of transition on screen from 0 (Surface A) to 255 (Surface B).

Attributes:
  * value - An integer between 0 and 127.
Children:
  * none

### surface ###
` <surface n="SURFACE" type="TYPE" file="FILE" /> `

This tag is **required**. The surface tag tells Vusion what to load initally to a surface.

Attributes:
  * n - The surface (either a or b)
  * type - The type the surface is (either: image, video or live)
  * file - The file/index to load. Note: Images support a question mark (?) after the file to specify an X and Y coordinate. Eg: "test.png?100x0" will load the test.png image 100 to the right of the left corner of the screen.

### midi ###
```
<midi>
...
</midi>
```

This tag is **required**. The midi tag keeps all the midi bindings for a midi controller.

Attributes:
  * none
Children:
  * note
  * cc

### note ###
` <note n="NOTE" c="CHANNEL" action="FUNCTION" /> `
At least one tag should be present in a file. This assigns a function to a MIDI Noteon event.

Attributes:
  * n - the note in numerical value
  * c - midi channel (1 - 16)
  * action - The function to execute. See the [MIDI Functions](MIDI_Functions.md) page.

### cc ###
` <cc n="NUMBER" c="CHANNEL" change="ATTRIBUTE" /> `
At least one tag should be present in a file thought it is not required. This assigns an attribute to a MIDI cc event.

Attributes:
  * n - the number of the message
  * c - midi channel (1 - 16)
  * change - The attribute of Vusion to change. See the [MIDI Attributes](MIDI_Attributes.md) page.