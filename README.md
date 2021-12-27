# pycwpanel

pycwpanel is a Python library that interacts with the Control Web Panel (formerly CentOS Web Panel).

At the time of writing this, the library only takes a backup of user accounts' data i.e. home directory and SQL databases and uploads them to an S3 bucket. 

It's recommended to setup a cronjob that executes the backup script atleast once everyday.

More features will be implemented soon that will cover most of CWP's functionalities.

This is just a start :) I am making this in my spare time and I'm looking forward to learn much from making this. Feel free to correct to my coding and Linux skills.


## Requirements
- A working Control Web Panel setup
- CWP API enabled and configured under CWP Settings > API Manager
- AWS S3 bucket name
- AWS S3 key (not to be confused with Access key)
- AWS S3 Access Key
- AWS S3 Secret Key


## Installation

```bash

cd /opt/

# Clone this repo
sudo git clone https://github.com/macnate-digital/pycwppanel.git

# Drop into the repo
cd pycwpanel

# Install the package
sudo pip install pycwpanel

```

## Usage

After installing the package, sourcing the environment, amd providing a `usernames.txt` file at the same directory level, you can run `backup.py` to start making backups of your user accounts data.

```bash
sudo python3.9 backup.py
``

