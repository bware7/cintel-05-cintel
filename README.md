# cintel-05-cintel

This repository contains a PyShiny-based interactive app demonstrating continuous intelligence concepts with live data updates. The app simulates real-time temperature readings and visualizes the data using a chart with a regression trend line.

## Features
- Real-time temperature updates displayed in a value box.
- Recent temperature readings shown in a data grid.
- Interactive chart displaying temperature trends with a regression line.
- Built with PyShiny and related libraries for a responsive user experience.

## Project Structure
- `dashboard/app.py`: Main application file for the PyShiny app.
- `requirements.txt`: Contains the Python dependencies for the project.
- `.gitignore`: Specifies files and directories to be ignored by Git.

## Requirements
The following Python packages are required:
- `shiny`
- `shinylive`
- `faicons`
- `pandas`
- `pyarrow`
- `plotly`
- `scipy`
- `shinywidgets`

## How to Run
1. Clone the repository:
```bash
   git clone https://github.com/bware7/cintel-05-cintel.git
   cd cintel-05-cintel
```

**Set up a virtual environment and install dependencies:** 
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Run the app:** 
```bash
shiny run --reload --launch-browser dashboard/app.py
```

## GitHub Pages
The app is also hosted via GitHub Pages. [cintel-05-cintel](https://bware7.github.io/cintel-05-cintel/)