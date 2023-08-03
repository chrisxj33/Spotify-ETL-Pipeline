# Spotify-ETL-Pipeline

# REPO IN PROGRESS

### **Overview**

This project showcases the development and implementation of an automated ETL (Extract, Transform, Load) pipeline using Apache Airflow, Spotify API, and AWS services (EC2 & S3). The aim of the pipeline is to extract data daily from Spotify's "Top 50 Tracks" playlist, process it, and then load the transformed data into a designated AWS S3 bucket.

The importance of this project lies in its automation and scalability. It leverages Airflow's capabilities to schedule and monitor workflows, ensuring that data extraction and transformation take place seamlessly and consistently, without manual intervention.

Through this project, valuable insights into daily trends and patterns in the "Top 50 Tracks" playlist can be gathered, providing a dynamic snapshot of music tastes and trends. This data can be further utilized for a variety of applications, from music recommendation systems to market research in the music industry.

By leveraging cloud computing capabilities of AWS, the project ensures that the processed data is stored safely and can be accessed or analyzed at any time, from anywhere. This project serves as a powerful demonstration of the ability to manage and automate data workflows, an increasingly valuable skill in today's data-driven business landscape.

Key achievements of the project:

- Built a fully automated and scalable ETL pipeline.
- Integrated and interacted with Spotify API to extract relevant data.
- Utilized Python libraries like Pandas for efficient data processing.
- Successfully implemented permissions and policies using AWS IAM for secure access to S3 buckets.
- Utilized Apache Airflow for workflow scheduling and monitoring.
- Handled all the necessary setup and configurations of the AWS EC2 instance, ensuring a seamless interaction between the cloud server and the Airflow setup.

This project reflects a solid understanding of ETL processes, cloud computing, data wrangling, and task scheduling, underscoring the ability to automate complex workflows and manage large datasets effectively and efficiently.

### ETL Script

This script is an ETL process that extracts songs from the “Top 50 Tracks” playlist from Spotify, processes the data, and saves it to a specified AWS S3 bucket as a CSV file.

**Extract:** Call the Spotify API for the song ID’s and assocaited data.

**Transform:** The raw results, which are in JSON format, are flattened into a pandas DataFrame. Unnecessary columns are dropped and data from columns containing a list of dictionaries are extracted using a function that is applied to each row of the DataFrame. Individual dataframes are merged to form a single dataset.

**Load:** The transformed data is then loaded to an AWS S3 bucket. The DataFrame is converted to a CSV file and saved to a specified S3 bucket as `spotify_data.csv`.

### Airflow Script

This script is used to create and schedule an Apache Airflow Directed Acyclic Graph (DAG) to automate the ETL process defined in the function `run_spotify_etl` that was created in the `spotify_etl.py` file. The script is divided into four distinct sections. Defining the default arguments, defining the DAG, defining the task to be executed and lastly executing the task.

### Launching an EC2 Instance

For the Amazon Machine Image (AMI) we will be using Ubuntu, which is a distribution of the Linux operating system. Ubuntu is commonly used to host Apache Airflow for many reasons such as stability, security and community support. 

As for the virtual machine’s (VM) specs, the t2.medium will be used (specs should meet software requirements, in this case Airflow). A key pair needs to be generated to securely connect to the VM. The key pair file should be saved somewhere securely.

Tweaking the VM’s firewall is important to ensure security. We will be accessing Airflow (which is hosted on the VM) via our web browser from our main PC. Therefor, within the indbound rules, we allow incoming HTTP connections strictly from our IP only. Once everything has been configured the EC2 instance can be launched.

### Configuring EC2 Permissions

To enable our EC2 instance to interact with an AWS S3 bucket such as writing transformed data to it, we need to configure the EC2's permissions to do so. This process involves four main components: Permissions, Policies, IAM Roles, and finally, associating these with our EC2 instance.

**Permission:** These are declarations of what actions are allowed (or denied) on which AWS resources. In our case, we need our EC2 instance to both read from and write to an S3 bucket. We define these specific actions in our permission.

**Policies:** These are documents that contain one or more permissions. Policies are essentially a way to manage and organize permissions. They can be attached to various AWS identities, including users, groups, and roles, granting these identities the capabilities defined within the permissions. We'll incorporate the permission we created (to read and write to S3) into our policy.

**Roles (IAM Roles)**: An IAM role is an AWS identity with associated permission policies. However, unlike a user, a role isn't linked to a specific person but can be assumed by any entity (user, application, or service) that needs it. Roles don't have long-term credentials such as passwords or access keys. Instead, when a role is assumed, AWS provides temporary security credentials. For our use case, we'll create a role and attach the policy (containing our S3 read/write permission) to this role.

**EC2 and Roles**: You can associate an IAM role with an EC2 instance, either during the instance's creation or by attaching the role to an already running instance. Once an EC2 instance has an associated role, any application running on the instance can use the permissions of the role. This is accomplished through AWS SDKs or the CLI, which are designed to retrieve and use the temporary security credentials linked with the role. In our case, we'll associate the EC2 instance with the role we created earlier. Now, our EC2 instance has the necessary permissions to read from and write to our S3 bucket

### Accessing and Setting Up the EC2 Instance

To connect to the VM we will use the SSH client option. This allows us to directly access and manipulate the VM via our PC’s terminal. 

To connect, open your terminal, `CD` into the file where the key pair is stored and paste in the Public DNS (something like `ssh -i "spotify_airflow_project.pem" ubuntu@ec2-xx-xxx-x-xxx.ap-southeast-2.compute.amazonaws.com`)

Once we’re into the VM, the following commands need to be run:

```bash
sudo apt-get update # get any system updates (opional but recommended)
sudo apt install python3-pip # install python onto the system
sudo pip install apache-airflow # install airflow
sudo pip install pandas # install pandas 
sudo pip install s3fs # this package is for mounting amazon s3
sudo pip install Spotipy # required for etl script
```

### Airflow

To start an airflow server run the command `airflow standalone`. A username and password will be supplied, these details need to be stored somewhere securely. 

### Moving Required Files

The script files that were created now need to be moved to the VM. There are a few options such as sending the files, however in this case we will simply create the files, copy and paste the contents and save them.

`CD` into the Airflow folder and then once more into the DAGS folder. Here is where we create all the required files for the DAG to run. Use `sudo nano filename.py` to create the file. A text editor will also pop up, paste the contents and save the file. This needs to be done for the following files:

`spotify_etl.py`

`spotify_dag.py`

To update the changes use `control + c` to suspend Airflow, then use `airflow standalone` once more. Everything is now set up to ETL the data and save it to the S3. We schedule this operation to repeat every 24 hours, updating with a new csv containing fresh songs.
