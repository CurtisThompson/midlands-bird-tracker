# Midlands Bird Tracker

This repository can be used to generate a daily report of bird sightings in the English Midlands. The pipeline pulls data from multiple sources and compiles them into a single HTML report; this report is compatible with email clients. An included GitHub Actions workflow runs this pipeline daily as well as send out the report by email.

## Set-Up

To run the Python pipeline on it's own, run the following command:

```
python run_pipeline.py
```

This will run all data collection, processing, and report generation but will not send the report via email.

For additional configuration of the pipeline, modify the variables within `./config/config.yaml`.

### GitHub Actions and Secrets

If you wish to run the report sending yourself then you will need to fork this repository.

Once you have forked the repository, you need to create three secrets within GitHub Secrets:

|Secret Name|Description|
|---|---|
|EMAIL_CONNECTION_PASSWORD|The password of the sender's email server.|
|EMAIL_CONNECTION_RECIPIENT|The email address(es) to send the report to.|
|EMAIL_CONNECTION_USERNAME|The username (email or code) of the sender's email server.|

To send the report with Gmail, see the information provided by the [Send Email Action](https://github.com/marketplace/actions/send-email). You need to set up an app password instead of using your regular email password. Once this is set up, the report will be sent daily using GitHub Actions.

## Data Sources

Bird sightings are currently collected from the following sources:

 - [The Derbyshire Ornithological Society](https://www.derbyshireos.org.uk/index.php)
 - [Leicestershire & Rutland Ornithological Society](https://lros.org.uk/)
 - [Nottinghamshire Birdwatchers](https://www.nottsbirders.net/index.html)

Please create a pull request to include more sources from across the Midlands.
