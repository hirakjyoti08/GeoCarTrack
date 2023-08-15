# GeoCarTrack

GeoCarTrack is a Python project that allows you to divide a geographical map into rectangles and track cars within specific time slots in those rectangles. It utilizes the OSMnx library for geographical data retrieval, geopandas for handling spatial data, and other supporting libraries.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python (>= 3.6) installed
- Required Python packages: `osmnx`, `geopandas`, `matplotlib`, `shapely`, `datetime`, `dateutil`, `re`

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/GeoCarTrack.git
    ```

2. Change into the project directory:

    ```bash
    cd GeoCarTrack
    ```

3. Install the required packages using pip:

    ```bash
    pip install osmnx geopandas matplotlib shapely
    ```

## Usage

1. Open the `main.py` file in your preferred Python environment.

2. Modify the following variables according to your needs:

    - `place_name`: The name of the place for which you want to track cars (e.g., "Rome, Italy").
    - `num_rows` and `num_columns`: The number of rows and columns you want to divide the map into.
    - `car_dataset_path`: The path to the directory containing car dataset text files.
    - `time_slot_input`: The desired time slot for car tracking in the format "start_time-end_time" (e.g., "14:00:00-23:00:00").
    - `date_input`: The date for which you want to track cars (format: `YYYY-MM-DD`).
    - `rectangle_id_input`: The ID of the rectangle you want to analyze.

3. Run the script:

    ```bash
    python main.py
    ```

## Output

The script will display a graphical representation of the map divided into rectangles. The selected rectangle will be highlighted in blue, and any cars found within that rectangle and time slot will be listed.

## Acknowledgments

- This project uses the OSMnx library developed by Geoff Boeing (https://github.com/gboeing/osmnx).

## License

OSMnx is open-source software licensed under the MIT License.

