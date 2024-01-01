# Spotify ETL (Mini Project)

### Overview

The aim of this project was to introduct myself to a simple data pipeline within the cloud. Here I learnt how to set up Airflow within an EC2 instance using a self managed approach for reduced cost. Additional skills included interacting with the VM via the command-line shell using Bash and networking / security within the cloud.

As a high-level overview of the project itself, I developed an automated data pipeline that extracts daily song information from Spotify's "Top 50 Tracks" playlist. Using an ETL (Extract, Transform, Load) script, the process fetches the song data, processes it into a structured pandas DataFrame, and then stores it into an AWS S3 bucket as a dated `.csv` file. To ensure the ETL process is executed seamlessly on a daily basis, I employed Apache Airflow, orchestrating a Directed Acyclic Graph (DAG) that controls the task sequence and dependencies. This entire operation is hosted on an AWS EC2 instance running the Ubuntu operating system. To enable interaction with the AWS S3 bucket, I configured the EC2 permissions using IAM roles, ensuring the server can both read from and write to the storage bucket. As a result, this setup offers an automated solution, capturing a daily snapshot of Spotify's trending tracks and storing them systematically in a central data repository. Since the infrastructure is cloud-based, there is an easy option for scalability by using a more powerful EC2 instance (vertical scaling).

![Temp](https://github.com/chrisxj33/Spotify-ETL-Pipeline/assets/53899548/712b171e-8bec-45a4-a93e-58ce6e4ae638)

### ETL Script

This script is an ETL process that extracts songs from the “Top 50 Tracks” playlist from Spotify, processes the data, and saves it to a specified AWS S3 bucket as a CSV file.

**Extract:** Call the Spotify API for the ID of each song within the playlist, along with each songs associated data such as mood, artist, etc.

**Transform:** The raw results, which are in JSON format, are flattened into a pandas DataFrame. Unnecessary columns are dropped and data from columns containing a list of dictionaries are extracted using a function that is applied to each row of the DataFrame. Individual dataframes are merged to form a single dataset.

**Load:** The transformed data is then loaded to an AWS S3 bucket. The DataFrame is converted to a `.csv` file and saved to a specified S3 bucket as `spotify_data_date.csv`.

### Airflow Script

This script is used to create and schedule an Apache Airflow Directed Acyclic Graph (DAG) to automate the ETL process. The airflow script essentially calls the function defined in the script previously created, `spotify_etl.py`.

### Launching an EC2 Instance

For the Amazon Machine Image (AMI) we will be using Ubuntu, which is a distribution of the Linux operating system. Ubuntu is commonly used to host Apache Airflow for many reasons such as stability, security and community support. 

As for the virtual machine’s (VM) specs, the t2.medium will be used (the specs need to meet Airflows requirements). A key pair is generated to securely connect to the VM and this is stored securely.

Tweaking the VMs firewall is important to ensure security. We will be accessing Airflow (which is hosted on the VM) via our web browser from our main PC. Therefor, within the indbound rules, we allow incoming connections strictly from our IP only. Once everything has been configured the EC2 instance can be launched.

### Establishing an Amazon S3 Bucket

Amazon S3 bucket is a perfect tool to utilise as our data lake due to its affordability and capacity to store semi-structured data (like the data we will be collecting). This bucket is our primary data reservoir, in which we accumulate and store the data extracted from Spotify every 24 hours.

For instance, each day when the data is pulled, we can store it as a separate file. This approach not only enables us to have a well-organised repository of daily data, but it also provides us with a historical record of each .csv file.

### Configuring EC2 Permissions

To enable our EC2 instance to interact with an AWS S3 bucket such as writing data to it, we need to configure the EC2s permissions to do so. This process involves four main components: Permissions, Policies, IAM Roles, and finally, associating these with our EC2 instance.

Permissions are declarations of what actions are allowed (or denied) on which AWS resources. In our case, we need our EC2 instance to both read from and write to an S3 bucket. We define these specific actions in our permission. Then, we'll associate the EC2 instance with the role we created. Now, our EC2 instance has the necessary permissions to read from and write to our S3 bucket

### Accessing and Setting Up the EC2 Instance

To connect to the VM, the SSH client option is used. This allows us to directly access and manipulate the VM via our PCs terminal. The public DNS (`ssh -i "spotify_airflow_project.pem" ubuntu@ec2-xx-xxx-x-xxx.ap-southeast-2.compute.amazonaws.com`) is used to connect.

Once we’re into the VM a virtual environment is created. The virtual environment just makes it easier to organise our code, dependencies, etc into a single directory. Then the required packages are installed. The following commands that were run are below:

```bash
sudo apt-get update # get any system updates
sudo apt install python3-pip # install Python3 onto the system
sudo pip install apache-airflow # install Airflow

# all packages required for the scripts
sudo pip install boto3
sudo pip install pandas
sudo pip install sqlalchemy
sudo pip install spotipy
sudo pip install psycopg2-binary
sudo pip install s3fs
```

### Airflow

The Airflow server is started by running the command `airflow standalone`. A username and password is created and this is stored securely. We can access the Airflow management interface from our main PCs browser by using our EC2 public DNS and the port that Airflow is listening on.

### Moving Required Files

The scripts that were created now need to be moved to the VM. There are a few options such as sending the files, however in this case we will simply create the files, copy and paste the contents, and save them.

We `CD` into into the DAGS folder. Here is where we create all the required files for the DAG to run. Use `sudo nano filename.py` to create the file. Paste the contents and save the file. This needs to be completed for the following files:

`spotify_etl.py`

`update_database.py`

`spotify_dag.py`

To update the changes use control + c to suspend the Airflow server, then use `airflow standalone` once more to "restart". Everything is now set up to ETL the data and save it to the S3. We schedule this operation to repeat every 24 hours, updating the S3 container with a new `.csv` containing fresh songs.

### Results

Below is how the data looks within the S3 Bucket. A new file is created for each daily snapshot.

![Untitled (1)](https://github.com/chrisxj33/Spotify-ETL-Pipeline/assets/53899548/6f290e53-0325-4a73-8e29-f5a6b406f2c4)

A couple of lines from from the `.csv` file showing the structure.

![Untitled](https://github.com/chrisxj33/Spotify-ETL-Pipeline/assets/53899548/66d55c23-bad2-4cf1-8e32-b803637d2448)

From here any additional operations can be carried out, such as preparing and storing the data into a relational database or warehouse like Redshift for analytics.
