# Setup Project
Download and Install the db driver from https://www.devart.com/odbc/postgresql/download.html
Open a powershell in the path ./StockTrackerDB and start database with the docker-compose up command 
Setup your email settings in ./EmailAlertService/settings.json
Start the EmailAlertService with the py ./EmailAlertService/program.py
Start the StockHistoryService with the py ./StockHistoryService/program.py
Start the api with the py ./StockMonitorApi/program.py