[Projekt-Homepage](https://peter88213.github.io/novelyst_timeline) > Gebrauchsanleitung

--- 

Ein [novelyst](https://peter88213.github.io/novelyst/)-Plugin providing synchronization with Timeline. 

---

# Installation

- Unzip the downloaded zipfile into a new folder.
- Move into this new folder and launch **setup.pyw**. This installs the plugin.

*Note: If you install novelyst at a later time, you can always install the plugin afterwards by running the novelyst_timeline setup script again.*

Das Plugin hängt einen **Timeline**-Eintrag an das *novelyst* **Extras**-Menü, und einen **Timeline-Plugin Online Hilfe**-Eintrag an das **Hilfe**-Menü an. 

### Launch from novelyst

The plugin's features are accessible via the **Extras > Timeline** submenu in *novelyst*.

The submenu has the following entries:

- Information (compare novelyst and timeline file dates)
- Update timeline from novelyst
- Update novelyst from timeline
- Edit timeline (launch Timeline)

## Custom configuration

You can override the default settings by providing a configuration file. Be always aware that faulty entries may cause program errors or unreadable Timeline projects. If you change a configuration inbetween, previously synchronized projects might no longer match. 

### Global configuration

An optional global configuration file can be placed in the configuration directory in your user profile. It is applied to any project. Its entries override novelyst_timeline's built-in constants. This is the path:
`c:\Users\<user name>\.novelyst\\config\timeline.ini`
  
The setup script installs a sample configuration file containing novelyst_timeline's default values. You can modify or delete it. 

### Local project configuration

An optional project configuration file named `nv-timeline.ini` can be placed in your project directory, i.e. the folder containing your novelyst and Timeline project files. It is only applied to this project. Its entries override novelyst_timeline's built-in constants as well as the global configuration, if any.

### How to provide/modify a configuration file

The novelyst_timeline distribution comes with a sample configuration file located in the `sample` subfolder. It contains novelyst_timeline's default settings and options. This file is also automatically copied to the global configuration folder during installation. You best make a copy and edit it.

- The SETTINGS section comprises the program "constants". If you change them, the program might behave differently than described in the documentation. So only touch them if you are clear about the consequences.
- The OPTIONS section comprises options for regular program execution. 
- Comment lines begin with a `#` number sign. In the example, they refer to the code line immediately above.

This is the configuration explained: 

```
[SETTINGS]

section_label = Section

# Events with this label become sections in a newly created 
# novelyst project. 

default_date_time = 2021-07-26 00:00:00

# Date/time stamp for imported novelyst sections without
# date/time set. When converting between specific
# date/time and unspecific D/H/M, this time stamp is used
# as a reference.

section_color = 170,240,160

# Color for events imported as sections from novelyst.

[OPTIONS]

ignore_unspecific = No

# No:  Transfer all Sections from novelyst to Timeline. Events
#      assigned to sections having no specific date/time stamp
#      get the default date plus the unspecific 'D' as start
#      date, and 'H':'M' as start time.
# Yes: Only transfer Sections with a specific date/time stamp
#      from novelyst to Timeline.

dhm_to_datetime = No

# Yes: Convert novelyst unspecific D/H/M to specific date/time
#      when synchronizing from Timeline.
#      Use the date from default_date_time as a reference.
#      Time is 'H':'M'.
# Precondition:
#      datetime_to_dhm = No

datetime_to_dhm = No

# Yes: Convert novelyst spcific date/time to unspecific D/H/M
#      when synchronizing from Timeline. Use the date from
#      default_date_time as a reference. H, M are taken from
#      the section time.
# Precondition:
#      dhm_to_datetime = No

```


### How to reset the configuration to defaults

Just delete your global and local configuration files.



## Conventions

### General
- The novelyst project file and the Timeline file are located in the same directory.
- They have the same file name and differ in the file extension.
- Either a timeline or a novelyst project is generated from the other file for the first time. After that, the two files can be synchronized against each other.
- **Please keep in mind:** Synchronizing means overwriting target data with source data. Since novelyst_timeline works in both directions, there is always a danger of confusing source and target, thus losing changes. So if the program asks you for confirmation to overwrite a file, better check if it's actually the target file.


### On the novelyst side

- Only normal sections are synchronized with Timeline, or exported to Timeline. Unused sections, "Notes" sections, and "Todo" sections will not show up in the timeline.
- Optionally, sections with an unspecific time stamp (day, hours, minutes) are not transferred to the timeline.
- Changes to the section date/time affect the event start date/time during synchronization.
- Changes to the section title affect the event text during synchronization.
- Changes to the section description affect the event description during synchronization.
- Changes to the section type may add or remove the corresponding event during synchronization.
- Adding or removing sections will add or remove the corresponding event during synchronization.


### On the Timeline side

- A section ID is a string looking like "ScID:1". It is auto-generated and must not be changed manually.
- Only events with a label containing the string "Section" (user input) or a section ID (auto-generated) are exported as sections to a new novelyst project.
- When generating a new novelyst project from a timeline the first time, "Section" labels are replaced with section ID labels.
- If a new novelyst project is generated again with the same timeline, the section ID labels may change.
- Only events with a label containing a section ID are synchronized with an existing novelyst project.
- Changes to the event start date/time affect the section date/time during synchronization.
- Changes to the event text affect the section title during synchronization.
- Changes to the event description affect the section description during synchronization.
- The section structure of an existing novelyst project can not be changed in Timeline. Adding/removing events, or adding/removing section IDs from event labels will *not* add or remove the corresponding section during synchronization. 

### Synchronization of unspecific date/time in novelyst with specific date/time in Timeline.

Day/Hour/Minute is converted to specific Timeline start/end date/time stamps, using the duration and the default date/time.

The other way around (Timeline to novelyst), there are three options:

- Retain each section's date/time mode (default).
- Overwrite D/H/M with specific date/time stamps (**dhm_to_datetime** option).
- Convert specific Timeline date/time stamps to D/H/M (**datetime_to_dhm** option)

D/H/M refers to the default date/time stamp that can be set in the configuration.


### Known limitations

- Section events that begin before 0100-01-01 in the timeline, will not be synchronized with novelyst, because novelyst can not handle these dates.
- The same applies to the section duration in this case, i.e. the event duration in Timeline and the section duration in novelyst may differ.
- Sections that begin before 0100-01-01 in the timeline, can not have the D/H/M information converted to a date/time stamp and vice versa.
- If a section event ends after 9999-12-31 in the timeline, the section duration is not synchronized with novelyst.


---

# Lizenz

Dies ist quelloffene Software, und das *novelyst_timeline*-Plugin steht unter der GPLv3-Lizenz. Für mehr Details besuchen Sie die[Website der GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.de.html), oder schauen Sie sich die [LICENSE](https://github.com/peter88213/novelyst_timeline/blob/main/LICENSE)-Datei an.
