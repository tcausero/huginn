# huginn
Named for one of the Norse god Odin's ravens who would gather information for him. A package to facilitate the investigation of anomalous spikes in public interest in an entity, then fetch and summarize news stories relevant to those spikes.



## NYT API Usage

This project requires the usage of the New York Times article search API.  Request a key at [developer.nytimes.com](developer.nytimes.com). You'll need to set your NYT API key as a system environment variable. Open the file `~/.bashrc` (or `~/.bash_profile` if the `.bashrc` doesn't exist) in any Unix based system (Mac, Ubuntu, etc), and add the following two lines to the end of the file: 

```
# Setting NYT API Key as an environment variable
export NYT_API_KEY="YOUR_KEY_HERE"
```

Where `YOUR_KEY_HERE`is your NYT API key, enclosed in quotes.

This  is necessary for requesting relevant links for a potential entity's anomalies.