The [novelyst](https://peter88213.github.io/novelyst/) Python program helps authors organize novels.  

The *novelyst_timeline* plugin synchronizes novelyst projects with [Timeline](https://peter88213.github.io/yw-timeline).

## Features

- Generate a *Timeline* project from a *novelyst* project.
- Synchronize *novelyst* scenes with corresponding *Timeline* events in both directions.
- When synchronizing a novelyst project with a timeline, optionally change unspecific scene "Day/Hour/Minute" to specific "date/time" and vice versa.

## Requirements

- [Timeline 2.4+](https://sourceforge.net/projects/thetimelineproj/). Versions below 2.4 do not support labels, which are necessary for synchronization with yWriter.
- [novelyst](https://peter88213.github.io/novelyst/) version 2.0.0+


## Download and install

[Download the latest release (version 3.0.0)](https://raw.githubusercontent.com/peter88213/novelyst_timeline/main/dist/novelyst_timeline_v3.0.0.zip)

- Unzip the downloaded zipfile "novelyst_timeline_v3.0.0.zip" into a new folder.
- Move into this new folder and launch **setup.pyw**. This installs the plugin.

*Note: If you install novelyst at a later time, you can always install the plugin afterwards by running the novelyst_timeline setup script again.*

## Usage and conventions

See the [instructions for use](usage)

### Note for Linux users

Please make sure that your Python3 installation has the *tkinter* module. On Ubuntu, for example, it is not available out of the box and must be installed via a separate package. 

------------------------------------------------------------------

[Changelog](changelog)

## License

This is Open Source software, and the *novelyst_timeline* plugin is licenced under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/novelyst_timeline/blob/main/LICENSE) file.


 




