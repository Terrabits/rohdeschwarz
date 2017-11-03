Cal Unit Control
================

A R&S Calibration Unit connected to a R&S VNA can be manually controlled, and the data for the standards can be extracted by the user via SCPI commands.

Control cal unit standards
--------------------------

R&S cal units can be set to four different states:

- Open
- Short
- Match
- Thru

These can be controlled by the user via SCPI commands; this feature is not available via the VNA user interface.

The SCPI commands are:

`SYST:COMM:AKAL:CONN OPEN, <port>`  
`SYST:COMM:AKAL:CONN SHOR, <port>`  
`SYST:COMM:AKAL:CONN MATC, <port>`  
`SYST:COMM:AKAL:CONN THR, <port1>, <port2>`

NOTE: Because the cal unit may not be physically capable of presenting all these states simultaneously, it is best to use them one at a time.

Data Extraction
---------------

The data is stored in flash in touchstone files on the cal unit itself. To read the data, the files must exported to disk on the VNA.

This functionality is not available through the VNA user interface; it is only available via SCPI commands.

### Export factory characterization

The scpi command to exract the factory data is:

`MMEM:AKAL:FACT:CONV '<dest>'`

Where `<dest>` is the destination of the extracted touchstone files on the VNA hard drive.

### Export user characterization

Although the cal unit comes with factory data, some users choose to re-characterize the cal unit. A typical example of this is when the cal unit connector types and genders don't match the setup: by re-characterizing the unit with adapters attached a cal unit with different port types can be created.

This user data is stored on the cal unit and can be extracted as well with the following command:

`MMEM:AKAL:USER:CONV '<dest>'`

Where `<dest>` is the destination of the extracted touchstone files on the VNA hard drive.

Data File naming convention
---------------------------

The files have the following naming convention:

| Standard | SCPI command                             | Note      |
|----------|------------------------------------------|-----------|
| Open     | `CalibrationUnit Open (P<i>).s1p`        |           |
| Short    | `CalibrationUnit Short (P<i>).s1p`       |           |
| Match    | `CalibrationUnit Match (P<i>).s1p`       |           |
| Thru     | `CalibrationUnit Through (P<i>P<j>).s2p` |`<i> < <j>`|

where <i>, <j> are the port number(s) the file holds data for. For thru path files, the port order convention is *`<i> < <j>`*.

NOTE:

Calibration with a R&S cal unit is UOSM unless a user characterization exists. Thus, there may not be any thru data. Check for thru file availability after extraction to avoid errors.

Data Extraction Procedure
-------------------------

The steps to read cal unit data are as follows:

1. Export touchstone files from cal unit to
   VNA hard drive
2. Download files from VNA hard drive to
   local computer (optional: if running script remotely)
3. Read the data from the touchstone files, using the file naming convention to find data for each port (combination) and cal unit state.

Example
-------

The included python script provides an example of how to do control the cal unit and extract the factory cal data. The script uses the `rohdeschwarz` instrument control library and `scikit-rf` (`skrf`) for reading touchstone files.
