# Swiss Tournament pairing

Pairing algorithm for Swiss tournaments. Geared towards the OoT Bingo Tournament.

* Copy `data/entrants.example.json` to `data/entrants.json`, or create your own `data/entrants.json` in the same format.
* Check and possbily change the settings at the top of `main.py`
* Run `main.py`
* When running the first time, the `data/entrants_pairing.json` will be created if it didn't exist yet.
* After running, a new `data/output/entrants_pairing_{timestamp}.json` file will be created, which has the updated data
  from the pairing. Copy the contents to `data/entrants_pairing.json` for the next round of pairing.
