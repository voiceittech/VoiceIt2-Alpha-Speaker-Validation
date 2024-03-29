# VoiceIt2 Speaker Validation (Alpha) Client Examples
> Andrew Lee ([andrew@voiceit.io](mailto:andrew@voiceit.io))

## Description

This repository contains HTTP clients implemented in various languages which tests all possible enrollment/verification combinations for two example users and their files:

- user A enrollment files against user A verification file
- user A enrollment files against user B verification file
- user B enrollment files against user B verification file
- user B enrollment files against user A verification file

When running the client, you will need to specify whether you want to target the **text dependent engine** (`siv3`) or the **non-text dependent engine** (`siv4`) using the an argument argument.

---

## Examples

| Language | Directory |
| --- | --- |
| Python | [`examples/python`](examples/python) |
| Node JS | [`examples/node`](examples/node) |

---

## SIV3/SIV4 API Specs

### Authentication

You will need to sign up for a VoiceIt account at [https://voiceit.io/signup](https://voiceit.io/signup), and utilize your API Key and API Token passed as Basic Auth credentials as part of the request.

An API Key will look like `key_00000000000000000000000000000000` and API Token looks like `tok_00000000000000000000000000000000`.

### Request Body (Multipart Form Upload):

| Key | Field Type | Description |
| -- | -- | -- |
| json | multipart text field | Defines file keys for enrollment and verification as well as the `uniqueId` |
| (enrollmentFile1, enrollmentFile2, enrollmentFile3...) [1 or more fields] | multipart data field | Enrollment files (keys must match the elements in the string array for `enrollmentsFileKeys` in `json` |
| (verificationFile) | multipart data field | Verification file (key must match the string stored under `verificationFileKey` in the `json` |


### Request JSON Fields: 

| Key | Data Type | Description |
| -- | -- | -- |
| enrollmentsFileKeys | `string array` | Multipart form data keys for the server to find enrollment files |
| verificationFileKey | `string` | Multipart form data key for server to find verification file |
| uniqueId | `string` | Used to save files, and also contained in the response JSON |



### JSON Response

| Key | Data Type | Description |
| -- | -- | -- |
| confidence | `float` | Confidence that verification file is from the same user as enrollment files |
| message | `string` | Used to convey whether or not the request succeeded or why it failed |
| statusCode | `integer` | |
| threshold | `float` | |
| uniqueId | `string` | Matches `uniqueId` from request |

Please read the source code for more detailed usage.

---

## Audio Requirements

During this alpha stage, the SIV3 recording file must be at between 1.5 seconds and 5 seconds long and with a minimum of 1.3 seconds of continuous human speech with max pause between phonetics of 500 miliseconds (no long pauses) in the recording. the SIV4 recording file must be between 500 miliseconds and 15.0 seconds with a minimum of 400 miliseconds of continuous human speech with max pause between phonetics of 1200ms (no long pauses) in the recording.

## Using Status Code
If the status code was not 200 in the JSON response, the request failed for some reason. Please refer to the message to figure out why.
