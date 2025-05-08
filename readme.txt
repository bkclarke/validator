The validator application is a python tkinter application. 

validator imports a config file and allows the user to compare a directory with that config file.

* can be used to represent wildcard values in filepaths;

config file can be edited in a text editor, or on the config editor tab in the application.

After editing and saving a config file, it does not need to be reloaded to compare against a directory.

Last used config file path will be retained when the application is next opened. 

example config file:

# --- FILES ---
#ctd
ctd/docs/sbe_application_notes/AN64.pdf
ctd/docs/sbe_application_notes/AN64-1.pdf
ctd/docs/sbe_application_notes/AN64-2.pdf
ctd/docs/sbe_application_notes/AN64-3.pdf
ctd/docs/sbe_application_notes/appnote11GeneralFeb11.pdf
ctd/docs/sbe_application_notes/appnote11QSPLOct12.pdf
ctd/docs/sbe_application_notes/appnote31_TCCorrections_Feb10.pdf
ctd/docs/sbe_application_notes/DriftReportNotice.pdf
ctd/docs/sbe_application_notes/GettingtheHighestResolutiononyourECO_v1.pdf
ctd/docs/sbe_application_notes/pres_to_depth_conver.pdf
ctd/docs/software_and_manuals/SBEDataProcessing_7.26.7HighRes.pdf
ctd/docs/software_and_manuals/SBEDataProcessing_Win32_V7.26.7-b40*
ctd/docs/software_and_manuals/Seasave_7.26.7HighRes.pdf
ctd/docs/software_and_manuals/Seasave_ReferenceSheet_001.pdf
ctd/docs/software_and_manuals/SeasaveV7.26.7-b40*
ctd/docs/software_and_manuals/Seaterm_Win32_V1_59*
ctd/docs/software_and_manuals/SoftwareBrochure4PageNov16_0.pdf
ctd/docs/CTD_deck_checklist_EN729*
ctd/docs/SBE11plus_0427_settings_*
ctd/ctd_readme_*

# --- FORBIDDEN ---
draft
DRAFT
Draft

# --- IGNORE ---
#ignored directories will not be checked for forbidden files
adcp/

# --- PASS ---
#passed directories will be checked for forbidden files
ctd/raw/