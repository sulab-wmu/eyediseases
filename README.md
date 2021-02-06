# Ek-optical

## Process of development

### Back end
* Create a new directory called virtualenvs.  
```bash
mkdir virtualenvs
```
* Enter the newly created directory virtualenvs, and create a virtual environment.  
```bash
cd /path/to/virtualenvs
Python3 -m venv ek_optical
```
* Activate the virtual environment with absolute path.  
```bash
source /path/to/virtualenvs/ek_optical/bin/activate
```
* Enter the ek_optical project directory, and install all the packages needed with pip.  
```bash
cd /path/to/ek_optical
pip install -r requirements.txt
```
* Start the back end service.  
```bash
./scripts/manage_dev.sh run
```
### Front end
* Enter the webapp directory, and install all the needed packages by the following command.  
```bash
npm install package-name
```
## Process of deployment
* Enter the webapp directory and pack all the files of the front end.  
```bash
cd /path/to/webapp
npm run buildprod
```
* Enter ek_optical and pack all the files in the project.  
```bash
python setup.py package
```
* Transfer the packed files to the server.  
```bash
scp -i wmu.pem optical-dist-0+workingcopy.tgz wmu@eyediseases.bio-data.cn:~/
```
* Stop the nginx proxy.  
```bash
sudo systemctl stop nginx
```
* Unpack the files to user optical.  
```bash
tsrunit deploy optical optical-dist-0+workingcopy.tgz
```
* Upgrade the current database.  
```bash
tstool ek manage db upgrade
```
* Run the back end server.
```bash
tsrunit start ek disco_server
```
* Check the running log of the back end server, use 'q' to exit.  
```bash
lesslog ek disco_server log
```
* Start the nginx proxy.  
```bash
sudo systemctl start nginx
```
## Maintenance
* Update the database with the following command. -f stands for the absolute path of the files needed to be updated and -t means whether to clear the original data table.    
```bash
tstool optical manage populate
# example is given below
tstool optical manage populate x19-go -f ~/update/GO/Retinitis/Retinitis.MF.txt -t Ture
```
