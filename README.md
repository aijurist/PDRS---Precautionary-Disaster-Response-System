
FORUS - FOCUSED OPERATIONAL RESCUERS UNIFIED SYSTEM




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
```






## API Reference

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

```
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
```
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

```
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