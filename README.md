# Extract oVirt engine VM details to CSV

## Description

This project provides scripts to extract virtual machine details from an oVirt-engine and save them to a CSV file. The scripts are written in Python and are compatible with Python 3.6 and above. The scripts have been tested on Ubuntu 22.04, Oracle Linux 8, and Oracle Linux 9.
. The scripts included are:

- `install-ubuntu.sh`: Installs the necessary Python dependencies for running the project on Ubuntu-based systems.
- `install-oracle.sh`: Installs the necessary Python dependencies for running the project on Oracle Linux-based systems.
- `get-cert.sh`: Extracts the SSL certificate in PEM format from a specified oVirt cluster's hostname and port, and saves it to a file named `cert.pem`.
- `main.py`: Queries all virtual machines from the oVirt-engine and saves the details to a CSV file named `vms.csv`.

## Usage

1. Choose the appropriate installation script based on your operating system:
   - For Ubuntu-based systems, run `install-ubuntu.sh`.
   - For Oracle Linux-based systems, run `install-oracle.sh`.

   These scripts will install the necessary Python dependencies to ensure the project functions correctly.

2. Run `get-cert.sh` to extract the SSL certificate from the oVirt cluster. Provide the hostname of the cluster and its port as command-line arguments. The certificate will be saved in the current directory as `cert.pem`. Example usage:

   ```shell
   ./get-cert.sh
   ```

The script will prompt for the hostname and port of the oVirt cluster.

3. Finally, execute the main script `main.py` to perform the desired operations. This script queries all virtual machines from the oVirt-engine and saves the details to a CSV file named `vms.csv`. Use the following command:

   ```shell
   python3 main.py
   ```

Ensure that the Python dependencies are installed and the SSL certificate (`cert.pem`) is present in the same directory as `main.py` before running this command.

## Compatibility

The scripts have been tested and verified to work on the following operating systems:

- Ubuntu 22.04
- Oracle Linux 8
- Oracle Linux 9