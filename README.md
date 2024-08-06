# YouTube Downloader Application

Downloader Application is an open-source tool designed to help you download YouTube videos and audio effortlessly. With a user-friendly interface, you can input a URL, select the resolution, choose to download audio only.

## Features

- **URL Input:** Simply paste the YouTube URL of the video you want to download.
- **Resolution Selection:** Choose the desired resolution for your video downloads.
- **Audio Only:** Option to download only the audio from a video.

## Technology Used

- **Python:** The core programming language used for the application logic.
- **PyQt6:** Used for the graphical user interface.
- **PyInstaller:** Used to compile the application into an executable.
- **pytube:** Library used to handle the downloading of YouTube videos.

## Installation

### Windows Executable

A pre-compiled executable is available in the `dist` directory. Due to the way it is packaged, it may be flagged as a virus by Windows Defender. Rest assured, it is not a virus. If you have concerns, you can compile the application yourself by following the instructions below.

### Compile from Source

1. **Clone the Repository:**

    ```sh
    git clone https://github.com/nikitairl/YT-download.git
    cd YT-download
    ```

2. **Set Up a Virtual Environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Run the Application:**

    ```sh
    cd app
    python YT-downloader.py
    ```

5. **Compile the Application (Optional):**

    If you want to create an executable:

    ```sh
    pip install -U pyinstaller 
    pyinstaller --onefile YT-downloader.py
    ```

    The executable will be available in the `dist` directory.

## Usage

1. **Open the Application:**
    - If using the executable, double-click to open.
    - If running from source, use `python ./app/YT-downloader.py`.

2. **Enter YouTube URL:** Paste the URL of the video you wish to download.

3. **Select Resolution:** Enter the desired resolution (e.g., 1080).

4. **Audio Only (Optional):** Check the box if you want to download only the audio.

5. **Start Download:** Click the "Download" button and monitor the progress in a console.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. You may use, distribute, and modify this code for non-commercial purposes. For commercial use, please contact the author for permission

## Acknowledgements

- [PyQt6](https://pypi.org/project/PyQt6/)
- [pytube](https://pytube.io/)
- [PyInstaller](https://www.pyinstaller.org/)

Thank you for using Downloader Application!
