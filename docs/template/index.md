# novelyst_timeline

The [novelyst](https://peter88213.github.io/novelyst/) Python program helps authors organize novels.  

The *novelyst_timeline* plugin synchronizes projects with [Timeline](https://peter88213.github.io/yw-timeline).

## Features

- Generate a *Timeline* project from a *yWriter* project.
- Synchronize *yWriter* scenes with corresponding *Timeline* events in both directions.
- When synchronizing a yWriter project with a timeline, optionally change unspecific scene "Day/Hour/Minute" to specific "date/time" and vice versa.
 
## Requirements

- [Python 3.7 or above](https://www.python.org). 
- [Timeline 2.4 or 2.5](https://sourceforge.net/projects/thetimelineproj/). Versions below 2.4 do not support labels, which are necessary for synchronization with yWriter.
- [novelyst](https://peter88213.github.io/novelyst/) version 1.0.0+


## Download and install

[Download the latest release (version 0.99.0)](https://raw.githubusercontent.com/peter88213/novelyst_timeline/main/dist/novelyst_timeline_v0.99.0.zip)

- Unzip the downloaded zipfile "novelyst_timeline_v0.99.0.zip" into a new folder.
- Move into this new folder and launch **setup.pyw**. This installs the plugin.

*Note: If you install *novelyst* at a later time, you can always install the plugin afterwards by running the *novelyst_timeline* setup script again.*

### Launch from novelyst

The plugin's features are accessible via the **Tools > Timeline** submenu in *novelyst*.

The submenu has the following entries:

- Information (compare yWriter and timeline file dates)
- Update timeline from yWriter
- Update yWriter from timeline
- Edit timeline (launch Timeline)

If you install *novelyst* at a later time, you can always install the plugin afterwards by running the *yw-timeline* setup script again.

### Note for Linux users

Please make sure that your Python3 installation has the *tkinter* module. On Ubuntu, for example, it is not available out of the box and must be installed via a separate package. 

------------------------------------------------------------------

[Changelog](changelog)

## License

This is Open Source software, and the *novelyst_timeline* plugin is licenced under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/novelyst_timeline/blob/main/LICENSE) file.


 




