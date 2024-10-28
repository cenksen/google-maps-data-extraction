# Google Maps Data Extraction

A script for extracting data from Google Maps.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/cenksen/google-maps-data-extraction.git
   cd google-maps-data-extraction
    ```

2.Install the required packages:
  ```bash
    pip install -r requirements.txt
   ```
3.Install the package:
  ```bash
    pip install .
   ```

## Usage

You can run the script using the following command:
 ```bash
google-maps-extract --search "Restaurant" --location "Turkey" --total 100
 ```

## Parameters
- --search: The term you want to search for (default is "Restaurant").
- --location: The location you want to search in (default is "Turkey").
- --total: The total number of listings to extract (default is 100).

## Output
The extracted data will be saved in the /output directory in the following formats:

- CSV (result.csv)
- JSON (result.json)
- HTML (result.html)

## Requirements
Make sure you have Python 3.x installed, along with the following packages:

- pandas
- playwright

## License
This project is licensed under the MIT License - see the LICENSE file for details.


## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.

