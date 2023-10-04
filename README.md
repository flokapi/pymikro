# About

Python module to control the Maschine Mikro MK3. It allows you to use this maschine not only to create music, but also to control a home automation or a robot or any other creative stuff.

It uses directly the USB HID protocol, as a result there is no dependency on a product specific driver and it can run on any operating system. Furthermore, this gives you access to the full capabilities of this hardware which makes it even more fun to use.



# Usage

```python
import pymikro

maschine = pymikro.MaschineMikroMk3()

# control LEDs
lState = {
    'button': {
        'stop': {'val': 1}
    },
    'strip': {
        1: {'val': 3, 'color': 'blue'}
    },
    'pad': {
        1: {'val': 3, 'color': 'purple'}
    }
}
maschine.setLights(lState)

maschine.setLight('pad', 6, 3, 'orange')
maschine.setLight('strip', 5, 3, 'green')
maschine.setLight('button', 'notes', 4)
maschine.updLights()

# control screen
maschine.setScreen("Hello World!\nIt's working")

# get button and pad updates
while True:
    cmd = maschine.readCmd()
    if cmd:
        if cmd['cmd'] == 'pad':
            print('Pad number {} pressed: {}'.format(cmd['pad_nb'], cmd['pad_val']))
        if cmd['cmd'] == 'btn':
            print('Buttons pressed: {}'.format(cmd['btn_pressed']))
```



# Setup

### Linux

Install the hid driver

```
sudo apt-get install libhidapi-hidraw0
```



Install the package

```
pip3 install pymikro
```



Set permissions for the device

```
cd /tmp
wget https://raw.githubusercontent.com/flokapi/pymikro/main/50-ni-maschine.rules
sudo cp 50-ni-maschine.rules /etc/udev/rules.d/
```



Plug or re-plug the maschine mikro USB cable.



### Windows

Install the hid driver:

1. Donwload the latest version of `hidapi-win.zip` from https://github.com/libusb/hidapi/releases

2. Extract the zip file and copy the `hidapi.dll` corresponding to your architecture to `C:\Users\<Username>\AppData\Local\Programs\Python`



Install the package

```
pip3 install pymikro
```



Plug or re-plug the maschine mikro USB cable.



# About

### Supported hardware features

Overall, there is actually more feature than the manufacturer uses :)



Pads:

- Set color (17 possible values) and intensity
- Get pressure value
- Info whether pressed, touched, or released

Buttons:

- get buttons being pressed
- set light brightness

Encoder:

- get value of the encoder (1 byte), and how much it moved
- whether it's being touched (not pressed)

Touch strip:

- get position of up to 2 fingers
- set color and brightness of each LED

Screen:

- set text with adjustable size, on 1 or 2 lines



### Supported operating systems

Tested on Linux &  Windows

Should also work on OSX by installing the hid api. See https://pypi.org/project/hid/



### API

#### Connection

```python
import pymikro

maschine = pymikro.MaschineMikroMk3()
maschine.showConnInfo()
```



#### Inputs

LEDs:

- The state of the LEDs for the pads/touch strip/buttons is defined in a single data-structure which can be accessed and modified using the  `getLights`  and`setLights` methods. The LEDs can also be set individually using `setLight`.

- To apply the changes, `updLights` must be called. Using a separate command allows to apply all the changes in a single write procedure (about 15ms) and increases the reactivity.

- Example:

  ```python
  maschine.setLights({})                         # set empty dictionary to disable all LEDs
  maschine.updLights()
  
  time.sleep(1)
  
  lState = {
      'button': {
          'stop': {'val': 1}                     # Button brighness value must be between 0 
      },
      'strip': {
          1: {'val': 4, 'color': 'blue'}         # Touch Strip LED brightness value must be between 0 and 3
      },
      'pad': {
          1: {'val': 3, 'color': 'purple'}       # Pad brightness value must be between 0 and 3
      }
  }
  maschine.setLights(lState)
  
  maschine.setLight('pad', 6, 3, 'orange')       # pad nb 6, brightness 3. 
  maschine.setLight('strip', 5, 3, 'green')      # strip led nb 5, brightness 3.
  maschine.setLight('button', 'notes', 4)        # button 'notes', brightness 4.
  maschine.updLights()
  ```

  

Screen

- Example

  ```python
  maschine.setScreen("Hello", 24)                       # Font size set to 24
  
  maschine.setScreen(f"Hello World!\nIt's working")     # Printing text on both lines with '\n'. 
                                                        # Default font size is 14
  ```



#### Outputs

Output commands can be read in a nonblocking way using the `readCmd` method, which returns:

- `None` if no new command is available
- A dictionary which content differs depending on the `cmd` key value (`btn` or `pad`)
- Example: `cmd = maschine.readCmd()`



Pads

- The pad command is only sent when the state of a pad is being changed (pressed/touched/released). The pad command is sent for a single pad at the time.

- Example

  ```python
  {
      'cmd': 'pad', 
      'pad_nb': 5, 
      'pad_val': 1360,                                 # between 0 and 4095
      'touched': True,                                 # finger in contact with the pad
      'pressed': False,                                # finger just pressed the pad (not 100% reliable)
      'released': False                                # finger just released the pad (not 100% reliable)
  }
  ```

  

Buttons:

- The button command is only sent when the state of the buttons/touch strip/encoder changed (including button release). The command contains the full state of the button group.

- Example

  ```python
  {
      'cmd': 'btn', 
      'btn_pressed': ['group', 'pattern', 'enter'],   # currently pressed buttons
      'encoder_pos': 10,                              # byte, cyclic value between 0 and 15
      'encoder_move': 1,                              # encoded moved to the right (+1) or left (-1)
      'encoder_touched': True,                        # finger in contact with the encoder
      'strip_pos_1': 123,                             # value of the strip if one finger touching
      'strip_pos_2': 0                                # second value if another finger is on the strip
  }
  ```




### Alternatives

[maschine-mikro-mk3-driver](https://github.com/r00tman/maschine-mikro-mk3-driver)

- Built for Linux only
- Makes the Maschine Mikro available through a midi interface
- Coded in Rust



Midi mode

- Windows/OSX only (midi interface emulated by the driver)

- press `shift` and `project` to enter midi mode
- you can use [mido](https://pypi.org/project/mido/ ) or any other software to handle the midi commands
- limited features/customization
