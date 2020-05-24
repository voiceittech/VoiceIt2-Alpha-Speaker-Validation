# SIV3/SIV4 (Alpha) Python Client
> Andrew Lee ([andrew@voiceit.io](mailto:andrew@voiceit.io))

## Description

This directory contains Python 3 based http client [client.py](./client.py) which tests all possible enrollment/verification combinations for two example users and their files:

- user A enrollment files against user A verification file
- user A enrollment files against user B verification file
- user B enrollment files against user B verification file
- user B enrollment files against user A verification file

When running the client, you will need to specify whether you want to target the **text dependent engine** (`siv3`) or the **non-text dependent engine** (`siv4`) using the `--target` argument.

---

## Usage

```
git clone https://github.com/voiceittech/VoiceIt2-Alpha-Speaker-Validation.git
cd VoiceIt2-Alpha-Speaker-Validation/examples/python
pip install requests
python3 client.py --target siv4
```

---

## Audio Requirements

During this alpha stage, the SIV3 recording file must be at between 1.5 seconds and 5 seconds long and with a minimum of 1.3 seconds of continuous human speech with max pause between phonetics of 500 miliseconds (no long pauses) in the recording. the SIV4 recording file must be between 500 miliseconds and 15.0 seconds with a minimum of 400 miliseconds of continuous human speech with max pause between phonetics of 1200ms (no long pauses) in the recording.
