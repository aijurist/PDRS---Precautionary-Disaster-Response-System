
# FORUS - FOCUSED OPERATIONAL RESCUERS UNIFIED SYSTEM
FORUS is a comprehensive Disaster Management and Control project designed to:

- Minimize Wait Times: Reduce delays in taking action during disaster situations.
- Identify Potential Disaster Areas: Predict and pinpoint regions where disasters might occur.
- Provide Detailed Reports: Generate thorough reports for each disaster event.
- Analyze Social Media: Utilize social media tweets to identify and verify disaster occurrences.
This system integrates real-time data analysis and verification to enhance disaster response and management efforts.


## Installation

Install FORUS by first cloning the repo using the command

```bash
git clone "https://github.com/aijurist/HACKFEST_24.git"
```

Then create a venv using VS code by doing the following 

- Open the cloned repo using VS code
- Go to the top searchbar of the project and choose ```Show and run commands``` or use ```Ctrl + Shift + P```
- Search for ```Python: Create Environment```
- Choose ```.conda``` if available else choose ```.venv```

To install the all packages run the command 

```bash
pip install -r requirements.txt
```

To run the Flask Application run the command 
```bash
python -u "./python/app.py" 
```## API Reference

#### Webscrape Twitter and get prediction results

```http
POST /api_twitter/scrape_twitter
```
The request body should be a JSON object with the following structure:
| Field | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. Your twitter username |
| `password` | `string` | **Required**. Your twitter password |
| `tweet_count` | `number` | Number of tweets to webscrape|

The response body will be something like 
```json
{
    "predictions": {
        "1": {
            "confidence": [
                0.9344901442527771,
                0.0655098706483841
            ],
            "hashtags": [
                "#unionbudget",
                "#india",
                "#growth",
                "#dns",
                "#PMOIndia",
                "#FinanceMinistry"
            ],
            "mentions": [
                "@delhinewstation"
            ],
            "prediction": 0,
            "text": "delhinewsstation @delhinewstation · 52s Parliament's Monsoon Session begins on Monday and will have 19 sittings till August 12 when the government is expected to present six bills. #unionbudget #india #growth #dns #PMOIndia #FinanceMinistry PMO India and Nirmala Sitharaman 2"
        },
    },
}
```

#### Get Report

```http
POST /api_model/get_report
```

The request body should be a JSON object with the following structure:

| Field | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `tweet`      | `string` | **Required**. Tweet to generate report for |
| `population`      | `dict` | **Required**. Population to take consideration for |

The response body will be something like 
```json
{
    "first_responder_count": 500,
    "number_of_camps": 5,
    "number_of_people": 342178,
    "supplies_required_count": {
        "food": {
            "cold-freeze foods": 2385710,
            "hot foods": 2737424,
            "snacks": 684350
        },
        "medicine": {
            "first aid kits": 6844,
            "iv drips": 3422,
            "other necessities": 10265
        },
        "water": 1026540
    },
    "validity_of_disaster": false
}
```

#### Get Coordinates

```http
POST /api_validation/get_population
```

The request body should be a JSON object with the following structure:

| Field | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `lat`      | `number` |  Latitude Of location |
| `lon`      | `number` |  Longitude Of location |
| `location_name`      | `string` |  Name of the affected location due to natural disaster |
| `radius`      | `number` |  The radius of impact of population to get |
| `is_urban`      | `boolean` |  if the location is an urban or an rural area |

Be sure to either give Latitude and Longitude values or the location_name atleast to find the population of the location

The response body will look something like 
```json
{
    "population_split": {
        "adults_18_44": 125594,
        "adults_45_59": 62797,
        "adults_60_plus": 31398,
        "children": 94195,
        "female_population": 151214,
        "male_population": 162771
    },
    "status": "success",
    "total_population": 313985
}
```

#### Get Coordinates
```http
POST /api_validation/get_coordinates
```

The request body should be a JSON object with the following structure:
| Field | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `location_name`      | `string` |  **Required** Location to get coordinates of |


The response body will look something like 
```json
{
    "latitude": 13.0294483,
    "location_name": "T. Nagar, Chennai, Tamil Nadu",
    "longitude": 80.2309064,
    "status": "success"
}
```

#### Finding location name from twitter tweet

```http
POST /api_validation/location_finder_twitter
```

The request body should be a JSON object with the following structure:
| Field | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `tweet`      | `string` |  **Required** The tweet to find the location of, if the tweet contains any location |

The response body will look something like 
```json
{
    "locations": {
        "coordinates": {
            "latitude": null,
            "longitude": null
        },
        "location": "Kurla, Mumbai"
    },
    "status": "success"
}
```

Note that the response of this endpoint might return null in some cases

# Using Ngrok for hosting 

- Download ngrok from the official website ```https://ngrok.com/download```

- Start the Flask application by using the command given ```python -u "./python/app.py" ```

- Open the ngrok.exe file and use the command:  
```bash
ngrok http 8080
```

An API Gateway to access the Flask application endpoints has been created
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`GEMINI_API_KEY`

`SERVICE_ACCOUNT_KEY`

#### GEMINI_API_KEY

-  Head to `https://aistudio.google.com/`
- Choose to create a new API key and create one

#### SERVICE_ACCOUNT_KEY

- Go to Google and search `GCP console`
- Head over to the console and press the menu towards the left
- Go to IAM and Billing and search for Service accounts
- Click on `Create new service account` and give the service account a name and a description
- Under `Grant this service account access to project`, grant the Project -> Editor role.
- Click Done
- After creating the service account, click on the service account name.
- Go to the "Keys" tab.
- Click "Add Key" > "Create New Key".
- Choose JSON and click "Create".
- A JSON key file will be downloaded to your computer. Keep it secure.
- Now navigate to the python directory in the project and paste the downloaded JSON key file there

Create a .env file in the same directory and structure it in the following manner

```code
GEMINI_API_KEY= {Your GEMINI_API_KEY}
SERVICE_ACCOUNT_KEY=python/{file_name}.json
```


