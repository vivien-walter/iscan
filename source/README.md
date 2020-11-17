# iSCAN

How-to compile a iSCAN executable from source files

## Instructions

*Note: The following procedure is designed to generate an executable file for all operating systems. However, the author only tested it on a reduced number of OS.*

1. Make sure you are using **Python 3.5** or **Python 3.6**

2. Download the **/sources/** folder from the GitHub repo.

3. Copy the content of the folder in a new directory on your computer.

4. Create a **virtualenv** (see official documentation below).

5. Install the following modules and packages using **pip** and the provided *requirements.txt* file. This can be done with the command

    ```bash
    pip install -r requirements.txt
    ```

6. Initialise the **fbs** project in the terminal

    ```bash
    > fbs startproject
    ```

    Please use *HPyMon* as the Application name and *VivienWalter* as the author - If you are only compiling and not modifying the source files.

7. Go in the **/src/** folder created by fbs and replace the folder **/main/** by the folder downloaded from the HPyMon GitHub repo in step 1.

8. Create the **executable** by using the command

    ```bash
    > fbs freeze
    ```

    If you want to create an **installer** instead, use the command

    ```bash
    > fbs installer
    ```

## Source(s)

- virtualenv documentation: https://virtualenv.pypa.io/en/latest/

- fbs instructions: https://build-system.fman.io/pyqt-exe-creation/
