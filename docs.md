## API specification for the backend

### 1. Upload Data (Mini Program)

**Description**: Upload user-related data, including steps, pulse rate, anxiety level

**API**: /user/stats/detailed

**Method**: PATCH

**Type of Params**: application/json

**Params Descriptions**:

| Name       | Optional | Type                           | Description                                                              |
| ---------- | -------- | ------------------------------ | ------------------------------------------------------------------------ |
| id         | No       | Integer                        | The id of the user.                                                      |
| steps      | Yes      | `List[List[day, value]]`       | A list of items in the format of `[day, value]`. Defaults to `[]`.       |
| heartrates | Yes      | `List[List[timestamp, value]]` | A list of items in the format of `[timestamp, value]`. Defaults to `[]`. |
| anxieties  | Yes      | `List[List[timestamp, value]]` | A list of items in the format of `[timestamp, value]`. Defaults to `[]`. |

Note: `List[timestamp, val]` is a list with two elements. The timestamp is a POSIX timestamp.

**Returns**:

If an error occurs, the following struct will be returned:

```json
{
    "message": "some messages"
}
```

or

```json
{
    "message": {
        "field-name": "error messages"
    }
}
```

Field-name is the name of any of the variables above.

**Status Code**:

- HTTP 200 means success.
- Errors include:
  - timestamp greater than the current timestamp.
  - Fields don’t exist


## 2. Get Users

**Description**: Get a list of user ids, sorted ascendingly.

**API**: /users

**Method**: GET

**Type of Params**: No

**Params Descriptions**: No

**Returns**: A list of user ids.

**Returns Example**:

```json
{
    "data": [0, 1, 2, 3, 4]
}
```

**Status Code**:
- HTTP 200 means success.
- Errors include:
  - Fields don’t exist (same as 1).


## 3. Get User Info (brief)

**Description**: Get some brief info for a specific user.

**API**: /user/stats/brief

**Method**: GET

**Type of Params**: application/json

**Params Descriptions**:

| Name | Optional | Type    | Description        |
| ---- | -------- | ------- | ------------------ |
| id   | No       | Integer | The id of the user |

**Returns**: User Infos (name, age, gender, anxiety)

**Returns Example**:

```json
{
    "id": 1,
    "name": "Hello World",
    "gender": "Male",
    "age": 25,
    "anxiety": 2.04
}
```

**Status Code**:

- HTTP 200 means success.
- Errors include:
  - Fields don’t exist


## 4. Get User Info (detailed)

**Description**: Get some user info for a specific user.

**API**: /user/stats/detailed

**Method**: GET

**Type of Params**: application/json

**Params Descriptions**:

| Name              | Optional | Type    | Description                                                              |
| ----------------- | -------- | ------- | ------------------------------------------------------------------------ |
| id                | No       | Integer | The id of the user                                                       |
| steps-day         | Yes      | Integer | The number of steps in the past n day. Defaults to 7.                    |
| anxieties-second  | Yes      | Integer | The number of anxieties in the past n seconds. Defaults to 15 seconds.   |
| heartrates-second | Yes      | Integer | The number of pulse rates in the past n seconds. Defaults to 15 seconds. |

**Returns**: User Infos (id, name, age, gender, steps, heartrates, anxieties) where steps, heartrates and anxieties are a list.

The element inside the step list is another list `[day, value]`. Day is the number of days after `01/01/1970`. The value is the number of steps the patient took on that day.

The element inside the heartrates and anxieties is another list `[timestamp, value]`. The timestamp is the POSIX timestamp. The value is the corresponding heart rate/anxiety level at that timestamp.

**Returns Example**:

```json
{
    "id": 1,
    "name": "Lorem Ipsum",
    "gender": "Female",
    "age": 36,
    "steps": [[9200, 2642], [9201, 9237]],
    "heartrates": [[1677383002, 77], [1677383003, 78]],
    "anxieties": []
}
```

**Status Code**:
- HTTP 200 means success.
- Errors include:
  - Fields don’t exist